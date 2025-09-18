# File: src/crypto/message_crypto.py

class MessageCrypto:
    """
    Message encryption and decryption for QrypTalk
    
    Provides authenticated encryption using AES-GCM.
    Handles message serialization and integrity protection.
    """
    
    def __init__(self):
        self.kdf = KeyDerivationFunction()
    
    def encrypt_message(self, message_key: bytes, plaintext: str, associated_data: Optional[bytes] = None) -> Dict[str, Any]:
        """
        Encrypt a message using AES-GCM
        
        Args:
            message_key: 32-byte AES key
            plaintext: Message to encrypt
            associated_data: Additional authenticated data (optional)
            
        Returns:
            Dict containing ciphertext, nonce, and metadata
        """
        if len(message_key) != 32:
            raise ValueError("Message key must be 32 bytes")
        
        try:
            # Convert message to bytes
            message_bytes = plaintext.encode('utf-8')
            
            # Generate random nonce for this message
            nonce = os.urandom(12)  # 96-bit nonce for AES-GCM
            
            # Create AESGCM cipher
            aesgcm = AESGCM(message_key)
            
            # Encrypt with authentication
            ciphertext = aesgcm.encrypt(nonce, message_bytes, associated_data)
            
            return {
                'ciphertext': ciphertext.hex(),
                'nonce': nonce.hex(),
                'algorithm': 'aes-256-gcm',
                'timestamp': time.time(),
                'length': len(message_bytes)
            }
            
        except Exception as e:
            logger.error(f"Message encryption failed: {str(e)}")
            raise KyberKEMError(f"Failed to encrypt message: {str(e)}")
    
    def decrypt_message(self, message_key: bytes, encrypted_data: Dict[str, Any], 
                       associated_data: Optional[bytes] = None) -> str:
        """
        Decrypt a message using AES-GCM
        
        Args:
            message_key: 32-byte AES key
            encrypted_data: Dict containing ciphertext and nonce
            associated_data: Additional authenticated data (optional)
            
        Returns:
            str: Decrypted message
            
        Raises:
            KyberKEMError: If decryption fails or authentication fails
        """
        if len(message_key) != 32:
            raise ValueError("Message key must be 32 bytes")
        
        try:
            # Extract components
            ciphertext = bytes.fromhex(encrypted_data['ciphertext'])
            nonce = bytes.fromhex(encrypted_data['nonce'])
            
            # Validate algorithm
            if encrypted_data.get('algorithm') != 'aes-256-gcm':
                raise KyberKEMError("Unsupported encryption algorithm")
            
            # Create AESGCM cipher
            aesgcm = AESGCM(message_key)
            
            # Decrypt and authenticate
            message_bytes = aesgcm.decrypt(nonce, ciphertext, associated_data)
            
            # Convert back to string
            return message_bytes.decode('utf-8')
            
        except InvalidSignature:
            logger.error("Message authentication failed")
            raise KyberKEMError("Message authentication failed - possible tampering")
        except Exception as e:
            logger.error(f"Message decryption failed: {str(e)}")
            raise KyberKEMError(f"Failed to decrypt message: {str(e)}")


