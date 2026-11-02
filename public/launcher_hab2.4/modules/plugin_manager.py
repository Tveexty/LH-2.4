# [file name]: plugin_manager.py
import flet as ft
import importlib.util
import os
import shutil
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .logger import get_logger

logger = get_logger(__name__)


class PluginAPI:
    """
    Расширенный SDK / API для плагинов и расширений Launcher Hab 2.4.
    Позволяет плагинам безопасно взаимодействовать с ядром лаунчера:
    - подписываться на события запуска/закрытия приложений (on_app_launched, on_tick);
    - добавлять бейджи на карточки приложений (get_app_card_badge);
    - хранить собственные настройки в JSON;
    - отправлять системные уведомления.
    """

    def __init__(self, plugin_manager, core=None):
        self.plugin_manager = plugin_manager
        self.core = core
        self._event_listeners: Dict[str, List[Callable]] = {}

    def on(self, event_name: str, callback: Callable):
        """Подписка на системное событие ('app_launched', 'theme_changed', 'tick')."""
        self._event_listeners.setdefault(event_name, []).append(callback)

    def emit(self, event_name: str, *args, **kwargs):
        """Вызов обработчиков события."""
        for cb in self._event_listeners.get(event_name, []):
            try:
                cb(*args, **kwargs)
            except Exception:
                logger.exception("Ошибка в обработчике события плагина: %s", event_name)

    def notify(self, title: str, message: str):
        """Показать уведомление в лаунчере."""
        if self.core and hasattr(self.core, "show_system_notification"):
            self.core.show_system_notification(title, message)

    def get_config(self, plugin_name: str, default: Optional[Dict] = None) -> Dict:
        return self.plugin_manager.get_plugin_config(plugin_name, default or {})

    def save_config(self, plugin_name: str, config: Dict) -> bool:
        return self.plugin_manager.save_plugin_config(plugin_name, config)

    def get_all_apps(self) -> List[Dict]:
        if self.core and hasattr(self.core, "app_manager"):
            return self.core.app_manager.get_all_apps()
        return []


class PluginManager:
    """Улучшенный менеджер плагинов и расширений (Launcher Hab 2.4)."""

    # Плагины, включенные по умолчанию при первом запуске 2.4
    DEFAULT_ENABLED_PLUGINS = {
        "session_tracker_plugin",
        "focus_mode_plugin",
        "smart_weather_plugin",
        "smart_music_controller",
    }

    def __init__(self, file_manager):
        self.file_manager = file_manager
        self.plugins_dir = Path("plugins")
        self.plugins_file = "plugins.json"
        self.plugin_configs_file = "plugin_configs.json"
        self.loaded_plugins: Dict[str, Any] = {}
        self.context = None
        self.api = PluginAPI(self)

        self.plugins_dir.mkdir(exist_ok=True)
        self.available_plugins = self.load_plugins_list()
        self.plugin_configs = self.file_manager.load_data(self.plugin_configs_file, {}) or {}
        self.refresh_plugins(load_enabled=True)

    def load_plugins_list(self) -> Dict[str, Dict[str, Any]]:
        data = self.file_manager.load_data(self.plugins_file, {})
        return data if isinstance(data, dict) else {}

    def save_plugins_list(self) -> bool:
        return self.file_manager.save_data(self.plugins_file, self.available_plugins)

    def get_plugin_config(self, plugin_name: str, default: Optional[Dict] = None) -> Dict:
        return self.plugin_configs.get(plugin_name, default if default is not None else {})

    def save_plugin_config(self, plugin_name: str, config: Dict) -> bool:
        self.plugin_configs[plugin_name] = config
        return self.file_manager.save_data(self.plugin_configs_file, self.plugin_configs)

    def discover_plugins(self) -> Dict[str, Dict[str, Any]]:
        """Обнаружить все плагины в директории plugins/ и считать их метаданные."""
        plugins: Dict[str, Dict[str, Any]] = {}
        for file_path in sorted(self.plugins_dir.glob("*.py")):
            if file_path.name.startswith("_"):
                continue

            plugin_name = file_path.stem
            saved_info = self.available_plugins.get(plugin_name, {})
            default_enabled = plugin_name in self.DEFAULT_ENABLED_PLUGINS
            plugins[plugin_name] = {
                "name": plugin_name,
                "display_name": saved_info.get("display_name", plugin_name.replace("_", " ").title()),
                "version": saved_info.get("version", "2.4"),
                "description": saved_info.get("description", "Расширение функциональности Launcher Hab"),
                "enabled": saved_info.get("enabled", default_enabled),
                "path": str(file_path.resolve()),
            }
        return plugins

    def load_plugin(self, plugin_name: str) -> bool:
        """Загрузить плагин и передать ему контекст и PluginAPI v2.4."""
        if plugin_name in self.loaded_plugins:
            return True

        plugin_info = self.available_plugins.get(plugin_name)
        if not plugin_info or not plugin_info.get("enabled", False):
            return False

        plugin_path = plugin_info.get("path")
        if not plugin_path or not os.path.exists(plugin_path):
            logger.warning("Файл плагина %s не найден: %s", plugin_name, plugin_path)
            return False

        module_name = f"launcher_plugin_{plugin_name}"
        try:
            spec = importlib.util.spec_from_file_location(module_name, plugin_path)
            if spec is None or spec.loader is None:
                logger.error("Не удалось создать spec для плагина %s", plugin_name)
                return False

            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            if not hasattr(module, "initialize_plugin"):
                logger.error("Плагин %s не содержит initialize_plugin()", plugin_name)
                return False

            plugin_instance = module.initialize_plugin()

            # Считываем метаданные из PLUGIN_META если они есть
            meta = getattr(plugin_instance, "PLUGIN_META", getattr(module, "PLUGIN_META", None))
            if isinstance(meta, dict):
                plugin_info["display_name"] = meta.get("name", plugin_info.get("display_name", plugin_name))
                plugin_info["version"] = meta.get("version", "2.4.0")
                plugin_info["description"] = meta.get("description", plugin_info.get("description", ""))
                plugin_info["icon"] = meta.get("icon", "extension")

            if self.context and hasattr(plugin_instance, "set_context"):
                plugin_instance.set_context(self.context)
            if hasattr(plugin_instance, "on_load"):
                plugin_instance.on_load(self.api)

            self.loaded_plugins[plugin_name] = {
                "instance": plugin_instance,
                "module_name": module_name,
            }
            logger.info("Плагин загружен: %s", plugin_name)
            return True
        except Exception:
            logger.exception("Ошибка загрузки плагина %s", plugin_name)
            return False

    def unload_plugin(self, plugin_name: str) -> bool:
        plugin_data = self.loaded_plugins.get(plugin_name)
        if not plugin_data:
            return False

        try:
            plugin_instance = plugin_data.get("instance")
            if hasattr(plugin_instance, "cleanup"):
                plugin_instance.cleanup()

            module_name = plugin_data.get("module_name")
            if module_name and module_name in sys.modules:
                del sys.modules[module_name]

            del self.loaded_plugins[plugin_name]
            logger.info("Плагин выгружен: %s", plugin_name)
            return True
        except Exception:
            logger.exception("Ошибка выгрузки плагина %s", plugin_name)
            return False

    def enable_plugin(self, plugin_name: str) -> bool:
        if plugin_name not in self.available_plugins:
            return False

        self.available_plugins[plugin_name]["enabled"] = True
        self.save_plugins_list()
        return self.load_plugin(plugin_name)

    def disable_plugin(self, plugin_name: str) -> bool:
        if plugin_name not in self.available_plugins:
            return False

        self.available_plugins[plugin_name]["enabled"] = False
        self.save_plugins_list()
        self.unload_plugin(plugin_name)
        return True

    def refresh_plugins(self, load_enabled: bool = False):
        discovered = self.discover_plugins()

        removed_plugins = set(self.available_plugins.keys()) - set(discovered.keys())
        for plugin_name in removed_plugins:
            self.unload_plugin(plugin_name)

        self.available_plugins = discovered
        if load_enabled:
            for plugin_name, plugin_info in self.available_plugins.items():
                if plugin_info.get("enabled", False):
                    self.load_plugin(plugin_name)
        self.save_plugins_list()

    def set_context(self, context):
        self.context = context
        self.api.core = context
        for plugin_data in self.loaded_plugins.values():
            plugin_instance = plugin_data.get("instance")
            if plugin_instance and hasattr(plugin_instance, "set_context"):
                plugin_instance.set_context(context)
            if plugin_instance and hasattr(plugin_instance, "on_load"):
                plugin_instance.on_load(self.api)

    # --- Новые хуки расширений 2.4 ---
    def notify_app_launched(self, app: Dict[str, Any]):
        """Уведомляет все активные плагины о запуске приложения."""
        self.api.emit("app_launched", app)
        for plugin_data in self.loaded_plugins.values():
            instance = plugin_data.get("instance")
            if instance and hasattr(instance, "on_app_launched"):
                try:
                    instance.on_app_launched(app)
                except Exception:
                    logger.exception("Ошибка on_app_launched в плагине")

    def notify_tick(self):
        """Периодический фоновый тик для плагинов (трекер времени и др.)."""
        self.api.emit("tick")
        for plugin_data in self.loaded_plugins.values():
            instance = plugin_data.get("instance")
            if instance and hasattr(instance, "on_tick"):
                try:
                    instance.on_tick()
                except Exception:
                    pass

    def get_app_card_badge(self, app: Dict[str, Any]) -> Optional[str]:
        """Опрашивает активные плагины для получения бейджа времени/статуса на карточке приложения."""
        for plugin_data in self.loaded_plugins.values():
            instance = plugin_data.get("instance")
            if instance and hasattr(instance, "get_app_card_badge"):
                try:
                    badge = instance.get_app_card_badge(app)
                    if badge:
                        return badge
                except Exception:
                    pass
        return None

    def is_app_running(self, app: Dict[str, Any]) -> bool:
        for plugin_data in self.loaded_plugins.values():
            instance = plugin_data.get("instance")
            if instance and hasattr(instance, "is_app_running"):
                try:
                    if instance.is_app_running(app):
                        return True
                except Exception:
                    pass
        return False

    def get_plugin_instance(self, plugin_name: str):
        data = self.loaded_plugins.get(plugin_name)
        return data.get("instance") if data else None

    def get_plugin_ui(self, plugin_name: str):
        plugin_data = self.loaded_plugins.get(plugin_name)
        if not plugin_data:
            return None

        plugin_instance = plugin_data.get("instance")
        if hasattr(plugin_instance, "get_ui_component"):
            return plugin_instance.get_ui_component()
        return None

    def create_plugin_template(self, slug: str, title: str) -> bool:
        """Генератор шаблона нового плагина по API v2.4."""
        safe_slug = "".join(c if c.isalnum() or c == "_" else "_" for c in slug.lower()).strip("_")
        if not safe_slug:
            return False
        if not safe_slug.endswith("_plugin"):
            safe_slug += "_plugin"

        file_path = self.plugins_dir / f"{safe_slug}.py"
        if file_path.exists():
            return False

        template = f'''import flet as ft


class CustomExtensionPlugin:
    PLUGIN_META = {{
        "id": "{safe_slug}",
        "name": "{title}",
        "version": "2.4.0",
        "description": "Пользовательское расширение, созданное через Plugin SDK 2.4",
        "icon": "auto_awesome",
    }}

    def __init__(self):
        self.context = None
        self.api = None

    def set_context(self, context):
        self.context = context

    def on_load(self, api):
        self.api = api

    def on_app_launched(self, app):
        pass

    def get_ui_component(self):
        return ft.Container(
            content=ft.Column([
                ft.Text("{title}", size=15, weight=ft.FontWeight.BOLD),
                ft.Text("Расширение активно и подключено к Plugin API 2.4", size=12),
            ], spacing=6),
            padding=12,
            border_radius=12,
        )


def initialize_plugin():
    return CustomExtensionPlugin()
'''
        file_path.write_text(template, encoding="utf-8")
        self.refresh_plugins(load_enabled=True)
        self.enable_plugin(safe_slug)
        return True

    def create_plugin_ui(self, colors):
        self.refresh_plugins(load_enabled=False)

        plugin_cards = []
        for plugin_name, plugin_info in self.available_plugins.items():
            is_enabled = plugin_info.get("enabled", False)
            is_loaded = plugin_name in self.loaded_plugins
            display_name = plugin_info.get("display_name", plugin_name)
            description = plugin_info.get("description", "")
            version = plugin_info.get("version", "2.4")
            icon_name = plugin_info.get("icon", "extension")

            status_text = "🟢 Активен" if is_loaded else "⚪ Выключен"
            status_color = colors["SUCCESS"] if is_loaded else colors["ON_SURFACE_VARIANT"]

            plugin_widget = self.get_plugin_ui(plugin_name) if is_loaded else None

            plugin_cards.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(icon_name, color=colors["ACCENT"], size=22),
                                    ft.Column(
                                        [
                                            ft.Row(
                                                [
                                                    ft.Text(display_name, weight=ft.FontWeight.BOLD, size=15),
                                                    ft.Text(f"v{version}", size=11, color=colors["ON_SURFACE_VARIANT"]),
                                                ],
                                                spacing=8,
                                            ),
                                            ft.Text(description, size=12, color=colors["ON_SURFACE_VARIANT"]),
                                        ],
                                        spacing=2,
                                        expand=True,
                                    ),
                                    ft.Container(
                                        content=ft.Text(status_text, size=12, color=status_color),
                                        bgcolor=colors["SURFACE_VARIANT"] + "40",
                                        padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                        border_radius=8,
                                    ),
                                ]
                            ),
                            ft.Row(
                                [
                                    ft.Switch(
                                        value=is_enabled,
                                        on_change=lambda e, pn=plugin_name: self.toggle_plugin(pn, e),
                                        active_track_color=colors["ACCENT"],
                                    ),
                                    ft.Text("Включен", size=12, color=colors["ON_SURFACE_VARIANT"]),
                                    ft.Container(width=12),
                                    ft.IconButton(
                                        icon="refresh",
                                        icon_size=16,
                                        on_click=lambda e, pn=plugin_name: self.reload_plugin(pn, e),
                                        tooltip="Перезагрузить плагин",
                                    ),
                                ]
                            ),
                            plugin_widget if plugin_widget else ft.Container(),
                        ],
                        spacing=8,
                    ),
                    bgcolor=colors["SETTINGS_CARD"],
                    border=ft.border.all(1, colors["OUTLINE"]),
                    border_radius=14,
                    padding=16,
                    margin=ft.margin.only(bottom=12),
                )
            )

        new_slug_field = ft.TextField(
            hint_text="ID плагина (напр. my_timer)",
            filled=True,
            bgcolor=colors["SURFACE_VARIANT"],
            border_radius=10,
            border_color="transparent",
            expand=True,
        )
        new_title_field = ft.TextField(
            hint_text="Название расширения",
            filled=True,
            bgcolor=colors["SURFACE_VARIANT"],
            border_radius=10,
            border_color="transparent",
            expand=True,
        )

        def _on_create_template(e):
            slug = (new_slug_field.value or "").strip()
            title = (new_title_field.value or "").strip() or "Новое расширение"
            if slug and self.create_plugin_template(slug, title):
                e.page.show_snack_bar(ft.SnackBar(content=ft.Text(f"✅ Плагин '{title}' создан и подключен!"), action="OK"))
                if self.context and hasattr(self.context, "update_main_content"):
                    self.context.update_main_content()
                e.page.update()

        sdk_box = ft.Container(
            bgcolor=colors["SURFACE_VARIANT"] + "30",
            border_radius=12,
            padding=14,
            margin=ft.margin.only(bottom=14),
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon("code", color=colors["ACCENT"], size=20),
                            ft.Text("Plugin SDK 2.4 — Быстрое создание расширения", weight=ft.FontWeight.BOLD, size=14),
                        ]
                    ),
                    ft.Text(
                        "Создайте собственный плагин с поддержкой хуков on_app_launched, on_tick и бейджей карточек.",
                        size=12,
                        color=colors["ON_SURFACE_VARIANT"],
                    ),
                    ft.Row([new_slug_field, new_title_field, ft.FilledButton("Создать шаблон", icon="add", on_click=_on_create_template)]),
                ],
                spacing=8,
            ),
        )

        return ft.Column(
            [
                ft.Text("Платформа плагинов и расширений (API 2.4)", size=20, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Управляйте установленными модулями, трекером игрового времени и расширениями лаунчера",
                    size=13,
                    color=colors["ON_SURFACE_VARIANT"],
                ),
                ft.Container(height=8),
                sdk_box,
                *plugin_cards,
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
        )

    def toggle_plugin(self, plugin_name, e):
        if e.control.value:
            self.enable_plugin(plugin_name)
        else:
            self.disable_plugin(plugin_name)
        if self.context and hasattr(self.context, "update_main_content"):
            self.context.update_main_content()
        e.page.update()

    def reload_plugin(self, plugin_name, e):
        self.unload_plugin(plugin_name)
        loaded = self.load_plugin(plugin_name)
        message = f"Плагин {plugin_name} перезагружен" if loaded else f"Не удалось загрузить плагин {plugin_name}"
        e.page.show_snack_bar(ft.SnackBar(content=ft.Text(message), action="OK"))
        if self.context and hasattr(self.context, "update_main_content"):
            self.context.update_main_content()
        e.page.update()
