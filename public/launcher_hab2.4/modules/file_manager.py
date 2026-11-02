import json
import os
from .encryption_manager import EncryptionManager
from .logger import get_logger

logger = get_logger(__name__)

class FileManager:
    DATA_FILES = {
        'settings': 'launcher_settings.json',
        'favorites': 'favorites.json', 
        'manual_paths': 'manual_paths.json',
        'custom_apps': 'custom_apps.json',
        'custom_themes': 'custom_themes.json'
    }
    
    def __init__(self):
        self.encryption_manager = EncryptionManager()
    
    def load_data(self, filename, default=None):
        """Загрузка данных с поддержкой дешифрования"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Дешифруем если это зашифрованные настройки
                if filename == self.DATA_FILES['settings'] and isinstance(data, dict) and 'encrypted' in data:
                    data = self.encryption_manager.decrypt_settings(data)
                
                return data
        except Exception:
            logger.exception("Ошибка загрузки %s", filename)
        return default if default is not None else {}
    
    def save_data(self, filename, data):
        """Сохранение данных с поддержкой шифрования"""
        try:
            # Шифруем настройки
            if filename == self.DATA_FILES['settings']:
                data = self.encryption_manager.encrypt_settings(data)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            logger.exception("Ошибка сохранения %s", filename)
            return False
    
    def load_settings(self):
        """Загрузка настроек с дешифрованием"""
        settings = self.load_data(self.DATA_FILES['settings'])
        if not settings:
            settings = {
                "theme": "dark", 
                "glass_effect": True, 
                "glass_intensity": "medium"
            }
        return settings
    
    def save_settings(self, settings_data):
        """Сохранение настроек с шифрованием"""
        return self.save_data(self.DATA_FILES['settings'], settings_data)