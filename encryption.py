"""
Encryption Module
Manages encryption and decryption with shared key support
"""

from cryptography.fernet import Fernet


class EncryptionManager:
    """
    Manages encryption/decryption with optional shared key
    If shared_key provided, uses that (for syncing between windows)
    Otherwise generates new key
    """
    def __init__(self, shared_key=None):
        """Initialize encryption"""
        if shared_key:
            # Use shared key from file (same for all windows)
            self.key = shared_key.encode() if isinstance(shared_key, str) else shared_key
            self.cipher = Fernet(self.key)
            print(f"✓ Using shared encryption key")
        else:
            # Generate new key (for single window)
            self.key = Fernet.generate_key()
            self.cipher = Fernet(self.key)
            print(f"✓ Generated new encryption key")
    
    def encrypt_message(self, message):
        """Encrypt message"""
        try:
            message_bytes = message.encode('utf-8')
            encrypted = self.cipher.encrypt(message_bytes)
            return encrypted.decode('utf-8')
        except Exception as e:
            print(f"Encryption error: {e}")
            return None
    
    def decrypt_message(self, encrypted_message):
        """Decrypt message"""
        try:
            encrypted_bytes = encrypted_message.encode('utf-8')
            decrypted = self.cipher.decrypt(encrypted_bytes)
            return decrypted.decode('utf-8')
        except Exception as e:
            print(f"Decryption error: {e}")
            return None
