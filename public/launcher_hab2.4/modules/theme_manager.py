# [file name]: theme_manager.py
import flet as ft
import json
import os
from .file_manager import FileManager
from .logger import get_logger

logger = get_logger(__name__)


class ThemeManager:
    CLOCK_STYLES = {
        "standard": "Классический (14:32:08)",
        "stacked": "Вертикальный Stacked (14 / 32)",
        "minimal": "Минималистичный (14:32)",
        "pill_glass": "Стеклянная капсула (14:32 • Дата)",
        "cyber_mono": "Цифровой моно ([ 14 : 32 : 08 ])",
        "compact_badge": "Компактный с днем недели",
    }

    BASE_THEMES = {
        "dark": {
            "NAME": "Темная",
            "BG": "#16181d",
            "SURFACE": "#222630",
            "SURFACE_VARIANT": "#2f3542",
            "ON_SURFACE": "#f8fafc",
            "ON_SURFACE_VARIANT": "#94a3b8",
            "OUTLINE": "#3b4252",
            "ACCENT": "#4285f4",
            "ACCENT_GLOW": "#4285f440",
            "ERROR": "#ff6b6b",
            "SUCCESS": "#4caf50",
            "WEB_BLUE": "#60a5fa",
            "GLASS_BG": "#22263066",
            "GLASS_BORDER": "#ffffff24",
            "GLASS_SHADOW": "#00000045",
            "GLASS_BG_LIGHT": "#22263038",
            "SETTINGS_BG": "#16181d",
            "SETTINGS_SURFACE": "#222630",
            "SETTINGS_CARD": "#2b303c",
        },
        "light": {
            "NAME": "Светлая",
            "BG": "#f1f5f9",
            "SURFACE": "#ffffff",
            "SURFACE_VARIANT": "#e2e8f0",
            "ON_SURFACE": "#0f172a",
            "ON_SURFACE_VARIANT": "#64748b",
            "OUTLINE": "#cbd5e1",
            "ACCENT": "#3b82f6",
            "ACCENT_GLOW": "#3b82f620",
            "ERROR": "#dc2626",
            "SUCCESS": "#059669",
            "WEB_BLUE": "#2563eb",
            "GLASS_BG": "#ffffff85",
            "GLASS_BORDER": "#0f172a14",
            "GLASS_SHADOW": "#0f172a12",
            "GLASS_BG_LIGHT": "#ffffff55",
            "SETTINGS_BG": "#f8fafc",
            "SETTINGS_SURFACE": "#ffffff",
            "SETTINGS_CARD": "#f1f5f9",
        },
        "purple": {
            "NAME": "Фиолетовая",
            "BG": "#151426",
            "SURFACE": "#252342",
            "SURFACE_VARIANT": "#35325c",
            "ON_SURFACE": "#ffffff",
            "ON_SURFACE_VARIANT": "#c4b5fd",
            "OUTLINE": "#4c4682",
            "ACCENT": "#a855f7",
            "ACCENT_GLOW": "#a855f735",
            "ERROR": "#ff6b6b",
            "SUCCESS": "#34d399",
            "WEB_BLUE": "#c084fc",
            "GLASS_BG": "#25234270",
            "GLASS_BORDER": "#ffffff22",
            "GLASS_SHADOW": "#00000045",
            "GLASS_BG_LIGHT": "#25234240",
            "SETTINGS_BG": "#151426",
            "SETTINGS_SURFACE": "#252342",
            "SETTINGS_CARD": "#35325c",
        },
        "spring": {
            "NAME": "Весна",
            "BG": "#fff5f7",
            "SURFACE": "#fce7f3",
            "SURFACE_VARIANT": "#fbcfe8",
            "ON_SURFACE": "#4a148c",
            "ON_SURFACE_VARIANT": "#880e4f",
            "OUTLINE": "#f472b6",
            "ACCENT": "#e91e63",
            "ACCENT_GLOW": "#e91e6320",
            "ERROR": "#f44336",
            "SUCCESS": "#10b981",
            "WEB_BLUE": "#db2777",
            "GLASS_BG": "#fce7f380",
            "GLASS_BORDER": "#880e4f15",
            "GLASS_SHADOW": "#00000018",
            "GLASS_BG_LIGHT": "#fce7f345",
            "SETTINGS_BG": "#fff5f7",
            "SETTINGS_SURFACE": "#fce7f3",
            "SETTINGS_CARD": "#fbcfe8",
        },
    }

    def __init__(self):
        self.file_manager = FileManager()
        self.custom_themes = self.load_custom_themes()
        self.smooth_animations = True
        self.android_animations = True
        self.load_settings()

    def load_settings(self):
        settings = self.file_manager.load_settings()
        if settings is None:
            settings = {}

        self.current_theme = settings.get("theme", "dark")
        self.glass_effect_enabled = settings.get("glass_effect", True)
        self.glass_intensity = settings.get("glass_intensity", "medium")
        self.advanced_glass_enabled = settings.get("advanced_glass_enabled", True)
        self.advanced_glass_opacity = settings.get("advanced_glass_opacity", 35)
        self.desktop_mode_enabled = settings.get("desktop_mode_enabled", True)
        self.smooth_animations = settings.get("smooth_animations", True)
        self.android_animations = settings.get("android_animations", True)

        # Настройки времени, часов и шрифтов (v2.2 - v2.4)
        self.time_format = settings.get("time_format", "24")
        self.date_format = settings.get("date_format", "dd.mm.yyyy")
        self.font_family = settings.get("font_family", "Segoe UI")
        self.font_size = settings.get("font_size", 14)
        self.time_font_size = settings.get("time_font_size", 20)
        self.date_font_size = settings.get("date_font_size", 12)
        self.time_font_family = settings.get("time_font_family", self.font_family)
        self.date_font_family = settings.get("date_font_family", self.font_family)
        self.backup_auto = settings.get("backup_auto", True)
        self.backup_interval = settings.get("backup_interval", 7)
        self.search_cache_enabled = settings.get("search_cache_enabled", True)
        self.virtualization_enabled = settings.get("virtualization_enabled", True)

        # Расширенные настройки стилей часов v2.4
        self.clock_style = settings.get("clock_style", "standard")
        self.show_date = settings.get("show_date", True)
        self.show_seconds = settings.get("show_seconds", True)
        self.show_weekday = settings.get("show_weekday", True)
        self.clock_glass_frame = settings.get("clock_glass_frame", True)
        self.time_color = settings.get(
            "time_color", self.get_theme(self.current_theme).get("ON_SURFACE", "#ffffff")
        )
        self.date_color = settings.get(
            "date_color", self.get_theme(self.current_theme).get("ON_SURFACE_VARIANT", "#94a3b8")
        )
        self.search_history_enabled = settings.get("search_history_enabled", True)

    def save_settings(self):
        settings_data = {
            "theme": self.current_theme,
            "glass_effect": self.glass_effect_enabled,
            "glass_intensity": self.glass_intensity,
            "advanced_glass_enabled": self.advanced_glass_enabled,
            "advanced_glass_opacity": self.advanced_glass_opacity,
            "desktop_mode_enabled": self.desktop_mode_enabled,
            "smooth_animations": self.smooth_animations,
            "android_animations": self.android_animations,
            "time_format": self.time_format,
            "date_format": self.date_format,
            "font_family": self.font_family,
            "font_size": self.font_size,
            "time_font_size": self.time_font_size,
            "date_font_size": self.date_font_size,
            "time_font_family": self.time_font_family,
            "date_font_family": self.date_font_family,
            "backup_auto": self.backup_auto,
            "backup_interval": self.backup_interval,
            "search_cache_enabled": self.search_cache_enabled,
            "virtualization_enabled": self.virtualization_enabled,
            "clock_style": self.clock_style,
            "show_date": self.show_date,
            "show_seconds": self.show_seconds,
            "show_weekday": self.show_weekday,
            "clock_glass_frame": self.clock_glass_frame,
            "time_color": self.time_color,
            "date_color": self.date_color,
            "search_history_enabled": self.search_history_enabled,
        }
        return self.file_manager.save_settings(settings_data)

    def load_custom_themes(self):
        themes = self.file_manager.load_data("custom_themes.json", {})
        return themes if themes is not None else {}

    def save_custom_themes(self):
        self.file_manager.save_data("custom_themes.json", self.custom_themes)

    def get_theme(self, theme_name=None):
        theme_name = theme_name or self.current_theme
        all_themes = {**self.BASE_THEMES, **self.custom_themes}
        return all_themes.get(theme_name, self.BASE_THEMES["dark"])

    def get_current_theme(self):
        return self.get_theme(self.current_theme)

    def apply_theme(self, page, theme_name):
        if theme_name not in self.BASE_THEMES and theme_name not in self.custom_themes:
            theme_name = "dark"

        self.current_theme = theme_name
        theme = self.get_theme(theme_name)

        if page:
            page.bgcolor = theme["BG"]
            if theme_name in ["light", "spring"]:
                page.theme_mode = ft.ThemeMode.LIGHT
            else:
                page.theme_mode = ft.ThemeMode.DARK

            try:
                page.theme = ft.Theme(
                    font_family=self.font_family,
                    page_transitions=ft.PageTransitionsTheme(
                        windows=ft.PageTransitionTheme.CUPERTINO,
                        linux=ft.PageTransitionTheme.CUPERTINO,
                        macos=ft.PageTransitionTheme.CUPERTINO,
                    )
                    if self.smooth_animations
                    else None,
                )
            except Exception:
                logger.exception("Не удалось применить тему")

        self.save_settings()
        return theme

    def toggle_glass_effect(self):
        self.glass_effect_enabled = not self.glass_effect_enabled
        self.save_settings()
        return self.glass_effect_enabled

    def set_glass_intensity(self, intensity):
        if intensity in ["light", "medium", "strong"]:
            self.glass_intensity = intensity
            self.save_settings()

    def set_advanced_glass(self, enabled: bool, opacity: int = None):
        self.advanced_glass_enabled = bool(enabled)
        if opacity is not None:
            self.advanced_glass_opacity = max(15, min(95, int(opacity)))
        self.save_settings()

    def set_desktop_mode(self, enabled: bool):
        self.desktop_mode_enabled = bool(enabled)
        self.save_settings()

    def toggle_smooth_animations(self):
        self.smooth_animations = not self.smooth_animations
        self.save_settings()
        return self.smooth_animations

    def toggle_android_animations(self):
        self.android_animations = not self.android_animations
        self.save_settings()
        return self.android_animations

    def get_available_themes(self):
        return {**self.BASE_THEMES, **self.custom_themes}

    def add_custom_theme(self, name, theme_data):
        if name and theme_data:
            self.custom_themes[name] = theme_data
            self.save_custom_themes()
            return True
        return False

    def set_time_format(self, format_type):
        if format_type in ["12", "24"]:
            self.time_format = format_type
            self.save_settings()

    def set_date_format(self, date_format):
        if date_format in ["dd.mm.yyyy", "mm/dd/yyyy", "yyyy-mm-dd"]:
            self.date_format = date_format
            self.save_settings()

    def set_font_family(self, font_family):
        self.font_family = font_family
        self.save_settings()

    def set_font_size(self, font_size):
        self.font_size = font_size
        self.save_settings()

    def set_time_style(self, time_size=None, date_size=None, time_family=None, date_family=None):
        if time_size is not None:
            self.time_font_size = int(time_size)
        if date_size is not None:
            self.date_font_size = int(date_size)
        if time_family:
            self.time_font_family = time_family
        if date_family:
            self.date_font_family = date_family
        self.save_settings()

    def set_backup_settings(self, auto_backup, interval):
        self.backup_auto = auto_backup
        self.backup_interval = interval
        self.save_settings()

    def set_performance_settings(self, search_cache, virtualization):
        self.search_cache_enabled = search_cache
        self.virtualization_enabled = virtualization
        self.save_settings()

    def set_clock_preferences(
        self,
        style=None,
        show_date=None,
        time_color=None,
        date_color=None,
        show_seconds=None,
        show_weekday=None,
        clock_glass_frame=None,
        time_font_size=None,
    ):
        if style in self.CLOCK_STYLES:
            self.clock_style = style
        if show_date is not None:
            self.show_date = bool(show_date)
        if show_seconds is not None:
            self.show_seconds = bool(show_seconds)
        if show_weekday is not None:
            self.show_weekday = bool(show_weekday)
        if clock_glass_frame is not None:
            self.clock_glass_frame = bool(clock_glass_frame)
        if time_font_size is not None:
            self.time_font_size = max(14, min(44, int(time_font_size)))
        if isinstance(time_color, str) and time_color.startswith("#"):
            self.time_color = time_color
        if isinstance(date_color, str) and date_color.startswith("#"):
            self.date_color = date_color
        self.save_settings()