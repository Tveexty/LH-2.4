# [file name]: encryption_manager.py
import base64
import hashlib
import json

try:
    from cryptography.fernet import Fernet
except ImportError:
    Fernet = None


class EncryptionManager:
    def __init__(self):
        # Формируем строго валидный 32-байтовый URL-safe base64 ключ для Fernet (44 символа base64)
        raw_seed = b"launcher_hab_encryption_key_2024_secure_v2_4"
        self.default_key = base64.urlsafe_b64encode(hashlib.sha256(raw_seed).digest())
        self._cipher = Fernet(self.default_key) if Fernet is not None else None

    def generate_key_from_password(self, password: str) -> bytes:
        """Генерация валидного 32-байтового ключа Fernet из пароля."""
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            b"launcher_hab_salt_2024",
            100000,
            dklen=32,
        )
        return base64.urlsafe_b64encode(digest)

    def encrypt_data(self, data) -> str:
        """Шифрование данных с защитой от потери настроек."""
        try:
            json_data = json.dumps(data, ensure_ascii=False)
            if self._cipher is not None:
                encrypted_data = self._cipher.encrypt(json_data.encode("utf-8"))
                return base64.urlsafe_b64encode(encrypted_data).decode("utf-8")
            return base64.urlsafe_b64encode(json_data.encode("utf-8")).decode("utf-8")
        except Exception as e:
            print(f"Ошибка шифрования: {e}")
            return ""

    def decrypt_data(self, encrypted_data: str):
        """Дешифрование данных."""
        try:
            if not encrypted_data:
                return None
            decoded_data = base64.urlsafe_b64decode(encrypted_data.encode("utf-8"))
            if self._cipher is not None:
                decrypted_data = self._cipher.decrypt(decoded_data)
                return json.loads(decrypted_data.decode("utf-8"))
            return json.loads(decoded_data.decode("utf-8"))
        except Exception as e:
            print(f"Ошибка дешифрования: {e}")
            return None

    def encrypt_settings(self, settings_dict: dict) -> dict:
        """Шифрование настроек. Если шифрование недоступно — сохраняет открытый словарь (без потери данных)."""
        if not isinstance(settings_dict, dict):
            return {}
        encrypted = self.encrypt_data(settings_dict)
        if encrypted:
            return {"encrypted": True, "version": "2.4", "data": encrypted}
        return settings_dict

    def decrypt_settings(self, encrypted_settings: dict) -> dict:
        """Дешифрование настроек с поддержкой как зашифрованного, так и обычного JSON."""
        if not isinstance(encrypted_settings, dict):
            return {}
        if "encrypted" in encrypted_settings and encrypted_settings.get("data"):
            decrypted = self.decrypt_data(encrypted_settings["data"])
            return decrypted if isinstance(decrypted, dict) else {}
        return encrypted_settings