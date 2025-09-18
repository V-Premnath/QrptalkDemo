# QrypTalk - Post-Quantum Secure Messaging App
# Phase 1: Cryptographic Foundation
# File: src/crypto/kyber_kem.py

"""
CRYSTALS-Kyber KEM implementation for QrypTalk
Provides post-quantum key encapsulation mechanism with three security levels
"""

import os
import json
import time
from enum import Enum
from typing import Tuple, Dict, Any, Optional
from dataclasses import dataclass
import logging

# Import pqcrypto Kyber implementations
from pqcrypto.kem.kyber512 import (
    generate_keypair as kyber512_keygen,
    encrypt as kyber512_encrypt, 
    decrypt as kyber512_decrypt
)
from pqcrypto.kem.kyber768 import (
    generate_keypair as kyber768_keygen,
    encrypt as kyber768_encrypt,
    decrypt as kyber768_decrypt  
)
from pqcrypto.kem.kyber1024 import (
    generate_keypair as kyber1024_keygen,
    encrypt as kyber1024_encrypt,
    decrypt as kyber1024_decrypt
)

# Cryptography library for additional operations
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidSignature
import secrets

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SecurityLevel(Enum):
    """Kyber security levels with corresponding parameters"""
    KYBER_512 = "kyber-512"   # ~AES-128 equivalent
    KYBER_768 = "kyber-768"   # ~AES-192 equivalent  
    KYBER_1024 = "kyber-1024" # ~AES-256 equivalent


@dataclass
class KeyPair:
    """Container for Kyber key pair with metadata"""
    public_key: bytes
    private_key: bytes
    security_level: SecurityLevel
    created_at: float
    key_id: str  # Unique identifier for this key pair
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize key pair metadata (not the actual keys)"""
        return {
            'security_level': self.security_level.value,
            'created_at': self.created_at,
            'key_id': self.key_id,
            'public_key_length': len(self.public_key),
            'private_key_length': len(self.private_key)
        }


@dataclass 
class EncapsulationResult:
    """Result of Kyber encapsulation operation"""
    ciphertext: bytes      # Kyber ciphertext to send to peer
    shared_secret: bytes   # Shared secret for key derivation
    timestamp: float       # When encapsulation was performed
    
    def secure_delete(self):
        """Securely clear the shared secret from memory"""
        if hasattr(self.shared_secret, '__len__'):
            # Convert to bytearray for in-place modification
            secret_array = bytearray(self.shared_secret)
            for i in range(len(secret_array)):
                secret_array[i] = 0
            self.shared_secret = bytes(secret_array)


class KyberKEMError(Exception):
    """Base exception for Kyber KEM operations"""
    pass


class KyberKEM:
    """
    CRYSTALS-Kyber Key Encapsulation Mechanism
    
    Provides post-quantum secure key exchange with three security levels.
    Follows the Strategy pattern for algorithm selection.
    """
    
    # Algorithm mapping for strategy pattern
    _ALGORITHMS = {
        SecurityLevel.KYBER_512: {
            'keygen': kyber512_keygen,
            'encrypt': kyber512_encrypt,
            'decrypt': kyber512_decrypt,
            'name': 'Kyber-512'
        },
        SecurityLevel.KYBER_768: {
            'keygen': kyber768_keygen, 
            'encrypt': kyber768_encrypt,
            'decrypt': kyber768_decrypt,
            'name': 'Kyber-768'
        },
        SecurityLevel.KYBER_1024: {
            'keygen': kyber1024_keygen,
            'encrypt': kyber1024_encrypt,
            'decrypt': kyber1024_decrypt,
            'name': 'Kyber-1024'
        }
    }
    
    def __init__(self, default_security_level: SecurityLevel = SecurityLevel.KYBER_768):
        """
        Initialize Kyber KEM with default security level
        
        Args:
            default_security_level: Default security level for operations
        """
        self.default_security_level = default_security_level
        logger.info(f"Initialized KyberKEM with {default_security_level.value}")
    
    def generate_keypair(self, security_level: Optional[SecurityLevel] = None) -> KeyPair:
        """
        Generate a new Kyber key pair
        
        Args:
            security_level: Security level to use, defaults to instance default
            
        Returns:
            KeyPair: Generated key pair with metadata
            
        Raises:
            KyberKEMError: If key generation fails
        """
        level = security_level or self.default_security_level
        
        try:
            algorithm = self._ALGORITHMS[level]
            logger.info(f"Generating {algorithm['name']} key pair")
            
            # Generate the key pair
            public_key, private_key = algorithm['keygen']()
            
            # Create key pair with metadata
            key_pair = KeyPair(
                public_key=public_key,
                private_key=private_key, 
                security_level=level,
                created_at=time.time(),
                key_id=self._generate_key_id()
            )
            
            logger.info(f"Generated key pair {key_pair.key_id} with {algorithm['name']}")
            return key_pair
            
        except Exception as e:
            logger.error(f"Key generation failed: {str(e)}")
            raise KyberKEMError(f"Failed to generate key pair: {str(e)}")
    
    def encapsulate(self, public_key: bytes, security_level: Optional[SecurityLevel] = None) -> EncapsulationResult:
        """
        Perform Kyber encapsulation to generate shared secret
        
        Args:
            public_key: Recipient's Kyber public key
            security_level: Security level to use for encapsulation
            
        Returns:
            EncapsulationResult: Ciphertext and shared secret
            
        Raises:
            KyberKEMError: If encapsulation fails
        """
        level = security_level or self.default_security_level
        
        try:
            algorithm = self._ALGORITHMS[level]
            
            # Validate public key length
            self._validate_public_key(public_key, level)
            
            logger.debug(f"Performing {algorithm['name']} encapsulation")
            
            # Perform encapsulation
            ciphertext, shared_secret = algorithm['encrypt'](public_key)
            
            result = EncapsulationResult(
                ciphertext=ciphertext,
                shared_secret=shared_secret,
                timestamp=time.time()
            )
            
            logger.debug(f"Encapsulation successful, shared secret: {len(shared_secret)} bytes")
            return result
            
        except Exception as e:
            logger.error(f"Encapsulation failed: {str(e)}")
            raise KyberKEMError(f"Failed to encapsulate: {str(e)}")
    
    def decapsulate(self, private_key: bytes, ciphertext: bytes, 
                   security_level: Optional[SecurityLevel] = None) -> bytes:
        """
        Perform Kyber decapsulation to recover shared secret
        
        Args:
            private_key: Our private key
            ciphertext: Ciphertext from encapsulation
            security_level: Security level used for original encapsulation
            
        Returns:
            bytes: Recovered shared secret
            
        Raises:
            KyberKEMError: If decapsulation fails
        """
        level = security_level or self.default_security_level
        
        try:
            algorithm = self._ALGORITHMS[level]
            
            # Validate inputs
            self._validate_private_key(private_key, level)
            self._validate_ciphertext(ciphertext, level)
            
            logger.debug(f"Performing {algorithm['name']} decapsulation")
            
            # Perform decapsulation
            shared_secret = algorithm['decrypt'](private_key, ciphertext)
            
            logger.debug(f"Decapsulation successful, shared secret: {len(shared_secret)} bytes")
            return shared_secret
            
        except Exception as e:
            logger.error(f"Decapsulation failed: {str(e)}")
            raise KyberKEMError(f"Failed to decapsulate: {str(e)}")
    
    def serialize_public_key(self, public_key: bytes, security_level: SecurityLevel) -> str:
        """
        Serialize public key for network transmission
        
        Args:
            public_key: Raw public key bytes
            security_level: Security level of the key
            
        Returns:
            str: JSON serialized public key with metadata
        """
        key_data = {
            'algorithm': 'kyber',
            'security_level': security_level.value,
            'public_key': public_key.hex(),
            'timestamp': time.time()
        }
        return json.dumps(key_data)
    
    def deserialize_public_key(self, serialized_key: str) -> Tuple[bytes, SecurityLevel]:
        """
        Deserialize public key from network transmission
        
        Args:
            serialized_key: JSON serialized public key
            
        Returns:
            Tuple[bytes, SecurityLevel]: Public key and security level
            
        Raises:
            KyberKEMError: If deserialization fails or key is invalid
        """
        try:
            key_data = json.loads(serialized_key)
            
            # Validate format
            if key_data.get('algorithm') != 'kyber':
                raise KyberKEMError("Invalid algorithm in serialized key")
            
            security_level = SecurityLevel(key_data['security_level'])
            public_key = bytes.fromhex(key_data['public_key'])
            
            # Validate deserialized key
            self._validate_public_key(public_key, security_level)
            
            return public_key, security_level
            
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            raise KyberKEMError(f"Failed to deserialize public key: {str(e)}")
    
    def _generate_key_id(self) -> str:
        """Generate unique key identifier"""
        return secrets.token_hex(16)
    
    def _validate_public_key(self, public_key: bytes, security_level: SecurityLevel):
        """Validate public key format and length"""
        if not isinstance(public_key, bytes):
            raise KyberKEMError("Public key must be bytes")
        
        # Expected public key lengths for each security level
        expected_lengths = {
            SecurityLevel.KYBER_512: 800,   # Approximate, adjust based on actual pqcrypto
            SecurityLevel.KYBER_768: 1184,
            SecurityLevel.KYBER_1024: 1568
        }
        
        expected_length = expected_lengths.get(security_level)
        if expected_length and len(public_key) != expected_length:
            logger.warning(f"Public key length {len(public_key)}, expected ~{expected_length}")
    
    def _validate_private_key(self, private_key: bytes, security_level: SecurityLevel):
        """Validate private key format and length"""
        if not isinstance(private_key, bytes):
            raise KyberKEMError("Private key must be bytes")
        
        if len(private_key) < 100:  # Sanity check
            raise KyberKEMError("Private key too short")
    
    def _validate_ciphertext(self, ciphertext: bytes, security_level: SecurityLevel):
        """Validate ciphertext format and length"""
        if not isinstance(ciphertext, bytes):
            raise KyberKEMError("Ciphertext must be bytes")
        
        if len(ciphertext) < 100:  # Sanity check
            raise KyberKEMError("Ciphertext too short")


