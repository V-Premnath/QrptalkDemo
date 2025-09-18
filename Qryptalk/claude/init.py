# File: src/crypto/__init__.py

"""
QrypTalk Cryptographic Module

Provides post-quantum secure cryptographic operations:
- CRYSTALS-Kyber KEM for key exchange
- HKDF for key derivation  
- AES-GCM for message encryption
"""

from .kyber_kem import KyberKEM, SecurityLevel, KeyPair, EncapsulationResult, KyberKEMError
from .key_derivation import KeyDerivationFunction
from .message_crypto import MessageCrypto

__all__ = [
    'KyberKEM',
    'SecurityLevel', 
    'KeyPair',
    'EncapsulationResult',
    'KyberKEMError',
    'KeyDerivationFunction',
    'MessageCrypto'
]

# Version info
__version__ = "0.1.0"
__author__ = "QrypTalk Development Team"


if __name__ == "__main__":
    # Basic functionality test
    print("QrypTalk Cryptographic Foundation Test")
    print("=" * 50)
    
    # Test KyberKEM
    kem = KyberKEM(SecurityLevel.KYBER_768)
    
    # Generate key pairs for Alice and Bob
    alice_keys = kem.generate_keypair()
    bob_keys = kem.generate_keypair()
    
    print(f"Alice key pair: {alice_keys.key_id}")
    print(f"Bob key pair: {bob_keys.key_id}")
    
    # Alice encapsulates to Bob
    encaps_result = kem.encapsulate(bob_keys.public_key)
    print(f"Encapsulation: {len(encaps_result.ciphertext)} byte ciphertext")
    
    # Bob decapsulates
    bob_shared_secret = kem.decapsulate(bob_keys.private_key, encaps_result.ciphertext)
    
    print(f"Shared secrets match: {bob_shared_secret == encaps_result.shared_secret}")
    
    # Test key derivation
    kdf = KeyDerivationFunction()
    alice_keys_derived = kdf.derive_message_keys(encaps_result.shared_secret, "test-conversation")
    bob_keys_derived = kdf.derive_message_keys(bob_shared_secret, "test-conversation")
    
    print(f"Derived keys match: {alice_keys_derived == bob_keys_derived}")
    
    # Test message encryption
    crypto = MessageCrypto()
    test_message = "Hello Bob, this is a post-quantum secure message!"
    
    encrypted = crypto.encrypt_message(alice_keys_derived['message_key'], test_message)
    print(f"Encrypted message: {len(encrypted['ciphertext'])} characters")
    
    decrypted = crypto.decrypt_message(bob_keys_derived['message_key'], encrypted)
    print(f"Decrypted message: {decrypted}")
    print(f"Message integrity: {decrypted == test_message}")
    
    print("\n✅ All cryptographic operations successful!")
    print("🔐 QrypTalk crypto foundation is ready for Phase 2!")