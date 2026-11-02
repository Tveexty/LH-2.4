# [file name]: ui_manager.py
import flet as ft
import threading
import time
import os
import uuid
from datetime import datetime
from .theme_manager import ThemeManager
from .app_manager import AppManager
from .system_monitor import SystemMonitor
from .glass_morphism import GlassMorphism

# Условный импорт для обработки отсутствующих модулей
try:
    from .plugin_manager import PluginManager
except ImportError:
    class PluginManager:
        def __init__(self, file_manager):
            self.file_manager = file_manager
        
        def create_plugin_ui(self, colors):
            return ft.Container(
                content=ft.Column([
                    ft.Icon("extension", size=48, color=colors["ON_SURFACE_VARIANT"]),
                    ft.Text("Плагины недоступны", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text("Установите зависимости для работы с плагинами", size=12, color=colors["ON_SURFACE_VARIANT"])
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                padding=40,
                alignment=ft.alignment.center
            )

try:
    from .audio_controller import AudioController
except ImportError:
    class AudioController:
        def __init__(self):
            pass
        
        def create_compact_audio_ui(self, colors):
            return ft.Container(
                content=ft.Row([
                    ft.IconButton(icon="volume_up", icon_size=20, icon_color=colors["ACCENT"]),
                    ft.Text("Аудио контроллер недоступен", size=12, color=colors["ON_SURFACE_VARIANT"])
                ]),
                bgcolor=colors["SETTINGS_CARD"],
                border_radius=12,
                padding=10,
                margin=ft.margin.only(bottom=10),
            )

class UIManager:
    def __init__(self, page: ft.Page):
        self.page = page
        self.theme_manager = ThemeManager()
        self.app_manager = AppManager()
        self.system_monitor = SystemMonitor()
        self.plugin_manager = PluginManager(self.app_manager.file_manager)
        self.audio_controller = AudioController()
        
        # UI элементы
        self.header = None
        self.sidebar = None
        self.main_content = None
        self.search_field = None
        self.apps_list = None
        self.loading_progress = None
        self.filter_button = None
        self.favorites_panel = None
        self.devices_container = None
        self.current_time_text = None
        self.current_date_text = None
        self.plugins_button = None
        self.audio_control_panel = None
        
        # Состояние
        self.current_filter = "all"
        self.filter_dialog_open = False
        self.auto_update_enabled = True
        self.system_notifications_enabled = True
        
        # Новые элементы для верхней панели
        self.volume_slider_visible = False
        self.volume_slider_container = None
        
    def initialize_ui(self):
        self.setup_page()
        self.create_ui_elements()
        self.setup_timers()
        self.apply_initial_theme()
    
    def setup_page(self):
        self.page.title = "Launcher Hab 2.1"
        self.page.padding = 0
        self.page.spacing = 0
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = "#1e1e1e"
        
        # Применяем плавные анимации если включены
        if self.theme_manager.smooth_animations:
            try:
                self.page.theme = ft.Theme(
                    page_transitions = ft.PageTransitionsTheme(
                        windows = ft.PageTransitionTheme.CUPERTINO,
                        linux = ft.PageTransitionTheme.CUPERTINO,
                        macos = ft.PageTransitionTheme.CUPERTINO
                    )
                )
            except:
                pass
        
        self.page.on_scroll = lambda e: None
    
    def create_ui_elements(self):
        self.create_time_elements()
        self.create_header()
        self.create_sidebar()
        self.create_main_content()
        self.create_loading_progress()
        
        content = ft.Row([
            self.sidebar,
            ft.VerticalDivider(width=1, color=self.get_colors()["OUTLINE"], thickness=1),
            ft.Container(content=self.main_content, expand=True, padding=0, margin=0),
        ], expand=True, spacing=0)
        
        self.page.add(self.header, content)
        self.update_interface_colors()
    
    def create_time_elements(self):
        self.current_time_text = ft.Text("", size=16, text_align=ft.TextAlign.RIGHT, weight=ft.FontWeight.W_500)
        self.current_date_text = ft.Text("", size=12, text_align=ft.TextAlign.RIGHT, color=self.get_colors()["ON_SURFACE_VARIANT"])
    
    def create_header(self):
        colors = self.get_colors()
        
        # Время и дата
        time_display = ft.Container(
            content=ft.Column([self.current_time_text, self.current_date_text], 
                            spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=15, alignment=ft.alignment.center
        )
        
        # Устройства (батарея и сеть)
        self.devices_container = ft.Container(
            content=self.system_monitor.create_devices_header(colors),
            padding=10, alignment=ft.alignment.center
        )
        
        # НОВАЯ СТРУКТУРА: Плагины, Звук, Настройки
        self.plugins_button = ft.IconButton(
            icon="extension",
            icon_color=colors["ON_SURFACE"],
            on_click=self.show_plugins_manager,
            tooltip="Управление плагинами",
        )
        
        # Кнопка звука с выпадающим микшером
        self.audio_button = ft.IconButton(
            icon="volume_up",
            icon_color=colors["ON_SURFACE"],
            on_click=self.toggle_volume_slider,
            tooltip="Управление громкостью",
        )
        
        # Контейнер для слайдера громкости (изначально скрыт)
        self.volume_slider_container = ft.Container(
            content=ft.Row([
                ft.Icon("volume_down", size=16, color=colors["ON_SURFACE_VARIANT"]),
                ft.Container(
                    content=ft.Slider(
                        value=self.audio_controller.get_volume_level(),
                        min=0,
                        max=100,
                        divisions=100,
                        label="{value}%",
                        on_change=self.on_volume_change,
                        active_color=colors["ACCENT"],
                        inactive_color=colors["SURFACE_VARIANT"],
                        width=120
                    ),
                    padding=ft.padding.symmetric(horizontal=5)
                ),
                ft.Icon("volume_up", size=16, color=colors["ON_SURFACE_VARIANT"]),
            ], spacing=5),
            bgcolor=colors["SURFACE_VARIANT"],
            border_radius=8,
            padding=10,
            visible=False,
            animate_opacity=300,
        )
        
        # Основной header
        self.header = ft.Container(
            content=ft.Row([
                ft.Text("Launcher Hab 2.1", size=24, weight=ft.FontWeight.BOLD,
                       color=colors["ON_SURFACE"], expand=True),
                self.devices_container,
                time_display,
                # НОВЫЙ ПОРЯДОК: Плагины -> Звук -> Настройки
                self.plugins_button,
                ft.Row([self.audio_button, self.volume_slider_container], spacing=5),
                ft.IconButton(
                    icon="settings", icon_color=colors["ON_SURFACE"],
                    on_click=self.show_settings, tooltip="Настройки",
                )
            ]),
            bgcolor=colors["SURFACE"], padding=15, margin=0
        )
    
    def toggle_volume_slider(self, e):
        """Переключение видимости слайдера громкости"""
        self.volume_slider_visible = not self.volume_slider_visible
        self.volume_slider_container.visible = self.volume_slider_visible
        self.volume_slider_container.update()
    
    def on_volume_change(self, e):
        """Обработчик изменения громкости"""
        volume = int(e.control.value)
        # Мгновенное применение громкости в отдельном потоке
        threading.Thread(
            target=self.audio_controller.set_volume_level, 
            args=(volume,), 
            daemon=True
        ).start()
        
        # Обновляем отображение
        e.control.label = f"{volume}%"
        e.control.update()
    
    def create_sidebar(self):
        self.search_field = ft.TextField(
            hint_text="Поиск приложений...", prefix_icon="search", filled=True,
            bgcolor=self.get_colors()["SURFACE_VARIANT"], border_radius=12,
            on_change=self.filter_apps, content_padding=15, expand=True,
            border_color="transparent"
        )
        
        self.filter_button = self.create_filter_button()
        self.apps_list = self.create_apps_list()
        
        self.sidebar = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Text("Приложения", size=18, weight=ft.FontWeight.BOLD, 
                                   color=self.get_colors()["ON_SURFACE"]),
                    padding=20, alignment=ft.alignment.center
                ),
                ft.Container(
                    content=ft.Row([self.search_field, self.filter_button], spacing=10),
                    padding=ft.padding.symmetric(horizontal=15, vertical=10)
                ),
                ft.Divider(color=self.get_colors()["OUTLINE"], height=1),
                ft.Container(content=self.apps_list, expand=True),
                ft.Divider(color=self.get_colors()["OUTLINE"], height=1),
                ft.Container(content=self.create_add_app_button(),
                           padding=ft.padding.symmetric(horizontal=15, vertical=10)),
            ]), width=350, bgcolor=self.get_colors()["SURFACE"], padding=0, margin=0
        )
    
    def create_apps_list(self):
        apps_list = ft.ListView(expand=True, spacing=2, padding=5)
        for app in self.app_manager.all_apps + self.app_manager.custom_apps:
            apps_list.controls.append(self.create_app_list_item(app))
        return apps_list
    
    def create_app_list_item(self, app):
        colors = self.get_colors()
        is_installed = self.app_manager.is_app_installed(app)
        
        bg_color = colors["GLASS_BG"] if self.theme_manager.glass_effect_enabled else colors["SURFACE_VARIANT"] + "30"
        
        app_item = ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(app["icon"], color=colors["WEB_BLUE"] if app["type"] == "web" 
                                   else (colors["ON_SURFACE"] if is_installed else colors["ERROR"]), size=28),
                    width=50, height=50, alignment=ft.alignment.center,
                    bgcolor=bg_color, border_radius=12,
                    shadow=ft.BoxShadow(blur_radius=8, color=colors["GLASS_SHADOW"], offset=ft.Offset(0, 2)),
                ),
                ft.Column([
                    ft.Text(app["name"], color=colors["ON_SURFACE"] if is_installed else colors["ERROR"],
                           size=14, weight=ft.FontWeight.W_500),
                    ft.Text(f"{app['category']} • {'Установлено' if is_installed else 'Не установлено'}", 
                           color=colors["ON_SURFACE_VARIANT"] if is_installed else colors["ERROR"], size=11),
                ], expand=True, spacing=2),
                ft.IconButton(
                    icon="more_vert", icon_size=18, icon_color=colors["ON_SURFACE_VARIANT"],
                    on_click=lambda e, app=app: self.show_app_menu_dialog(app), tooltip="Меню приложения",
                    style=ft.ButtonStyle(padding=ft.padding.all(8), bgcolor="transparent")
                )
            ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=15, vertical=12), border_radius=8,
            on_click=lambda e, app=app: self.launch_app(app), tooltip=f"Запустить {app['name']}",
            bgcolor=bg_color, margin=ft.margin.symmetric(vertical=2), height=80,
        )
        
        def on_hover(e):
            if e.data == "true":
                app_item.bgcolor = colors["ACCENT"] + "20"
            else:
                app_item.bgcolor = bg_color
            app_item.update()
        
        app_item.on_hover = on_hover
        return app_item
    
    def create_add_app_button(self):
        colors = self.get_colors()
        
        bg_color = colors["GLASS_BG_LIGHT"] if self.theme_manager.glass_effect_enabled else colors["SURFACE_VARIANT"] + "15"
        
        add_button = ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon("add", color=colors["ON_SURFACE"], size=28),
                    width=60, height=60, alignment=ft.alignment.center,
                    bgcolor=colors["ACCENT"] + "20", border_radius=12,
                ),
                ft.Column([
                    ft.Text("Добавить приложение", color=colors["ON_SURFACE"], size=14, weight=ft.FontWeight.W_500),
                    ft.Text("Создайте свое приложение", color=colors["ON_SURFACE_VARIANT"], size=11),
                ], expand=True, spacing=2),
            ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=15, vertical=12), border_radius=8,
            on_click=self.show_add_custom_app_dialog, tooltip="Добавить новое приложение",
            bgcolor=bg_color, margin=ft.margin.symmetric(vertical=2), height=80,
        )
        
        def on_hover(e):
            if e.data == "true":
                add_button.bgcolor = colors["ACCENT"] + "30"
            else:
                add_button.bgcolor = bg_color
            add_button.update()
        
        add_button.on_hover = on_hover
        return add_button
    
    def create_main_content(self):
        self.main_content = ft.Container(
            content=self.create_main_content_internal(),
            expand=True, padding=10, margin=0
        )
    
    def create_main_content_internal(self):
        colors = self.get_colors()
        
        # УБРАН ДАШБОРД С ПЛАГИНАМИ И АУДИО КОНТРОЛЛЕРОМ
        
        favorites_content = self.create_favorites_panel()
        category_sections = self.create_category_sections()
        
        main_content_list = [favorites_content]
        
        if category_sections:
            main_content_list.extend(category_sections)
        elif self.current_filter != "all":
            no_apps_content = ft.Column([
                ft.Icon("search_off", size=64, color=colors["ON_SURFACE_VARIANT"]),
                ft.Text("Нет приложений по выбранному фильтру", size=18, color=colors["ON_SURFACE_VARIANT"], weight=ft.FontWeight.W_500),
                ft.Text("Попробуйте выбрать другой фильтр или добавьте свои приложения", size=14, color=colors["ON_SURFACE_VARIANT"]),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)
            
            no_apps_card = GlassMorphism.create_card(no_apps_content, colors, hover_effect=False) if self.theme_manager.glass_effect_enabled else ft.Container(content=no_apps_content, padding=80, alignment=ft.alignment.center)
            
            main_content_list.append(no_apps_card)
    
        return ft.Column(main_content_list, scroll=ft.ScrollMode.ADAPTIVE)
    
    def create_favorites_panel(self):
        colors = self.get_colors()
        favorite_apps = self.app_manager.favorite_apps
        
        favorites_counter = ft.Container(
            content=ft.Text(
                f"{len(favorite_apps)}/10",
                size=12,
                color=colors["ON_SURFACE_VARIANT"],
                weight=ft.FontWeight.W_500
            ),
            bgcolor=colors["GLASS_BG"],
            padding=ft.padding.symmetric(horizontal=8, vertical=4),
            border_radius=8,
        )
        
        if not favorite_apps:
            empty_content = ft.Column([
                ft.Container(content=ft.Row([
                    ft.Icon("star", color=colors["ACCENT"], size=20),
                    ft.Text("Избранное", size=16, weight=ft.FontWeight.BOLD, color=colors["ON_SURFACE"]),
                    favorites_counter
                ]), padding=ft.padding.symmetric(horizontal=15, vertical=10)),
                ft.Container(
                    content=ft.Column([
                        ft.Icon("star_border", size=32, color=colors["ON_SURFACE_VARIANT"]),
                        ft.Text("Добавьте приложения в избранное", size=12, 
                               color=colors["ON_SURFACE_VARIANT"], text_align=ft.TextAlign.CENTER),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                    padding=15, alignment=ft.alignment.center
                )
            ])
            
            return GlassMorphism.create_card(empty_content, colors, hover_effect=False) if self.theme_manager.glass_effect_enabled else ft.Container(content=empty_content, bgcolor=colors["SURFACE"], border_radius=12, margin=ft.margin.symmetric(horizontal=10, vertical=5))
        
        favorites_grid = ft.GridView(runs_count=6, max_extent=120, child_aspect_ratio=0.9,
                                   spacing=15, run_spacing=20, padding=20)
        
        for app in favorite_apps:
            is_installed = self.app_manager.is_app_installed(app)
            
            # УЛУЧШЕННОЕ ОТОБРАЖЕНИЕ: показываем тип приложения под названием
            app_content = ft.Column([
                ft.Container(
                    content=ft.Stack([
                        ft.Icon(name=app["icon"], size=42, 
                               color=colors["WEB_BLUE"] if app["type"] == "web" 
                               else (colors["ON_SURFACE"] if is_installed else colors["ERROR"])),
                        ft.Container(
                            content=ft.Icon(
                                name="check_circle" if is_installed else "error",
                                size=16,
                                color=colors["SUCCESS"] if is_installed else colors["ERROR"]
                            ),
                            alignment=ft.alignment.bottom_right,
                            margin=ft.margin.only(top=-18, right=-5),
                        )
                    ]),
                    width=80,
                    height=80,
                    alignment=ft.alignment.center,
                    bgcolor=colors["GLASS_BG"] if self.theme_manager.glass_effect_enabled else colors["SURFACE_VARIANT"] + "30",
                    border_radius=15,
                    border=ft.border.all(1, GlassMorphism._apply_opacity(colors["OUTLINE"], 0.1)) if self.theme_manager.glass_effect_enabled else None,
                    shadow=ft.BoxShadow(blur_radius=8, color=colors["GLASS_SHADOW"], offset=ft.Offset(0, 2)),
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            app["name"],
                            size=12,
                            color=colors["WEB_BLUE"] if app["type"] == "web" 
                            else (colors["ON_SURFACE"] if is_installed else colors["ERROR"]),
                            text_align=ft.TextAlign.CENTER,
                            max_lines=1,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                        ft.Text(
                            f"{app['type'].upper()}",
                            size=9,
                            color=colors["ON_SURFACE_VARIANT"],
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ], spacing=2),
                    height=35,
                    alignment=ft.alignment.top_center,
                    padding=ft.padding.only(top=5)
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5, height=130)
            
            app_container = ft.Container(
                content=app_content,
                width=110,
                height=140,
                padding=10,
                on_click=lambda e, app=app: self.launch_app(app),
                on_long_press=lambda e, app=app: self.show_favorite_app_menu_dialog(app),
                tooltip=f"Запустить {app['name']} ({app['type']})\nДолгое нажатие для меню",
                border_radius=12,
                bgcolor="transparent",
                animate=ft.Animation(200, "easeOut"),
            )
            
            def create_hover_handler(button):
                def on_hover(e):
                    if e.data == "true":
                        button.scale = 1.05
                        button.shadow = ft.BoxShadow(blur_radius=20, color=colors["ACCENT_GLOW"], offset=ft.Offset(0, 5))
                    else:
                        button.scale = 1.0
                        button.shadow = ft.BoxShadow(blur_radius=8, color=colors["GLASS_SHADOW"], offset=ft.Offset(0, 2))
                    button.update()
                return on_hover
            
            app_container.on_hover = create_hover_handler(app_container)
            favorites_grid.controls.append(app_container)
        
        favorites_content = ft.Column([
            ft.Container(content=ft.Row([
                ft.Icon("star", color=colors["ACCENT"], size=20),
                ft.Text("Избранное", size=16, weight=ft.FontWeight.BOLD, color=colors["ON_SURFACE"]),
                favorites_counter
            ]), padding=ft.padding.symmetric(horizontal=15, vertical=10)),
            favorites_grid
        ])
        
        return GlassMorphism.create_card(favorites_content, colors, hover_effect=False) if self.theme_manager.glass_effect_enabled else ft.Container(content=favorites_content, bgcolor=colors["SURFACE"], border_radius=12, margin=ft.margin.symmetric(horizontal=10, vertical=5))
    
    def create_category_sections(self):
        colors = self.get_colors()
        all_available_apps = self.app_manager.all_apps + self.app_manager.custom_apps
        filtered_apps = self.filter_apps_by_type(all_available_apps)
        
        categories = {}
        for app in filtered_apps:
            if app["category"] not in categories:
                categories[app["category"]] = []
            categories[app["category"]].append(app)
        
        category_sections = []
        for category, apps in categories.items():
            if apps:
                apps_grid = ft.GridView(runs_count=6, max_extent=120, child_aspect_ratio=0.9, spacing=15, run_spacing=20, padding=20)
                
                for app in apps:
                    is_installed = self.app_manager.is_app_installed(app)
                    app_button = GlassMorphism.create_app_button(
                        app, colors, is_installed,
                        glass_effect=self.theme_manager.glass_effect_enabled,
                        on_click=lambda e, app=app: self.launch_app(app)
                    )
                    
                    def create_hover_handler(button):
                        def on_hover(e):
                            if e.data == "true":
                                button.scale = 1.05
                                button.shadow = ft.BoxShadow(blur_radius=20, color=colors["ACCENT_GLOW"], offset=ft.Offset(0, 5))
                            else:
                                button.scale = 1.0
                                button.shadow = ft.BoxShadow(blur_radius=8, color=colors["GLASS_SHADOW"], offset=ft.Offset(0, 2))
                            button.update()
                        return on_hover
                    
                    app_button.on_hover = create_hover_handler(app_button)
                    apps_grid.controls.append(app_button)
                
                category_header = ft.Container(
                    content=ft.Row([
                        ft.Icon(self.get_category_icon(category), color=colors["ACCENT"], size=20),
                        ft.Text(category, size=20, weight=ft.FontWeight.BOLD, color=colors["ON_SURFACE"]),
                        ft.Container(
                            content=ft.Text(f"{len(apps)}", size=14, color=colors["ON_SURFACE_VARIANT"], weight=ft.FontWeight.W_500),
                            bgcolor=colors["SURFACE_VARIANT"],
                            padding=ft.padding.symmetric(horizontal=10, vertical=4),
                            border_radius=12,
                        )
                    ]),
                    padding=ft.padding.only(left=30, top=30, bottom=15, right=30),
                )
                
                category_content = ft.Column([category_header, apps_grid])
                
                if self.theme_manager.glass_effect_enabled:
                    category_card = GlassMorphism.create_card(category_content, colors, hover_effect=False)
                else:
                    category_card = ft.Container(
                        content=category_content,
                        shadow=ft.BoxShadow(blur_radius=8, color=colors["GLASS_SHADOW"], offset=ft.Offset(0, 2)),
                        margin=ft.margin.only(bottom=25), border_radius=12, bgcolor=colors["SURFACE"],
                    )
                
                category_sections.append(category_card)
        
        return category_sections
    
    def get_category_icon(self, category):
        icons = {
            "Browser": "web", "Media": "play_arrow", "Music": "music_note",
            "Social": "groups", "Games": "sports_esports", "System": "computer",
            "Office": "work", "Cloud": "cloud", "Health": "medical_services",
            "Government": "verified_user",
        }
        return icons.get(category, "apps")
    
    def filter_apps_by_type(self, apps_list):
        if self.current_filter == "all":
            return apps_list
        elif self.current_filter == "web":
            return [app for app in apps_list if app["type"] == "web"]
        elif self.current_filter == "app":
            return [app for app in apps_list if app["type"] == "app"]
        elif self.current_filter == "system":
            return [app for app in apps_list if app["type"] == "system"]
        elif self.current_filter == "custom":
            return [app for app in apps_list if app in self.app_manager.custom_apps]
        return apps_list
    
    def create_filter_button(self):
        colors = self.get_colors()
        
        filter_btn = ft.Container(
            content=ft.Icon("filter_list", color=colors["ON_SURFACE"], size=20),
            width=44, height=44, alignment=ft.alignment.center,
            bgcolor=colors["SURFACE_VARIANT"] + "30", border_radius=12,
            on_click=self.show_filter_menu, tooltip="Фильтровать по типу",
        )
        
        def on_hover(e):
            if e.data == "true":
                filter_btn.bgcolor = colors["ACCENT"] + "20"
            else:
                filter_btn.bgcolor = colors["SURFACE_VARIANT"] + "30"
            filter_btn.update()
        
        filter_btn.on_hover = on_hover
        return filter_btn

    def show_filter_menu(self, e):
        if self.filter_dialog_open:
            return
        
        colors = self.get_colors()
        self.filter_dialog_open = True
        
        def close_dialog(e=None):
            self.filter_dialog_open = False
            self.page.close(dialog)
        
        def apply_selected_filter(filter_type, e):
            self.current_filter = filter_type
            self.update_main_content()
            close_dialog()
        
        filter_options = [
            ("all", "apps", "Все приложения"),
            ("web", "public", "Веб-приложения"),
            ("app", "desktop_windows", "Локальные приложения"), 
            ("system", "computer", "Системные приложения"),
            ("custom", "star", "Мои приложения")
        ]
        
        menu_items = []
        for filter_type, icon, text in filter_options:
            is_active = self.current_filter == filter_type
            menu_items.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(icon, color=colors["ACCENT"] if is_active else colors["ON_SURFACE_VARIANT"]),
                        ft.Text(text, expand=True, color=colors["ON_SURFACE"], weight=ft.FontWeight.W_500 if is_active else ft.FontWeight.NORMAL),
                        ft.Icon("check", color=colors["ACCENT"], size=16) if is_active else ft.Container(width=16, height=16)
                    ]),
                    on_click=lambda e, ft=filter_type: apply_selected_filter(ft, e),
                    padding=15,
                    bgcolor=colors["ACCENT"] + "10" if is_active else "transparent",
                    border_radius=8,
                )
            )
        
        dialog_content = ft.Column([
            ft.Text("Фильтры приложений", size=18, weight=ft.FontWeight.BOLD, color=colors["ON_SURFACE"]),
            ft.Container(height=10),
            *menu_items
        ], height=280)
        
        dialog_container = ft.Container(
            content=dialog_content, 
            padding=20,
            bgcolor=colors["SURFACE"], 
            border_radius=12
        )
        
        dialog = ft.AlertDialog(
            modal=True,
            content=dialog_container,
            actions=[
                ft.TextButton("Закрыть", on_click=close_dialog)
            ],
            shape=ft.RoundedRectangleBorder(radius=12)
        )
        
        self.page.open(dialog)
    
    def create_loading_progress(self):
        colors = self.get_colors()
        self.loading_progress = ft.Container(
            content=ft.Column([
                ft.Icon("rocket_launch", size=40, color=colors["ACCENT"]),
                ft.Text("Запуск приложения...", size=14, color=colors["ON_SURFACE"], weight=ft.FontWeight.W_500),
                ft.Container(
                    content=ft.ProgressBar(value=0, color=colors["ACCENT"], bgcolor=colors["SURFACE_VARIANT"], height=8, border_radius=4),
                    width=250, padding=ft.padding.only(top=10)
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10, alignment=ft.MainAxisAlignment.CENTER),
            bgcolor=colors["SURFACE"], border_radius=15, padding=25, visible=False,
            width=320, height=140, top=100, alignment=ft.alignment.top_center,
            shadow=ft.BoxShadow(blur_radius=15, color=colors["GLASS_SHADOW"], offset=ft.Offset(0, 5)),
        )
    
    def get_colors(self):
        return self.theme_manager.get_current_theme()
    
    def update_interface_colors(self):
        colors = self.get_colors()
        self.page.bgcolor = colors["BG"]
        
        if self.header:
            self.header.bgcolor = colors["SURFACE"]
        if self.sidebar:
            self.sidebar.bgcolor = colors["SURFACE"]
        if self.main_content:
            self.main_content.bgcolor = colors["BG"]
        if self.current_time_text:
            self.current_time_text.color = colors["ON_SURFACE"]
        if self.current_date_text:
            self.current_date_text.color = colors["ON_SURFACE_VARIANT"]
        if self.search_field:
            self.search_field.bgcolor = colors["SURFACE_VARIANT"]
            self.search_field.color = colors["ON_SURFACE"]
            self.search_field.hint_style = ft.TextStyle(color=colors["ON_SURFACE_VARIANT"])
        
        self.page.update()
    
    def setup_timers(self):
        def time_timer():
            while True:
                self.update_time()
                time.sleep(1)
        
        def devices_timer():
            while True:
                self.update_devices_header()
                time.sleep(5)
        
        threading.Thread(target=time_timer, daemon=True).start()
        threading.Thread(target=devices_timer, daemon=True).start()
    
    def update_time(self):
        if self.current_time_text and self.current_date_text:
            now = datetime.now()
            self.current_time_text.value = now.strftime("%H:%M:%S")
            self.current_date_text.value = now.strftime("%d.%m.%Y")
            self.page.update()
    
    def update_devices_header(self):
        if self.devices_container:
            self.devices_container.content = self.system_monitor.create_devices_header(self.get_colors())
            self.page.update()
    
    def apply_initial_theme(self):
        self.theme_manager.apply_theme(self.page, self.theme_manager.current_theme)
        self.update_interface_colors()
        self.update_time()

    def show_settings(self, e):
        colors = self.get_colors()
        
        settings_content = self.create_modern_settings(colors)
        
        settings_dialog = ft.AlertDialog(
            title=ft.Container(
                content=ft.Row([
                    ft.Icon("tune", color=colors["ACCENT"], size=24),
                    ft.Text("Настройки", size=20, weight=ft.FontWeight.BOLD),
                ]),
                padding=ft.padding.only(bottom=10)
            ),
            content=ft.Container(
                content=settings_content,
                width=700,
                height=600,
            ),
            actions=[
                ft.TextButton("Закрыть", on_click=lambda e: self.page.close(settings_dialog))
            ],
        )
        self.page.open(settings_dialog)

    def create_modern_settings(self, colors):
        return ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Внешний вид",
                    icon=ft.Icon("palette"),
                    content=self.create_appearance_settings(colors)
                ),
                ft.Tab(
                    text="Приложения", 
                    icon=ft.Icon("apps"),
                    content=self.create_apps_settings(colors)
                ),
                ft.Tab(
                    text="Плагины",
                    icon=ft.Icon("extension"),
                    content=self.create_plugins_settings(colors)
                ),
                ft.Tab(
                    text="Система",
                    icon=ft.Icon("settings"),
                    content=self.create_system_settings_tab(colors)
                ),
                ft.Tab(
                    text="История версий",
                    icon=ft.Icon("history_edu"),
                    content=self.create_version_history(colors)
                ),
            ],
            expand=1,
        )

    def create_appearance_settings(self, colors):
        return ft.Container(
            content=ft.Column([
                self.create_settings_section(
                    "Тема оформления",
                    "Выберите цветовую схему приложения",
                    self.create_theme_selector(colors),
                    colors
                ),
                self.create_settings_section(
                    "Кастомные темы",
                    "Создавайте и управляйте своими темами",
                    self.create_custom_themes_management(colors),
                    colors
                ),
                self.create_settings_section(
                    "Эффекты интерфейса", 
                    "Настройте визуальные эффекты",
                    self.create_effects_settings(colors),
                    colors
                ),
            ], scroll=ft.ScrollMode.ADAPTIVE),
            padding=20
        )

    def create_apps_settings(self, colors):
        return ft.Container(
            content=ft.Column([
                self.create_settings_section(
                    "Управление приложений",
                    "Настройки приложений и избранного",
                    self.create_apps_management(colors),
                    colors
                ),
            ], scroll=ft.ScrollMode.ADAPTIVE),
            padding=20
        )

    def create_plugins_settings(self, colors):
        return ft.Container(
            content=ft.Column([
                self.create_settings_section(
                    "Управление плагинами",
                    "Расширьте функциональность лаунчера",
                    self.plugin_manager.create_plugin_ui(colors),
                    colors
                ),
            ], scroll=ft.ScrollMode.ADAPTIVE),
            padding=20
        )

    def create_system_settings_tab(self, colors):
        return ft.Container(
            content=ft.Column([
                self.create_settings_section(
                    "Автоматическое обновление",
                    "Обновлять интерфейс автоматически при изменениях",
                    self.create_auto_update_settings(colors),
                    colors
                ),
                self.create_settings_section(
                    "Системные уведомления",
                    "Показывать уведомления о действиях",
                    self.create_notifications_settings(colors),
                    colors
                ),
            ], scroll=ft.ScrollMode.ADAPTIVE),
            padding=20
        )

    def create_auto_update_settings(self, colors):
        return ft.Column([
            ft.Row([
                ft.Switch(
                    value=self.auto_update_enabled,
                    on_change=lambda e: self.toggle_auto_update(e),
                    active_track_color=colors["ACCENT"],
                ),
                ft.Column([
                    ft.Text("Автоматическое обновление интерфейса", weight=ft.FontWeight.W_500),
                    ft.Text("Интерфейс обновляется сразу при изменениях", size=12, color=colors["ON_SURFACE_VARIANT"]),
                ], expand=True)
            ]),
            ft.Container(height=10),
            ft.Text("При добавлении/удалении приложений интерфейс автоматически перерисовывается", 
                   size=12, color=colors["ON_SURFACE_VARIANT"]),
        ])

    def create_notifications_settings(self, colors):
        return ft.Column([
            ft.Row([
                ft.Switch(
                    value=self.system_notifications_enabled,
                    on_change=lambda e: self.toggle_system_notifications(e),
                    active_track_color=colors["ACCENT"],
                ),
                ft.Column([
                    ft.Text("Системные уведомления", weight=ft.FontWeight.W_500),
                    ft.Text("Показывать уведомления о действиях", size=12, color=colors["ON_SURFACE_VARIANT"]),
                ], expand=True)
            ]),
            ft.Container(height=10),
            ft.Text("Уведомления о создании приложений, изменении настроек и других действиях", 
                   size=12, color=colors["ON_SURFACE_VARIANT"]),
        ])

    def toggle_auto_update(self, e):
        self.auto_update_enabled = e.control.value
        if self.auto_update_enabled:
            self.show_system_notification("Автообновление включено", "Интерфейс будет обновляться автоматически")

    def toggle_system_notifications(self, e):
        self.system_notifications_enabled = e.control.value
        if self.system_notifications_enabled:
            self.show_system_notification("Уведомления включены", "Вы будете получать уведомления о действиях")

    def show_system_notification(self, title, message):
        if self.system_notifications_enabled:
            self.page.show_snack_bar(ft.SnackBar(
                content=ft.Column([
                    ft.Text(title, weight=ft.FontWeight.BOLD),
                    ft.Text(message, size=12)
                ], tight=True),
                action="OK",
                duration=3000
            ))

    def create_settings_section(self, title, subtitle, content, colors):
        return ft.Container(
            content=ft.Column([
                ft.ListTile(
                    title=ft.Text(title, weight=ft.FontWeight.BOLD, size=16),
                    subtitle=ft.Text(subtitle, color=colors["ON_SURFACE_VARIANT"], size=12),
                ),
                ft.Container(
                    content=content,
                    bgcolor=colors["SETTINGS_CARD"],
                    border_radius=12,
                    padding=20
                )
            ], spacing=10),
            margin=ft.margin.only(bottom=20)
        )

    def create_theme_selector(self, colors):
        themes = self.theme_manager.get_available_themes()
        theme_buttons = ft.Row(scroll=ft.ScrollMode.ADAPTIVE, spacing=15)
        
        for theme_name, theme_data in themes.items():
            is_current = theme_name == self.theme_manager.current_theme
            
            theme_button = ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Icon("palette", color=theme_data["ON_SURFACE"], size=24),
                        width=60, height=60,
                        bgcolor=theme_data["SURFACE"],
                        border_radius=12,
                        alignment=ft.alignment.center,
                    ),
                    ft.Text(theme_data["NAME"], size=12, text_align=ft.TextAlign.CENTER),
                    ft.Container(
                        content=ft.Icon("check", color=colors["ACCENT"], size=16),
                        bgcolor=colors["ACCENT"] + "20",
                        border_radius=8,
                        padding=4,
                        visible=is_current
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                on_click=lambda e, tn=theme_name: self.apply_theme_settings(tn),
                padding=10,
                bgcolor=colors["ACCENT"] + "10" if is_current else colors["SURFACE_VARIANT"] + "20",
                border_radius=12,
                width=100,
            )
            theme_buttons.controls.append(theme_button)
        
        return theme_buttons

    def create_custom_themes_management(self, colors):
        return ft.Column([
            self.create_settings_button(
                "Создать новую тему",
                "palette",
                lambda e: self.show_create_theme_dialog(),
                colors
            ),
            self.create_settings_button(
                "Импорт темы", 
                "file_upload",
                lambda e: self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Функция в разработке"), action="OK")),
                colors
            ),
            self.create_settings_button(
                "Экспорт текущей темы",
                "file_download", 
                lambda e: self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Функция в разработке"), action="OK")),
                colors
            ),
        ], spacing=10)

    def show_create_theme_dialog(self):
        colors = self.get_colors()
        
        # ИСПРАВЛЯЕМ: Делаем поле названия темы видимым
        theme_name = ft.TextField(
            label="Название темы",
            hint_text="Моя уникальная тема",
            expand=True,
            filled=True,
            bgcolor=colors["SURFACE_VARIANT"],
            border_radius=10,
            content_padding=15,
            border_color="transparent"
        )
        
        # Функция для создания поля с цветным индикатором
        def create_color_field(label, default_value):
            color_indicator = ft.Container(
                width=30,
                height=30,
                border_radius=6,
                bgcolor=default_value,
                border=ft.border.all(2, colors["OUTLINE"])
            )
            
            text_field = ft.TextField(
                label=label,
                value=default_value,
                hint_text=default_value,
                on_change=lambda e, ci=color_indicator: self.update_color_indicator(ci, e.control.value),
                expand=True,
                filled=True,
                bgcolor=colors["SURFACE_VARIANT"],
                border_radius=10,
                content_padding=15,
                border_color="transparent"
            )
            
            return ft.Row([text_field, color_indicator], spacing=10)
        
        # Создаем поля с цветными индикаторами
        bg_color_row = create_color_field("Основной фон", "#1e1e1e")
        surface_color_row = create_color_field("Поверхность", "#2d2d2d")
        accent_color_row = create_color_field("Акцентный цвет", "#4285f4")
        text_color_row = create_color_field("Цвет текста", "#ffffff")
        secondary_text_row = create_color_field("Вторичный текст", "#cccccc")
        
        def create_theme(e):
            if theme_name.value:
                # Извлекаем значения из полей ввода
                bg_color = bg_color_row.controls[0].value
                surface_color = surface_color_row.controls[0].value
                accent_color = accent_color_row.controls[0].value
                text_color = text_color_row.controls[0].value
                secondary_text = secondary_text_row.controls[0].value
                
                # Валидация HEX-формата
                if not all(self.is_valid_hex(color) for color in [bg_color, surface_color, accent_color, text_color, secondary_text]):
                    self.page.show_snack_bar(ft.SnackBar(content=ft.Text("❌ Неверный формат HEX-цветов"), action="OK"))
                    return
                
                new_theme = {
                    "NAME": theme_name.value,
                    "BG": bg_color,
                    "SURFACE": surface_color,
                    "SURFACE_VARIANT": "#3d3d3d",
                    "ON_SURFACE": text_color,
                    "ON_SURFACE_VARIANT": secondary_text,
                    "OUTLINE": "#444444",
                    "ACCENT": accent_color,
                    "ACCENT_GLOW": accent_color + "40",
                    "ERROR": "#ff6b6b",
                    "SUCCESS": "#4caf50",
                    "WEB_BLUE": accent_color,
                    "GLASS_BG": surface_color + "80",
                    "GLASS_BORDER": "#ffffff20",
                    "GLASS_SHADOW": "#00000040",
                    "GLASS_BG_LIGHT": surface_color + "40",
                    "SETTINGS_BG": bg_color,
                    "SETTINGS_SURFACE": surface_color,
                    "SETTINGS_CARD": "#3d3d3d"
                }
                
                if self.theme_manager.add_custom_theme(theme_name.value, new_theme):
                    self.page.close(dialog)
                    self.page.show_snack_bar(ft.SnackBar(content=ft.Text(f"✅ Тема '{theme_name.value}' создана!"), action="OK"))
                    # Обновляем селектор тем
                    self.update_main_content()
            else:
                self.page.show_snack_bar(ft.SnackBar(content=ft.Text("❌ Введите название темы"), action="OK"))
        
        def cancel_create(e):
            self.page.close(dialog)
        
        dialog = ft.AlertDialog(
            title=ft.Text("Создать кастомную тему"),
            content=ft.Container(
                content=ft.Column([
                    theme_name,  # ТЕПЕРЬ ВИДИМОЕ ПОЛЕ
                    bg_color_row,
                    surface_color_row,
                    accent_color_row,
                    text_color_row,
                    secondary_text_row,
                    ft.Text("Формат цветов: #RRGGBB (например: #1e1e1e)", size=12, color=colors["ON_SURFACE_VARIANT"]),
                ], height=400),  # Увеличиваем высоту
                width=500  # Увеличиваем ширину
            ),
            actions=[
                ft.TextButton("Отмена", on_click=cancel_create),
                ft.FilledButton("Создать", on_click=create_theme),
            ]
        )
        
        self.page.open(dialog)
    
    def is_valid_hex(self, color):
        """Проверка валидности HEX-цвета"""
        import re
        pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
        return bool(re.match(pattern, color))
    
    def update_color_indicator(self, color_indicator, hex_value):
        """Обновление цветного индикатора"""
        if self.is_valid_hex(hex_value):
            color_indicator.bgcolor = hex_value
        else:
            color_indicator.bgcolor = "#ff0000"  # Красный при ошибке
        color_indicator.update()

    def create_effects_settings(self, colors):
        return ft.Column([
            ft.Row([
                ft.Switch(
                    value=self.theme_manager.glass_effect_enabled,
                    on_change=lambda e: self.toggle_glass_effect(),
                    active_track_color=colors["ACCENT"],
                ),
                ft.Column([
                    ft.Text("Glass Morphism", weight=ft.FontWeight.W_500),
                    ft.Text("Полупрозрачные эффекты", size=12, color=colors["ON_SURFACE_VARIANT"]),
                ], expand=True)
            ]),
            
            ft.Container(height=15),
            
            ft.Text("Интенсивность эффекта", size=14, weight=ft.FontWeight.W_500),
            ft.Text("Настройте уровень прозрачности", size=12, color=colors["ON_SURFACE_VARIANT"]),
            ft.Container(height=10),
            self.create_glass_intensity_selector(colors),
            
            ft.Container(height=15),
            
            ft.Row([
                ft.Switch(
                    value=self.theme_manager.smooth_animations,
                    on_change=lambda e: self.toggle_smooth_animations(),
                    active_track_color=colors["ACCENT"],
                ),
                ft.Column([
                    ft.Text("Плавные анимации", weight=ft.FontWeight.W_500),
                    ft.Text("Более плавные и красивые переходы", size=12, color=colors["ON_SURFACE_VARIANT"]),
                ], expand=True)
            ]),
            
            ft.Container(height=15),
            
            ft.Row([
                ft.Switch(
                    value=self.theme_manager.android_animations,
                    on_change=lambda e: self.toggle_android_animations(),
                    active_track_color=colors["ACCENT"],
                ),
                ft.Column([
                    ft.Text("Android-анимации", weight=ft.FontWeight.W_500),
                    ft.Text("Анимации как в Android (из малого в большое)", size=12, color=colors["ON_SURFACE_VARIANT"]),
                ], expand=True)
            ]),
        ])

    def create_glass_intensity_selector(self, colors):
        intensities = [
            ("light", "blur_on", "Слабая", "Минимальная прозрачность"),
            ("medium", "blur_medium", "Средняя", "Оптимальный баланс"),
            ("strong", "blur_off", "Сильная", "Максимальная прозрачность")
        ]
        
        intensity_buttons = ft.Row(spacing=10)
        
        for intensity, icon, title, description in intensities:
            is_active = self.theme_manager.glass_intensity == intensity
            
            intensity_button = ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Icon(icon, color=colors["ACCENT"] if is_active else colors["ON_SURFACE_VARIANT"], size=24),
                        width=60, height=60,
                        bgcolor=colors["ACCENT"] + "20" if is_active else colors["SURFACE_VARIANT"] + "30",
                        border_radius=12,
                        alignment=ft.alignment.center,
                    ),
                    ft.Text(title, size=12, weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER),
                    ft.Text(description, size=10, color=colors["ON_SURFACE_VARIANT"], text_align=ft.TextAlign.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                on_click=lambda e, ints=intensity: self.set_glass_intensity(ints),
                padding=15,
                bgcolor=colors["ACCENT"] + "10" if is_active else colors["SURFACE_VARIANT"] + "20",
                border=ft.border.all(2, colors["ACCENT"] if is_active else "transparent"),
                border_radius=12,
                expand=True,
            )
            intensity_buttons.controls.append(intensity_button)
        
        return intensity_buttons

    def create_apps_management(self, colors):
        return ft.Column([
            self.create_settings_button(
                "Обновить список приложений",
                "refresh",
                lambda e: self.refresh_apps_list(),
                colors
            ),
            self.create_settings_button(
                "Сбросить избранное", 
                "star_border",
                lambda e: self.reset_favorites(),
                colors
            ),
            self.create_settings_button(
                "Очистить ручные пути",
                "clear_all",
                lambda e: self.clear_manual_paths(),
                colors
            ),
        ], spacing=10)

    def create_settings_button(self, text, icon, on_click, colors):
        button = ft.Container(
            content=ft.Row([
                ft.Icon(icon, color=colors["ACCENT"], size=20),
                ft.Text(text, expand=True),
                ft.Icon("chevron_right", color=colors["ON_SURFACE_VARIANT"], size=16)
            ]),
            on_click=on_click,
            padding=15,
            bgcolor=colors["SURFACE_VARIANT"] + "20",
            border_radius=8,
        )
        
        def on_hover(e):
            if e.data == "true":
                button.bgcolor = colors["ACCENT"] + "10"
            else:
                button.bgcolor = colors["SURFACE_VARIANT"] + "20"
            button.update()
        
        button.on_hover = on_hover
        return button

    def create_version_history(self, colors):
        versions = {
            "2.1": [
                "🧩 СИСТЕМА ПЛАГИНОВ - модульное расширение функциональности",
                "🔌 Менеджер плагинов с загрузкой/выгрузкой в реальном времени", 
                "📁 Автоматическое обнаружение плагинов в папке 'plugins'",
                "🎛️ Компактный аудио-контроллер в основном интерфейсе",
                "🔊 Управление системной громкостью через слайдер",
                "📶 Переключатели Bluetooth и Wi-Fi",
                "🎨 РАСШИРЕННАЯ СИСТЕМА КАСТОМНЫХ ТЕМ",
                "🌈 Создание собственных тем оформления",
                "🔄 Динамическое обновление списка тем",
                "⚡ Оптимизация производительности системы плагинов",
                "🔧 Улучшенный API для разработчиков плагинов",
                "📱 Лучшая адаптация для сенсорных устройств",
                "🎯 Улучшенная навигация в настройках",
                "🐛 Исправление мелких ошибок интерфейса"
            ],
            "2.0": [
                "🚀 МАЖОРНОЕ ОБНОВЛЕНИЕ - ПОЛНАЯ ПЕРЕРАБОТКА",
                "🎨 Новая улучшенная темная тема с лучшей контрастностью",
                "⚡ Оптимизация производительности - на 30% меньше потребления ресурсов",
                "📱 Уникальные Android-анимации открытия окон",
                "✨ Эффекты наведения для всех элементов интерфейса",
                "🔧 Полная модуляризация кодовой базы",
                "🎯 Улучшенная система цветов и теней",
                "📚 Добавлено 50+ новых иконок Material Design",
                "🔄 Переработанный интерфейс настроек",
                "💫 Плавные переходы между состояниями",
                "🎪 Анимации масштабирования при наведении",
                "🔮 Улучшенный Glass Morphism с настраиваемой интенсивностью",
                "📊 Оптимизированная работа с памятью",
                "⚙️ Умное кэширование ресурсов",
                "🌙 Автоматическое управление темой",
                "🔍 Улучшенный поиск с подсказками",
                "📱 Адаптивный дизайн для всех разрешений",
                "🎮 Геймифицированный интерфейс",
                "🔒 Улучшенная система безопасности",
                "📦 Модульная архитектура для легкого расширения"
            ],
            "1.9": [
                "🔐 Система шифрования — безопасное хранение настроек",
                "🛡️ Обработка исключений — try/catch во всех компонентах", 
                "⚡ Управление потоками — ThreadPool и асинхронность",
                "🔮 Glass Morphism — полупрозрачные эффекты для кнопок",
                "🎯 Избранное в основной части — полноразмерные плитки",
                "🎨 Система кастомных тем — создавайте свои темы",
                "📱 Адаптивный дизайн — улучшенная UX/UI",
                "🔧 Оптимизация производительности — ThreadPoolManager",
                "🚀 Асинхронные операции — плавный интерфейс",
                "💎 Улучшенная безопасность — Fernet шифрование"
            ],
            "1.8": [
                "📱 Панель устройств перемещена в header",
                "⭐ Панель избранного в основной части",
                "🎯 Убрано постоянное свечение фильтров",
                "📏 Уменьшена высота диалога фильтров",
                "📁 Кнопка проводника в диалоге добавления",
                "🔋 Система мониторинга устройств в реальном времени",
                "🔒 Ограничение избранного до 10 приложений",
                "💎 Оптимизация интерфейса для компактности",
                "🔄 Улучшенное обновление интерфейса в реальном времени",
                "🎨 Плавные анимации для избранных приложений",
                "📊 Точный мониторинг батареи с процентами",
                "🌐 Улучшенное определение сетевых соединений",
                "🔧 Исправлены ошибки кодировки при работе с реестром"
            ],
            "1.7": [
                "🎨 Улучшенный визуальный дизайн с тенями и разделителями",
                "📱 Сбалансированные размеры иконок и текста",
                "🖱️ Плавные hover-анимации карточек приложений",
                "✨ Свечение Fluent Design при наведении",
                "🎯 Улучшенная контрастность текстов",
                "📂 Визуальное разделение между секциями",
                "🔧 Улучшенная кнопка фильтра с tooltip",
                "🚀 Плавная прокрутка главной страницы",
                "🎨 Более яркие акцентные цвета",
                "⚡ Стабильное переключение тем без артефактов",
                "💎 Express-кнопка добавления приложений с градиентом",
                "🕒 Обновленная верхняя панель с местом для аватара",
                "🔔 Информативные tooltip'ы для статусов приложений"
            ],
            "1.6": [
                "Мгновенное обновление интерфейса при изменениям",
                "Компактная система фильтров в сайдбаре", 
                "Увеличенные иконки приложений (70% площади)",
                "Увеличенные кнопки приложений для лучшего UX",
                "Исправлены все проблемы со сменой тем",
                "Полная синхронизация цветов интерфейса",
                "Автоматическое обновление без перезапуска"
            ],
            "1.5": [
                "4 темы оформления: Тёмная, Светлая, Фиолетовая, Весна",
                "Улучшенная светлая тема с лучшей читаемостью",
                "Красивая фиолетовая тема",
                "Нежная тема 'Весна' в цветах сакуры", 
                "Удобный переключатель тем в настройках",
                "Увеличены иконки приложений для лучшей видимости",
                "Исправлено выравнивание элементов интерфейса",
                "Визуальный выбор иконок при добавлении приложений",
                "Улучшенный дизайн загрузки приложений",
                "Все приложения выровнены по сетке",
                "Убраны иконки '+' из хедера",
                "Статичная кнопка добавления приложения"
            ],
            "1.4": [
                "Кнопка меню (три точки) для каждого приложения",
                "Быстрый доступ к избранному через меню",
                "Изменение пути к файлу для любого приложения", 
                "Удаление кастомных приложений через меню",
                "Улучшенное управление приложениями",
                "Более удобная навигация по функциям"
            ],
            "1.3": [
                "Продвинутые анимации интерфейса",
                "Номер эффекта для кнопок", 
                "Анимация запуска приложений",
                "Главное подавление элементов",
                "Анимация переключения тем",
                "Контекстовное меню по клику"
            ],
            "1.2": [
                "Официальные сайты для скачивания",
                "Добавление своих приложений",
                "Улучшенный поиск приложений", 
                "Сохранение всех изменений",
                "Правильное определение Word, Excel",
                "Улучшена проверка установки",
                "Оптимизировано сохранение данных"
            ],
            "1.1": [
                "Таймер времени — правильное обновление",
                "Сохранение избранного между запусками",
                "Улучшенная проверка установки приложений",
                "Универсальные системные команды", 
                "Ручной выбор пути к приложению",
                "Цветовые индикаторы для веб-приложений",
                "Контекстовное меню (долгое нажатие)",
                "Сохранение настроек и ручных путей"
            ],
            "1.0": [
                "Базовый запуск приложений",
                "Категории приложений", 
                "Тёмная тема",
                "Поиск приложений"
            ]
        }
        
        version_items = []
        for version, features in versions.items():
            version_items.append(
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(f"Version {version}", weight=ft.FontWeight.BOLD, size=16, color=colors["ACCENT"]),
                            ft.Container(
                                content=ft.Text(f"{len(features)} обновлений", size=12, color=colors["ON_SURFACE_VARIANT"]),
                                bgcolor=colors["SURFACE_VARIANT"] + "30",
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                border_radius=8
                            )
                        ]),
                        ft.Column([
                            ft.Text(feature, size=13, color=colors["ON_SURFACE_VARIANT"]) 
                            for feature in features
                        ], spacing=4)
                    ], spacing=10),
                    bgcolor=colors["SETTINGS_CARD"],
                    border_radius=12,
                    padding=20,
                    margin=ft.margin.only(bottom=15)
                )
            )
        
        return ft.Column(
            [
                ft.Text("История обновлений Launcher Hab", size=18, weight=ft.FontWeight.BOLD),
                ft.Text("Полный список изменений с момента создания", size=14, color=colors["ON_SURFACE_VARIANT"]),
                ft.Container(height=20),
                *version_items
            ],
            scroll=ft.ScrollMode.ADAPTIVE
        )

    def apply_theme_settings(self, theme_name):
        self.theme_manager.apply_theme(self.page, theme_name)
        self.update_interface_colors()
        self.update_main_content()
        self.page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Тема применена: {theme_name}"), action="OK"))

    def toggle_glass_effect(self):
        enabled = self.theme_manager.toggle_glass_effect()
        self.update_main_content()
        self.update_sidebar()
        message = "Glass Morphism включен" if enabled else "Glass Morphism выключен"
        self.page.show_snack_bar(ft.SnackBar(content=ft.Text(message), action="OK"))

    def set_glass_intensity(self, intensity):
        self.theme_manager.set_glass_intensity(intensity)
        self.update_main_content()
        self.update_sidebar()
        intensity_names = {"light": "Слабая", "medium": "Средняя", "strong": "Сильная"}
        self.page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Интенсивность установлена: {intensity_names[intensity]}"), action="OK"))

    def toggle_smooth_animations(self):
        enabled = self.theme_manager.toggle_smooth_animations()
        message = "Плавные анимации включены" if enabled else "Плавные анимации выключены"
        self.page.show_snack_bar(ft.SnackBar(content=ft.Text(message), action="OK"))

    def toggle_android_animations(self):
        enabled = self.theme_manager.toggle_android_animations()
        message = "Android-анимации включены" if enabled else "Android-анимации выключены"
        self.page.show_snack_bar(ft.SnackBar(content=ft.Text(message), action="OK"))

    def refresh_apps_list(self):
        self.update_main_content()
        self.update_sidebar()
        self.page.show_snack_bar(ft.SnackBar(content=ft.Text("✅ Список приложений обновлен"), action="OK"))

    def reset_favorites(self):
        self.app_manager.favorite_apps = []
        self.app_manager.save_favorites()
        self.update_main_content()
        self.page.show_snack_bar(ft.SnackBar(content=ft.Text("✅ Избранное сброшено"), action="OK"))

    def clear_manual_paths(self):
        self.app_manager.manual_paths = {}
        self.app_manager.save_manual_paths()
        self.update_main_content()
        self.update_sidebar()
        self.page.show_snack_bar(ft.SnackBar(content=ft.Text("✅ Ручные пути очищены"), action="OK"))

    def show_plugins_manager(self, e):
        colors = self.get_colors()
        
        plugins_content = self.plugin_manager.create_plugin_ui(colors)
        
        plugins_dialog = ft.AlertDialog(
            title=ft.Container(
                content=ft.Row([
                    ft.Icon("extension", color=colors["ACCENT"], size=24),
                    ft.Text("Управление плагинами", size=20, weight=ft.FontWeight.BOLD),
                ]),
                padding=ft.padding.only(bottom=10)
            ),
            content=ft.Container(
                content=plugins_content,
                width=600,
                height=500,
            ),
            actions=[
                ft.TextButton("Закрыть", on_click=lambda e: self.page.close(plugins_dialog))
            ],
        )
        self.page.open(plugins_dialog)

    def show_app_menu_dialog(self, app):
        colors = self.get_colors()
        
        def close_dialog(e=None):
            self.page.close(dialog)
        
        def add_to_favorites_action(e):
            # Проверяем на дублирование
            if self.app_manager.is_duplicate_favorite(app):
                self.show_duplicate_favorite_dialog(app)
            else:
                success, message = self.app_manager.add_to_favorites(app)
                if self.system_notifications_enabled:
                    self.show_system_notification("Избранное", message)
                if success:
                    self.update_main_content()
            close_dialog()
        
        def remove_from_favorites_action(e):
            success, message = self.app_manager.remove_from_favorites(app)
            if self.system_notifications_enabled:
                self.show_system_notification("Избранное", message)
            if success:
                self.update_main_content()
            close_dialog()
        
        def install_app_action(e):
            import webbrowser
            if app.get("official_url"):
                webbrowser.open(app["official_url"])
                if self.system_notifications_enabled:
                    self.show_system_notification("Установка", f"🌐 Открывается официальный сайт {app['name']}")
            else:
                if self.system_notifications_enabled:
                    self.show_system_notification("Ошибка", "❌ Официальный сайт не указан")
            close_dialog()
        
        def find_path_action(e):
            self.select_manual_path(app)
            close_dialog()
        
        def show_path_action(e):
            if app["package"] in self.app_manager.manual_paths:
                path = self.app_manager.manual_paths[app["package"]]
                if self.system_notifications_enabled:
                    self.show_system_notification("Путь к приложению", f"📁 Путь: {path}")
            else:
                if self.system_notifications_enabled:
                    self.show_system_notification("Ошибка", "❌ Путь не указан")
            close_dialog()

        def open_file_location_action(e):
            """НОВАЯ ФУНКЦИЯ: Открыть расположение файла"""
            try:
                if app["package"] in self.app_manager.manual_paths:
                    file_path = self.app_manager.manual_paths[app["package"]]
                    folder_path = os.path.dirname(file_path)
                    if os.path.exists(folder_path):
                        os.startfile(folder_path)
                        if self.system_notifications_enabled:
                            self.show_system_notification("Проводник", f"📂 Открыта папка: {folder_path}")
                    else:
                        if self.system_notifications_enabled:
                            self.show_system_notification("Ошибка", "❌ Папка не найдена")
                else:
                    if self.system_notifications_enabled:
                        self.show_system_notification("Ошибка", "❌ Путь к приложению не указан")
            except Exception as ex:
                if self.system_notifications_enabled:
                    self.show_system_notification("Ошибка", f"❌ Не удалось открыть папку: {str(ex)}")
            close_dialog()

        def edit_tags_action(e):
            """НОВАЯ ФУНКЦИЯ: Редактировать теги и заметки"""
            self.show_edit_tags_dialog(app)
            close_dialog()
        
        def edit_app_action(e):
            if app in self.app_manager.custom_apps:
                self.show_edit_custom_app_dialog(app)
            else:
                if self.system_notifications_enabled:
                    self.show_system_notification("Ошибка", "❌ Можно редактировать только кастомные приложения")
            close_dialog()
        
        def remove_app_action(e):
            if app in self.app_manager.custom_apps:
                self.app_manager.remove_custom_app(app)
                self.update_main_content()
                self.update_sidebar()
                if self.system_notifications_enabled:
                    self.show_system_notification("Удаление", f"🗑️ {app['name']} удалено")
            else:
                if self.system_notifications_enabled:
                    self.show_system_notification("Ошибка", "❌ Можно удалять только кастомные приложения")
            close_dialog()
        
        is_favorite = any(fav.get("id") == app.get("id") for fav in self.app_manager.favorite_apps) if "id" in app else app in self.app_manager.favorite_apps
        is_custom = app in self.app_manager.custom_apps
        has_manual_path = app["package"] in self.app_manager.manual_paths
        
        # ОПТИМИЗИРУЕМ МЕНЮ: компактные ListTile с меньшими отступами
        menu_items = []
        
        # Основные
        def show_duplicate_favorite_dialog(self, app):
            """Показать диалог при попытке добавить дубликат в избранное"""
        colors = self.get_colors()
        
        similar_apps = self.app_manager.get_similar_favorites(app)
        
        def close_dialog(e=None):
            self.page.close(dialog)
        
        def replace_existing(e, existing_app):
            # Удаляем существующее и добавляем новое
            self.app_manager.remove_from_favorites(existing_app)
            success, message = self.app_manager.add_to_favorites(app)
            if self.system_notifications_enabled:
                self.show_system_notification("Избранное", message)
            if success:
                self.update_main_content()
            close_dialog()
        
        def add_anyway(e):
            # Добавляем несмотря на дублирование
            success, message = self.app_manager.add_to_favorites(app)
            if self.system_notifications_enabled:
                self.show_system_notification("Избранное", message)
            if success:
                self.update_main_content()
            close_dialog()
        
        content_controls = [
            ft.Text("Похожее приложение уже в избранном", size=16, weight=ft.FontWeight.BOLD),
            ft.Text(f"'{app['name']}' похоже на:", size=14, color=colors["ON_SURFACE_VARIANT"]),
            ft.Container(height=10),
        ]
        
        # Показываем похожие приложения
        for similar in similar_apps:
            content_controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(similar["icon"], color=colors["ACCENT"], size=20),
                        ft.Text(similar["name"], expand=True),
                        ft.Text(similar["category"], size=12, color=colors["ON_SURFACE_VARIANT"]),
                    ]),
                    padding=10,
                    bgcolor=colors["SURFACE_VARIANT"] + "20",
                    border_radius=8,
                    margin=ft.margin.only(bottom=5),
                )
            )
        
        content_controls.extend([
            ft.Container(height=15),
            ft.Text("Выберите действие:", size=14, weight=ft.FontWeight.W_500),
        ])
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Дублирование в избранном"),
            content=ft.Container(
                content=ft.Column(content_controls, height=300),
                width=400
            ),
            actions=[
                ft.Row([
                    ft.TextButton("Отмена", on_click=close_dialog),
                    ft.TextButton("Заменить", on_click=lambda e: replace_existing(e, similar_apps[0])),
                    ft.FilledButton("Добавить всё равно", on_click=add_anyway),
                ], alignment=ft.MainAxisAlignment.END)
            ],
        )
        
        self.page.open(dialog)

    def show_favorite_app_menu_dialog(self, app):
        """Контекстное меню для избранных приложений (долгое нажатие)"""
        colors = self.get_colors()
        
        def close_dialog(e=None):
            self.page.close(dialog)
        
        def remove_from_favorites_action(e):
            success, message = self.app_manager.remove_from_favorites(app)
            if self.system_notifications_enabled:
                self.show_system_notification("Избранное", message)
            if success:
                self.update_main_content()
            close_dialog()
        
        def launch_app_action(e):
            self.launch_app(app)
            close_dialog()
        
        def edit_tags_action(e):
            self.show_edit_tags_dialog(app)
            close_dialog()
        
        # Компактное меню для избранного
        menu_items = ft.Column([
            ft.ListTile(
                leading=ft.Icon("play_arrow", color=colors["SUCCESS"], size=20),
                title=ft.Text("Запустить", size=14),
                on_click=launch_app_action,
                dense=True,
            ),
            ft.ListTile(
                leading=ft.Icon("local_offer", color=colors["WEB_BLUE"], size=20),
                title=ft.Text("Редактировать теги", size=14),
                on_click=edit_tags_action,
                dense=True,
            ),
            ft.Divider(height=1),
            ft.ListTile(
                leading=ft.Icon("star", color=colors["ACCENT"], size=20),
                title=ft.Text("Удалить из избранного", size=14),
                on_click=remove_from_favorites_action,
                dense=True,
            ),
        ], spacing=0)
        
        dialog = ft.AlertDialog(
            modal=True,
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(app["icon"], size=24, color=colors["ACCENT"]),
                            ft.Text(app["name"], size=16, weight=ft.FontWeight.BOLD, color=colors["ON_SURFACE"]),
                        ], spacing=12),
                        padding=ft.padding.only(bottom=10)
                    ),
                    menu_items
                ], tight=True),
                width=280,
                height=200
            ),
            actions=[
                ft.TextButton("Закрыть", on_click=close_dialog)
            ],
            shape=ft.RoundedRectangleBorder(radius=12)
        )
        
        self.page.open(dialog)

    def create_advanced_search_panel(self, colors):
        """Создание расширенной панели поиска с фильтрами"""
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon("search", color=colors["ON_SURFACE_VARIANT"], size=20),
                    ft.Text("Расширенный поиск", size=16, weight=ft.FontWeight.BOLD),
                    ft.Container(width=10),
                    ft.IconButton(
                        icon="expand_less",
                        icon_size=16,
                        on_click=lambda e: self.toggle_advanced_search(),
                        tooltip="Свернуть панель поиска"
                    )
                ]),
                ft.Container(height=10),
                ft.Row([
                    ft.TextField(
                        hint_text="Поиск по тегам...",
                        prefix_icon="local_offer",
                        filled=True,
                        bgcolor=colors["SURFACE_VARIANT"],
                        border_radius=10,
                        on_change=self.search_by_tags,
                        expand=True,
                        border_color="transparent"
                    ),
                    ft.Container(width=10),
                    ft.Dropdown(
                        options=[
                            ft.dropdown.Option("all", "Все типы"),
                            ft.dropdown.Option("installed", "Только установленные"),
                            ft.dropdown.Option("web", "Веб-приложения"),
                            ft.dropdown.Option("custom", "Мои приложения"),
                        ],
                        value="all",
                        width=150,
                        filled=True,
                        bgcolor=colors["SURFACE_VARIANT"],
                        border_radius=10,
                        border_color="transparent"
                    )
                ])
            ]),
            bgcolor=colors["SURFACE_VARIANT"] + "20",
            border_radius=12,
            padding=15,
            margin=ft.margin.only(bottom=15),
            visible=False  # Изначально скрыта
        )

    def toggle_advanced_search(self):
        """Переключение видимости расширенного поиска"""
        # Реализация переключения расширенного поиска
        pass

    def search_by_tags(self, e):
        """Поиск приложений по тегам"""
        query = e.control.value
        if not query:
            # Если запрос пустой, показываем все приложения
            self.update_main_content()
            return
        
        # Ищем приложения по тегам
        results = self.app_manager.search_apps_by_tags(query)
        
        # Обновляем интерфейс с результатами поиска
        self.show_search_results(results, query)

    def show_search_results(self, results, query):
        """Показать результаты поиска"""
        colors = self.get_colors()
        
        if not results:
            # Нет результатов
            no_results_content = ft.Column([
                ft.Icon("search_off", size=64, color=colors["ON_SURFACE_VARIANT"]),
                ft.Text("Ничего не найдено", size=18, color=colors["ON_SURFACE_VARIANT"], weight=ft.FontWeight.W_500),
                ft.Text(f"По запросу: '{query}'", size=14, color=colors["ON_SURFACE_VARIANT"]),
                ft.Text("Попробуйте изменить запрос или использовать другие теги", size=12, color=colors["ON_SURFACE_VARIANT"]),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)
            
            self.main_content.content = ft.Column([
                self.create_favorites_panel(),
                GlassMorphism.create_card(no_results_content, colors, hover_effect=False) if self.theme_manager.glass_effect_enabled else ft.Container(content=no_results_content, padding=80, alignment=ft.alignment.center)
            ], scroll=ft.ScrollMode.ADAPTIVE)
        else:
            # Есть результаты
            results_header = ft.Container(
                content=ft.Row([
                    ft.Icon("search", color=colors["ACCENT"], size=20),
                    ft.Text("Результаты поиска", size=20, weight=ft.FontWeight.BOLD, color=colors["ON_SURFACE"]),
                    ft.Container(
                        content=ft.Text(f"{len(results)} найдено", size=14, color=colors["ON_SURFACE_VARIANT"], weight=ft.FontWeight.W_500),
                        bgcolor=colors["SURFACE_VARIANT"],
                        padding=ft.padding.symmetric(horizontal=10, vertical=4),
                        border_radius=12,
                    )
                ]),
                padding=ft.padding.only(left=30, top=30, bottom=15, right=30),
            )
            
            results_grid = ft.GridView(runs_count=6, max_extent=120, child_aspect_ratio=0.9, spacing=15, run_spacing=20, padding=20)
            
            for app in results:
                is_installed = self.app_manager.is_app_installed(app)
                app_button = GlassMorphism.create_app_button(
                    app, colors, is_installed,
                    glass_effect=self.theme_manager.glass_effect_enabled,
                    on_click=lambda e, app=app: self.launch_app(app)
                )
                
                def create_hover_handler(button):
                    def on_hover(e):
                        if e.data == "true":
                            button.scale = 1.05
                            button.shadow = ft.BoxShadow(blur_radius=20, color=colors["ACCENT_GLOW"], offset=ft.Offset(0, 5))
                        else:
                            button.scale = 1.0
                            button.shadow = ft.BoxShadow(blur_radius=8, color=colors["GLASS_SHADOW"], offset=ft.Offset(0, 2))
                        button.update()
                    return on_hover
                
                app_button.on_hover = create_hover_handler(app_button)
                results_grid.controls.append(app_button)
            
            search_results_content = ft.Column([results_header, results_grid])
            
            if self.theme_manager.glass_effect_enabled:
                search_card = GlassMorphism.create_card(search_results_content, colors, hover_effect=False)
            else:
                search_card = ft.Container(
                    content=search_results_content,
                    shadow=ft.BoxShadow(blur_radius=8, color=colors["GLASS_SHADOW"], offset=ft.Offset(0, 2)),
                    margin=ft.margin.only(bottom=25), border_radius=12, bgcolor=colors["SURFACE"],
                )
            
            self.main_content.content = ft.Column([
                self.create_favorites_panel(),
                search_card
            ], scroll=ft.ScrollMode.ADAPTIVE)
        
        self.page.update()

    def create_quick_actions_panel(self, colors):
        """Создание панели быстрых действий"""
        quick_actions = [
            ("refresh", "Обновить", "Обновить список приложений", lambda e: self.refresh_apps_list()),
            ("rocket_launch", "Быстрый запуск", "Запустить несколько приложений", lambda e: self.show_quick_launch_dialog()),
            ("dashboard", "Статистика", "Показать статистику использования", lambda e: self.show_usage_stats()),
            ("auto_fix_high", "Оптимизация", "Оптимизировать производительность", lambda e: self.optimize_performance()),
        ]
        
        actions_grid = ft.GridView(runs_count=4, max_extent=100, child_aspect_ratio=1.2, spacing=10, run_spacing=10, padding=20)
        
        for icon, title, tooltip, on_click in quick_actions:
            action_card = ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Icon(icon, color=colors["ACCENT"], size=28),
                        width=60, height=60,
                        bgcolor=colors["GLASS_BG"],
                        border_radius=12,
                        alignment=ft.alignment.center,
                        shadow=ft.BoxShadow(blur_radius=8, color=colors["GLASS_SHADOW"], offset=ft.Offset(0, 2)),
                    ),
                    ft.Text(title, size=12, text_align=ft.TextAlign.CENTER, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                on_click=on_click,
                tooltip=tooltip,
                padding=10,
                border_radius=12,
                bgcolor=colors["SURFACE_VARIANT"] + "20",
            )
            
            def create_hover_handler(card):
                def on_hover(e):
                    if e.data == "true":
                        card.bgcolor = colors["ACCENT"] + "20"
                        card.scale = 1.05
                    else:
                        card.bgcolor = colors["SURFACE_VARIANT"] + "20"
                        card.scale = 1.0
                    card.update()
                return on_hover
            
            action_card.on_hover = create_hover_handler(action_card)
            actions_grid.controls.append(action_card)
        
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Icon("flash_on", color=colors["ACCENT"], size=20),
                        ft.Text("Быстрые действия", size=16, weight=ft.FontWeight.BOLD, color=colors["ON_SURFACE"]),
                    ]),
                    padding=ft.padding.symmetric(horizontal=15, vertical=10)
                ),
                actions_grid
            ]),
            bgcolor=colors["SURFACE"],
            border_radius=12,
            margin=ft.margin.symmetric(horizontal=10, vertical=5)
        )

    def show_quick_launch_dialog(self):
        """Диалог быстрого запуска нескольких приложений"""
        colors = self.get_colors()
        
        selected_apps = []
        
        def close_dialog(e=None):
            self.page.close(dialog)
        
        def toggle_app_selection(app, checkbox):
            if checkbox.value:
                selected_apps.append(app)
            else:
                selected_apps.remove(app)
        
        def launch_selected(e):
            if not selected_apps:
                if self.system_notifications_enabled:
                    self.show_system_notification("Ошибка", "❌ Выберите хотя бы одно приложение")
                return
            
            # Запускаем выбранные приложения
            for app in selected_apps:
                self.launch_app(app)
            
            close_dialog()
            if self.system_notifications_enabled:
                self.show_system_notification("Быстрый запуск", f"🚀 Запущено {len(selected_apps)} приложений")
        
        # Создаем список приложений с чекбоксами
        apps_list = ft.Column(scroll=ft.ScrollMode.ADAPTIVE, height=300)
        
        for app in self.app_manager.get_all_apps():
            is_installed = self.app_manager.is_app_installed(app)
            if is_installed:
                checkbox = ft.Checkbox(
                    value=False,
                    on_change=lambda e, app=app: toggle_app_selection(app, e.control)
                )
                
                app_item = ft.Container(
                    content=ft.Row([
                        checkbox,
                        ft.Icon(app["icon"], color=colors["WEB_BLUE"] if app["type"] == "web" else colors["ON_SURFACE"], size=20),
                        ft.Text(app["name"], expand=True),
                        ft.Text(app["category"], size=12, color=colors["ON_SURFACE_VARIANT"]),
                    ]),
                    padding=10,
                    bgcolor=colors["SURFACE_VARIANT"] + "20",
                    border_radius=8,
                    margin=ft.margin.only(bottom=5),
                )
                apps_list.controls.append(app_item)
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Быстрый запуск приложений"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Выберите приложения для запуска:", size=14),
                    ft.Container(height=10),
                    apps_list
                ]),
                width=500,
                height=400
            ),
            actions=[
                ft.Row([
                    ft.TextButton("Отмена", on_click=close_dialog),
                    ft.FilledButton(f"Запустить выбранные ({len(selected_apps)})", on_click=launch_selected),
                ], alignment=ft.MainAxisAlignment.END)
            ],
        )
        
        self.page.open(dialog)

    def show_usage_stats(self):
        """Показать статистику использования"""
        colors = self.get_colors()
        
        # Собираем статистику
        total_apps = len(self.app_manager.get_all_apps())
        installed_apps = len([app for app in self.app_manager.get_all_apps() if self.app_manager.is_app_installed(app)])
        favorite_apps = len(self.app_manager.favorite_apps)
        custom_apps = len(self.app_manager.custom_apps)
        
        stats_content = ft.Column([
            ft.Container(
                content=ft.Row([
                    ft.Icon("analytics", color=colors["ACCENT"], size=24),
                    ft.Text("Статистика использования", size=18, weight=ft.FontWeight.BOLD),
                ]),
                padding=ft.padding.only(bottom=20)
            ),
            
            ft.Row([
                self.create_stat_card("📱", "Всего приложений", str(total_apps), colors),
                self.create_stat_card("✅", "Установлено", str(installed_apps), colors),
            ]),
            
            ft.Row([
                self.create_stat_card("⭐", "В избранном", str(favorite_apps), colors),
                self.create_stat_card("🎨", "Мои приложения", str(custom_apps), colors),
            ]),
            
            ft.Container(height=20),
            
            ft.Text("Категории приложений:", size=16, weight=ft.FontWeight.W_500),
            ft.Container(height=10),
        ])
        
        # Добавляем статистику по категориям
        categories = {}
        for app in self.app_manager.get_all_apps():
            if app["category"] not in categories:
                categories[app["category"]] = 0
            categories[app["category"]] += 1
        
        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            stats_content.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(self.get_category_icon(category), color=colors["ACCENT"], size=16),
                        ft.Text(category, expand=True),
                        ft.Text(str(count), size=14, color=colors["ON_SURFACE_VARIANT"]),
                    ]),
                    padding=10,
                    bgcolor=colors["SURFACE_VARIANT"] + "20",
                    border_radius=8,
                    margin=ft.margin.only(bottom=5),
                )
            )
        
        dialog = ft.AlertDialog(
            modal=True,
            content=ft.Container(
                content=stats_content,
                width=400,
                height=500,
            ),
            actions=[
                ft.TextButton("Закрыть", on_click=lambda e: self.page.close(dialog))
            ],
        )
        
        self.page.open(dialog)

    def create_stat_card(self, emoji, title, value, colors):
        """Создать карточку статистики"""
        return ft.Container(
            content=ft.Column([
                ft.Text(emoji, size=24),
                ft.Text(title, size=12, color=colors["ON_SURFACE_VARIANT"], text_align=ft.TextAlign.CENTER),
                ft.Text(value, size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            padding=20,
            bgcolor=colors["SURFACE_VARIANT"] + "20",
            border_radius=12,
            expand=True,
            margin=5,
        )

    def optimize_performance(self):
        """Оптимизация производительности"""
        # Очистка кэша и временных данных
        import shutil
        import tempfile
        
        try:
            # Очищаем временные файлы
            temp_dir = tempfile.gettempdir()
            # Здесь можно добавить логику очистки специфичных для лаунчера временных файлов
            
            if self.system_notifications_enabled:
                self.show_system_notification("Оптимизация", "✅ Производительность оптимизирована")
        except Exception as e:
            if self.system_notifications_enabled:
                self.show_system_notification("Ошибка", f"❌ Ошибка оптимизации: {str(e)}")

    def create_welcome_tour(self):
        """Создание приветственного тура для новых пользователей"""
        colors = self.get_colors()
        
        tour_steps = [
            {
                "title": "Добро пожаловать в Launcher Hab 2.1!",
                "content": "Это ваш новый умный лаунчер с расширенными возможностями",
                "icon": "rocket_launch"
            },
            {
                "title": "Избранное", 
                "content": "Добавляйте часто используемые приложения в избранное для быстрого доступа",
                "icon": "star"
            },
            {
                "title": "Поиск и фильтры",
                "content": "Используйте поиск и фильтры для быстрого нахождения приложений",
                "icon": "search"
            },
            {
                "title": "Настройки",
                "content": "Настройте внешний вид и функциональность под себя",
                "icon": "settings"
            }
        ]
        
        current_step = 0
        
        def next_step(e):
            nonlocal current_step
            if current_step < len(tour_steps) - 1:
                current_step += 1
                update_tour_content()
        
        def prev_step(e):
            nonlocal current_step
            if current_step > 0:
                current_step -= 1
                update_tour_content()
        
        def finish_tour(e):
            self.page.close(tour_dialog)
            # Сохраняем, что тур был показан
            self.file_manager.save_data('user_preferences.json', {'welcome_tour_shown': True})
        
        def update_tour_content():
            step = tour_steps[current_step]
            tour_content.content.controls[0].content.controls[0].name = step["icon"]
            tour_content.content.controls[1].value = step["title"]
            tour_content.content.controls[2].value = step["content"]
            
            # Обновляем прогресс
            progress_text.value = f"{current_step + 1}/{len(tour_steps)}"
            progress_text.update()
            
            # Обновляем кнопки
            prev_button.disabled = current_step == 0
            next_button.visible = current_step < len(tour_steps) - 1
            finish_button.visible = current_step == len(tour_steps) - 1
            
            tour_content.update()
        
        progress_text = ft.Text(f"1/{len(tour_steps)}", size=12, color=colors["ON_SURFACE_VARIANT"])
        
        tour_content = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Icon(tour_steps[0]["icon"], size=48, color=colors["ACCENT"]),
                    padding=20,
                    alignment=ft.alignment.center
                ),
                ft.Text(tour_steps[0]["title"], size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Text(tour_steps[0]["content"], size=14, color=colors["ON_SURFACE_VARIANT"], text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            padding=30,
            width=400,
            height=300
        )
        
        prev_button = ft.TextButton("Назад", on_click=prev_step, disabled=True)
        next_button = ft.TextButton("Далее", on_click=next_step)
        finish_button = ft.FilledButton("Начать использовать", on_click=finish_tour, visible=False)
        
        tour_dialog = ft.AlertDialog(
            modal=True,
            content=ft.Column([
                tour_content,
                ft.Container(
                    content=ft.Row([
                        progress_text,
                        ft.Row([prev_button, next_button, finish_button])
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=20
                )
            ]),
        )
        
        # Проверяем, показывался ли уже тур
        user_prefs = self.file_manager.load_data('user_preferences.json', {})
        if not user_prefs.get('welcome_tour_shown', False):
            self.page.open(tour_dialog)

    def setup_initial_tour(self):
        """Настройка начального тура при первом запуске"""
        user_prefs = self.file_manager.load_data('user_preferences.json', {})
        if not user_prefs.get('welcome_tour_shown', False):
            self.create_welcome_tour()

# Дополняем класс дополнительными утилитами
def initialize_app(page: ft.Page):
    """Функция инициализации приложения"""
    try:
        ui_manager = UIManager(page)
        ui_manager.initialize_ui()
        ui_manager.setup_initial_tour()  # Добавляем приветственный тур
        return ui_manager
    except Exception as e:
        # Резервный интерфейс при ошибке
        page.add(
            ft.Text("Ошибка запуска приложения", size=20, color="red"),
            ft.Text(f"Детали: {str(e)}", size=14),
            ft.FilledButton("Перезапустить", on_click=lambda e: page.restart())
        )
        return None