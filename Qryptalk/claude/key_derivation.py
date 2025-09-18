# File: src/crypto/key_derivation.py

class KeyDerivationFunction:
    """
    Key derivation functions for QrypTalk
    
    Derives message encryption keys from Kyber shared secrets using HKDF.
    Follows secure patterns for key material handling.
    """
    
    # Standard key lengths
    MESSAGE_KEY_LENGTH = 32     # AES-256 key
    MAC_KEY_LENGTH = 32         # HMAC-SHA256 key  
    IV_LENGTH = 12              # AES-GCM IV
    ROOT_KEY_LENGTH = 32        # Root key for key chaining
    
    def __init__(self):
        self.algorithm = hashes.SHA256()
    
    def derive_message_keys(self, shared_secret: bytes, context: str = "qryptalk-message") -> Dict[str, bytes]:
        """
        Derive message encryption keys from Kyber shared secret
        
        Args:
            shared_secret: Shared secret from Kyber KEM
            context: Context string for key derivation
            
        Returns:
            Dict containing message_key, mac_key, and iv
        """
        if len(shared_secret) != 32:  # Kyber shared secrets are 32 bytes
            raise ValueError("Invalid shared secret length")
        
        # Derive root key first
        root_key = self._derive_key(
            shared_secret, 
            salt=b"qryptalk-root",
            info=context.encode(),
            length=self.ROOT_KEY_LENGTH
        )
        
        # Derive individual keys from root key
        message_key = self._derive_key(
            root_key,
            salt=b"qryptalk-msg", 
            info=b"message-encryption",
            length=self.MESSAGE_KEY_LENGTH
        )
        
        mac_key = self._derive_key(
            root_key,
            salt=b"qryptalk-mac",
            info=b"message-authentication", 
            length=self.MAC_KEY_LENGTH
        )
        
        # Generate IV from root key (deterministic but unique per conversation)
        iv = self._derive_key(
            root_key,
            salt=b"qryptalk-iv",
            info=context.encode(),
            length=self.IV_LENGTH
        )
        
        return {
            'message_key': message_key,
            'mac_key': mac_key, 
            'iv': iv,
            'root_key': root_key
        }
    
    def derive_next_generation_key(self, current_root_key: bytes, generation: int) -> bytes:
        """
        Derive next generation root key for key rotation
        
        Args:
            current_root_key: Current root key
            generation: Key generation number
            
        Returns:
            bytes: Next generation root key
        """
        return self._derive_key(
            current_root_key,
            salt=f"qryptalk-gen-{generation}".encode(),
            info=b"key-rotation",
            length=self.ROOT_KEY_LENGTH
        )
    
    def _derive_key(self, key_material: bytes, salt: bytes, info: bytes, length: int) -> bytes:
        """
        Internal key derivation using HKDF
        
        Args:
            key_material: Input key material
            salt: Salt for HKDF
            info: Context info for HKDF
            length: Desired output length
            
        Returns:
            bytes: Derived key
        """
        hkdf = HKDF(
            algorithm=self.algorithm,
            length=length,
            salt=salt,
            info=info
        )
        return hkdf.derive(key_material)


