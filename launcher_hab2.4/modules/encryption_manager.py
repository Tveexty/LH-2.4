import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import json

class EncryptionManager:
    def __init__(self):
        # Ключ шифрования по умолчанию
        self.default_key = b'launcher_hab_encryption_key_2024_secure_'
    
    def generate_key_from_password(self, password: str, salt: bytes = None) -> tuple:
        """Генерация ключа из пароля"""
        try:
            if salt is None:
                salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            return key, salt
        except Exception as e:
            print(f"Ошибка генерации ключа: {e}")
            return None, None
    
    def encrypt_data(self, data: str, key: bytes = None) -> dict:
        """Шифрование данных"""
        try:
            if key is None:
                key = self.default_key
            fernet = Fernet(key)
            encrypted_data = fernet.encrypt(data.encode())
            return {
                'encrypted': base64.urlsafe_b64encode(encrypted_data).decode(),
                'timestamp': self._get_timestamp()
            }
        except Exception as e:
            print(f"Ошибка шифрования: {e}")
            return None
    
    def decrypt_data(self, encrypted_data: dict, key: bytes = None) -> str:
        """Дешифрование данных"""
        try:
            if key is None:
                key = self.default_key
            fernet = Fernet(key)
            decrypted_data = fernet.decrypt(base64.urlsafe_b64decode(encrypted_data['encrypted']))
            return decrypted_data.decode()
        except Exception as e:
            print(f"Ошибка дешифрования: {e}")
            return None
    
    def _get_timestamp(self):
        """Получить текущую временную метку"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def encrypt_settings(self, settings_data):
        """Шифрование настроек"""
        if isinstance(settings_data, dict):
            return self.encrypt_data(json.dumps(settings_data))
        return settings_data
    
    def decrypt_settings(self, encrypted_settings):
        """Дешифрование настроек"""
        if isinstance(encrypted_settings, dict) and 'encrypted' in encrypted_settings:
            decrypted = self.decrypt_data(encrypted_settings)
            if decrypted:
                return json.loads(decrypted)
        return encrypted_settings