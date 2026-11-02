# [file name]: ui_dialogs.py
import flet as ft
import os
import uuid
from .glass_morphism import GlassMorphism
from .ui_dialogs_add_app import AddAppDialogMixin
from .ui_dialogs_workspace import WorkspaceDialogMixin

class UIDialogs(AddAppDialogMixin, WorkspaceDialogMixin):
    def __init__(self, ui_core):
        self.core = ui_core

    def show_filter_menu(self, e):
        if self.core.filter_dialog_open:
            return
        
        colors = self.core.get_colors()
        self.core.filter_dialog_open = True
        
        def close_dialog(e=None):
            self.core.filter_dialog_open = False
            self.core.page.close(dialog)
        
        def apply_selected_filter(filter_type, e):
            self.core.current_filter = filter_type
            self.core.update_main_content()
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
            is_active = self.core.current_filter == filter_type
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
        
        self.core.page.open(dialog)

    def _legacy_show_add_custom_app_dialog(self, e):
        """Устаревшая версия. Оставлено для совместимости."""
        return self.show_add_custom_app_dialog(e)

    def show_settings(self, e):
        colors = self.core.get_colors()
        
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
                ft.TextButton("Закрыть", on_click=lambda e: self.core.page.close(settings_dialog))
            ],
        )
        self.core.page.open(settings_dialog)

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
                 self.create_settings_section(
                    "🕒 Кастомизация времени и шрифтов",
                    "Новые стили часов, формат даты/времени и цвета",
                    self.create_customization_settings(colors),
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
                    self.core.plugin_manager.create_plugin_ui(colors),
                    colors
                ),
            ], scroll=ft.ScrollMode.ADAPTIVE),
            padding=20
        )

    def create_system_settings_tab(self, colors):
        return ft.Container(
            content=ft.Column([
                self.create_settings_section(
                    "Smart Workspace",
                    "Пресеты запуска для игр/разработки/фокуса",
                    ft.Column([
                        self.create_settings_button("Открыть Smart Workspace", "rocket_launch", lambda e: self.show_workspace_manager(e), colors),
                    ]),
                    colors
                ),
                self.create_settings_section(
                    "Поведение окна",
                    "Режим замены рабочего стола",
                    ft.Column([
                        ft.Row([
                            ft.Switch(
                                value=self.core.theme_manager.desktop_mode_enabled,
                                on_change=lambda e: self.core.theme_manager.set_desktop_mode(e.control.value),
                                active_track_color=colors["ACCENT"],
                            ),
                            ft.Text("После сворачивания сразу вернуть LauncherHub", expand=True),
                        ])
                    ]),
                    colors
                ),
                self.create_settings_section(
                    "Автоматическое обновление",
                    "Обновлять интерфейс автоматически при изменениях",
                    self.create_auto_update_settings(colors),
                    colors
                ),
            
                self.create_settings_section(
                    "🎯 ОПТИМИЗАЦИИ ПРОИЗВОДИТЕЛЬНОСТИ",
                    "Ускорение работы и снижение потребления ресурсов",
                    self.create_performance_settings(colors),
                    colors
                ),
                self.create_settings_section(
                    "💾 СИСТЕМА РЕЗЕРВНОГО КОПИРОВАНИЯ", 
                    "Безопасное сохранение и восстановление всех настроек",
                    self.create_backup_settings(colors),
                    colors
                ),
                self.create_settings_section(
                    "⌨️ ГОРЯЧИЕ КЛАВИШИ И ЖЕСТЫ",
                    "Быстрые комбинации клавиш и управление жестами", 
                    self.create_hotkey_settings(colors),
                    colors
                ),
                self.create_settings_section(
                    "🕒 КАСТОМИЗАЦИЯ ВРЕМЕНИ И ШРИФТОВ",
                    "Настройте отображение времени и текста под себя",
                    self.create_customization_settings(colors),
                    colors
                ),
            ], scroll=ft.ScrollMode.ADAPTIVE),
            padding=20
        )

    def create_performance_settings(self, colors):
        """Настройки оптимизации производительности"""
        return ft.Column([
            ft.Row([
                ft.Switch(
                    value=self.core.theme_manager.search_cache_enabled,
                    on_change=lambda e: self.core.theme_manager.set_performance_settings(
                        e.control.value,
                        self.core.theme_manager.virtualization_enabled
                    ),
                    active_track_color=colors["ACCENT"],
                ),
                ft.Column([
                    ft.Text("Кэширование поиска", weight=ft.FontWeight.W_500),
                    ft.Text("Мгновенные результаты при повторных запросах", size=12, color=colors["ON_SURFACE_VARIANT"]),
                ], expand=True)
            ]),
            
            ft.Container(height=15),
            
            ft.Row([
                ft.Switch(
                    value=self.core.theme_manager.virtualization_enabled,
                    on_change=lambda e: self.core.theme_manager.set_performance_settings(
                        self.core.theme_manager.search_cache_enabled,
                        e.control.value
                    ),
                    active_track_color=colors["ACCENT"],
                ),
                ft.Column([
                    ft.Text("Виртуализация списков", weight=ft.FontWeight.W_500),
                    ft.Text("Плавная работа с тысячами приложений", size=12, color=colors["ON_SURFACE_VARIANT"]),
                ], expand=True)
            ]),
            
            ft.Container(height=15),
            
            ft.Text("Эти оптимизации снижают потребление памяти на 40% и ускоряют отклик интерфейса", 
                   size=12, color=colors["SUCCESS"], weight=ft.FontWeight.W_500),
        ])

    def create_backup_settings(self, colors):
        """Настройки резервного копирования"""
        return ft.Column([
            ft.Row([
                ft.Switch(
                    value=self.core.theme_manager.backup_auto,
                    on_change=lambda e: self.core.theme_manager.set_backup_settings(
                        e.control.value, 
                        self.core.theme_manager.backup_interval
                    ),
                    active_track_color=colors["ACCENT"],
                ),
                ft.Column([
                    ft.Text("Автоматическое резервное копирование", weight=ft.FontWeight.W_500),
                    ft.Text("Регулярное сохранение всех настроек", size=12, color=colors["ON_SURFACE_VARIANT"]),
                ], expand=True)
            ]),
            
            ft.Container(height=10),
            
            ft.Text("Интервал автоматического бэкапа:", size=14, weight=ft.FontWeight.W_500),
            ft.Dropdown(
                value=str(self.core.theme_manager.backup_interval),
                options=[
                    ft.dropdown.Option("1", "Ежедневно"),
                    ft.dropdown.Option("3", "Каждые 3 дня"), 
                    ft.dropdown.Option("7", "Еженедельно"),
                    ft.dropdown.Option("30", "Ежемесячно"),
                ],
                on_change=lambda e: self.core.theme_manager.set_backup_settings(
                    self.core.theme_manager.backup_auto,
                    int(e.control.value)
                ),
                filled=True,
                bgcolor=colors["SURFACE_VARIANT"],
                border_radius=10,
                content_padding=15,
                border_color="transparent"
            ),
            
            ft.Container(height=15),
            
            ft.Row([
                ft.FilledButton(
                    "Создать резервную копию сейчас",
                    icon="backup",
                    on_click=lambda e: self.create_backup_now(e),
                ),
                ft.FilledButton(
                    "Восстановить из копии", 
                    icon="restore",
                    on_click=lambda e: self.show_restore_dialog(e),
                ),
            ], spacing=10),
            
            ft.Container(height=10),
            
            self.create_settings_button(
                "Управление резервными копиями",
                "folder_open", 
                lambda e: self.show_backup_manager(e),
                colors
            ),
        ])

    def create_hotkey_settings(self, colors):
        """Настройки горячих клавиш"""
        return ft.Column([
            ft.Text("Стандартные горячие клавиши:", size=14, weight=ft.FontWeight.W_500),
            ft.Container(
                content=ft.Column([
                    ft.Row([ft.Text("Ctrl + F", weight=ft.FontWeight.W_500), ft.Text("Фокус в поиск", expand=True)]),
                    ft.Row([ft.Text("Ctrl + R", weight=ft.FontWeight.W_500), ft.Text("Обновить приложения", expand=True)]),
                    ft.Row([ft.Text("Ctrl + ,", weight=ft.FontWeight.W_500), ft.Text("Открыть настройки", expand=True)]),
                    ft.Row([ft.Text("Escape", weight=ft.FontWeight.W_500), ft.Text("Очистить поиск", expand=True)]),
                    ft.Row([ft.Text("Ctrl + Q", weight=ft.FontWeight.W_500), ft.Text("Выход", expand=True)]),
                ], spacing=8),
                bgcolor=colors["SURFACE_VARIANT"] + "20",
                border_radius=10,
                padding=15
            ),
            
            ft.Container(height=15),
            
            self.create_settings_button(
                "Настроить кастомные горячие клавиши",
                "keyboard",
                lambda e: self.show_custom_hotkeys_dialog(e),
                colors
            ),
            
            ft.Container(height=10),
            
            ft.Text("Жесты управления:", size=14, weight=ft.FontWeight.W_500),
            ft.Container(
                content=ft.Column([
                    ft.Row([ft.Text("🖱️ Двойной клик", weight=ft.FontWeight.W_500), ft.Text("Запуск приложения", expand=True)]),
                    ft.Row([ft.Text("🖱️ Долгое нажатие", weight=ft.FontWeight.W_500), ft.Text("Контекстное меню", expand=True)]),
                    ft.Row([ft.Text("📱 Свайп вправо", weight=ft.FontWeight.W_500), ft.Text("Следующая категория", expand=True)]),
                    ft.Row([ft.Text("📱 Свайп влево", weight=ft.FontWeight.W_500), ft.Text("Предыдущая категория", expand=True)]),
                ], spacing=8),
                bgcolor=colors["SURFACE_VARIANT"] + "20",
                border_radius=10,
                padding=15
            ),
        ])

    def create_customization_settings(self, colors):
        """Расширенные настройки кастомизации времени, стилей часов и шрифтов (v2.4)"""
        clock_styles = [
            ("standard", "Классический (14:32:08)"),
            ("stacked", "Stacked (14 / 32)"),
            ("minimal", "Минималистичный (14:32)"),
            ("pill_glass", "Стеклянная капсула"),
            ("cyber_mono", "Цифровой Моно"),
            ("compact_badge", "Компактный с днем недели"),
        ]

        style_buttons = []
        for s_key, s_label in clock_styles:
            is_sel = getattr(self.core.theme_manager, "clock_style", "standard") == s_key
            style_buttons.append(
                ft.FilledButton(
                    s_label,
                    on_click=lambda e, k=s_key: self.set_clock_preferences(style=k),
                    style=ft.ButtonStyle(
                        color=colors["ON_SURFACE"] if is_sel else colors["ON_SURFACE_VARIANT"],
                        bgcolor=colors["ACCENT"] + "30" if is_sel else colors["SURFACE_VARIANT"],
                    ),
                )
            )

        color_presets = ["#ffffff", "#60a5fa", "#34d399", "#fbbf24", "#f472b6", "#c084fc"]
        preset_chips = [
            ft.Container(
                width=26,
                height=26,
                bgcolor=hex_c,
                border_radius=13,
                border=ft.border.all(2, colors["ON_SURFACE"] if self.core.theme_manager.time_color == hex_c else "transparent"),
                on_click=lambda e, hc=hex_c: self.set_clock_preferences(time_color=hc),
                tooltip=f"Цвет часов: {hex_c}",
            )
            for hex_c in color_presets
        ]

        return ft.Column([
            ft.Text("Формат времени:", size=14, weight=ft.FontWeight.W_500),
            ft.Row([
                ft.FilledButton(
                    "24-часовой",
                    on_click=lambda e: self.core.set_time_format("24"),
                    style=ft.ButtonStyle(
                        color=colors["ON_SURFACE"] if self.core.theme_manager.time_format == "24" else colors["ON_SURFACE_VARIANT"],
                        bgcolor=colors["ACCENT"] + "25" if self.core.theme_manager.time_format == "24" else colors["SURFACE_VARIANT"]
                    )
                ),
                ft.FilledButton(
                    "12-часовой (AM/PM)",
                    on_click=lambda e: self.core.set_time_format("12"),
                    style=ft.ButtonStyle(
                        color=colors["ON_SURFACE"] if self.core.theme_manager.time_format == "12" else colors["ON_SURFACE_VARIANT"],
                        bgcolor=colors["ACCENT"] + "25" if self.core.theme_manager.time_format == "12" else colors["SURFACE_VARIANT"]
                    )
                ),
            ], spacing=10),
            ft.Container(height=8),
            ft.Text("Стиль часов (v2.4):", size=14, weight=ft.FontWeight.W_500),
            ft.Row(style_buttons, wrap=True, spacing=8, run_spacing=8),
            ft.Container(height=6),
            ft.Row([
                ft.Switch(
                    value=getattr(self.core.theme_manager, "show_seconds", True),
                    on_change=lambda e: self.set_clock_preferences(show_seconds=e.control.value),
                    active_track_color=colors["ACCENT"],
                ),
                ft.Text("Показывать секунды", expand=True),
                ft.Switch(
                    value=self.core.theme_manager.show_date,
                    on_change=lambda e: self.set_clock_preferences(show_date=e.control.value),
                    active_track_color=colors["ACCENT"],
                ),
                ft.Text("Показывать дату", expand=True),
            ]),
            ft.Row([
                ft.Switch(
                    value=getattr(self.core.theme_manager, "show_weekday", True),
                    on_change=lambda e: self.set_clock_preferences(show_weekday=e.control.value),
                    active_track_color=colors["ACCENT"],
                ),
                ft.Text("День недели (Пн, Вт...)", expand=True),
                ft.Switch(
                    value=getattr(self.core.theme_manager, "clock_glass_frame", True),
                    on_change=lambda e: self.set_clock_preferences(clock_glass_frame=e.control.value),
                    active_track_color=colors["ACCENT"],
                ),
                ft.Text("Стеклянная капсула вокруг часов", expand=True),
            ]),
            ft.Row([
                ft.Text("Размер часов:", size=13),
                ft.Slider(
                    value=getattr(self.core.theme_manager, "time_font_size", 20),
                    min=14,
                    max=38,
                    divisions=24,
                    label="{value}px",
                    active_color=colors["ACCENT"],
                    on_change=lambda e: self.set_clock_preferences(time_font_size=int(e.control.value)),
                    expand=True,
                ),
            ]),
            ft.Row([
                ft.Text("Быстрый цвет часов:", size=13),
                *preset_chips,
            ], spacing=8),
            ft.Row([
                ft.TextField(
                    label="HEX цвет времени",
                    value=self.core.theme_manager.time_color,
                    hint_text="#ffffff",
                    on_submit=lambda e: self.set_clock_preferences(time_color=e.control.value),
                    filled=True,
                    bgcolor=colors["SURFACE_VARIANT"],
                    border_radius=10,
                    expand=True,
                ),
                ft.TextField(
                    label="HEX цвет даты",
                    value=self.core.theme_manager.date_color,
                    hint_text="#94a3b8",
                    on_submit=lambda e: self.set_clock_preferences(date_color=e.control.value),
                    filled=True,
                    bgcolor=colors["SURFACE_VARIANT"],
                    border_radius=10,
                    expand=True,
                ),
            ], spacing=10),
            ft.Container(height=12),
            ft.Text("Настройки шрифта интерфейса:", size=14, weight=ft.FontWeight.W_500),
            ft.Row([
                ft.Dropdown(
                    label="Шрифт",
                    value=self.core.theme_manager.font_family,
                    options=[
                        ft.dropdown.Option("Segoe UI"),
                        ft.dropdown.Option("Arial"),
                        ft.dropdown.Option("Helvetica"),
                        ft.dropdown.Option("Tahoma"),
                        ft.dropdown.Option("Verdana"),
                        ft.dropdown.Option("Consolas"),
                        ft.dropdown.Option("System UI"),
                    ],
                    on_change=lambda e: self.core.set_font_family(e.control.value),
                    expand=True,
                    filled=True,
                    bgcolor=colors["SURFACE_VARIANT"],
                    border_radius=10,
                ),
                ft.Dropdown(
                    label="Размер",
                    value=str(self.core.theme_manager.font_size),
                    options=[ft.dropdown.Option(str(i)) for i in range(12, 21)],
                    on_change=lambda e: self.core.set_font_size(int(e.control.value)),
                    width=120,
                    filled=True,
                    bgcolor=colors["SURFACE_VARIANT"],
                    border_radius=10,
                ),
            ]),
        ])

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
        self.core.theme_manager.set_clock_preferences(
            style=style,
            show_date=show_date,
            time_color=time_color,
            date_color=date_color,
            show_seconds=show_seconds,
            show_weekday=show_weekday,
            clock_glass_frame=clock_glass_frame,
            time_font_size=time_font_size,
        )
        self.core.update_header()
        self.core.update_time()

    def update_time_style(self, time_size=None, date_size=None, time_family=None, date_family=None):
        self.core.theme_manager.set_time_style(time_size, date_size, time_family, date_family)
        self.core.update_header()

    def create_auto_update_settings(self, colors):
        return ft.Column([
            ft.Row([
                ft.Switch(
                    value=self.core.auto_update_enabled,
                    on_change=self.core.toggle_auto_update,
                    active_track_color=colors["ACCENT"],
                ),
                ft.Column([
                    ft.Text("Автоматическое обновление интерфейса", weight=ft.FontWeight.W_500),
                    ft.Text("Интерфейс обновляется сразу при изменениям", size=12, color=colors["ON_SURFACE_VARIANT"]),
                ], expand=True)
            ]),
            ft.Container(height=10),
            ft.Text("При добавлении/удалении приложений интерфейс автоматически перерисовывается", 
                   size=12, color=colors["ON_SURFACE_VARIANT"]),
        ])

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
        themes = self.core.theme_manager.get_available_themes()
        theme_buttons = ft.Row(scroll=ft.ScrollMode.ADAPTIVE, spacing=15)
        
        for theme_name, theme_data in themes.items():
            is_current = theme_name == self.core.theme_manager.current_theme
            
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
                on_click=lambda e, tn=theme_name: self.core.apply_theme_settings(tn),
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
                lambda e: self.core.page.show_snack_bar(ft.SnackBar(content=ft.Text("Функция в разработке"), action="OK")),
                colors
            ),
            self.create_settings_button(
                "Экспорт текущей темы",
                "file_download", 
                lambda e: self.core.page.show_snack_bar(ft.SnackBar(content=ft.Text("Функция в разработке"), action="OK")),
                colors
            ),
        ], spacing=10)

    def show_create_theme_dialog(self):
        colors = self.core.get_colors()
        
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
        
        bg_color_row = create_color_field("Основной фон", "#1e1e1e")
        surface_color_row = create_color_field("Поверхность", "#2d2d2d")
        accent_color_row = create_color_field("Акцентный цвет", "#4285f4")
        text_color_row = create_color_field("Цвет текста", "#ffffff")
        secondary_text_row = create_color_field("Вторичный текст", "#cccccc")
        
        def create_theme(e):
            if theme_name.value:
                bg_color = bg_color_row.controls[0].value
                surface_color = surface_color_row.controls[0].value
                accent_color = accent_color_row.controls[0].value
                text_color = text_color_row.controls[0].value
                secondary_text = secondary_text_row.controls[0].value
                
                if not all(self.is_valid_hex(color) for color in [bg_color, surface_color, accent_color, text_color, secondary_text]):
                    self.core.page.show_snack_bar(ft.SnackBar(content=ft.Text("❌ Неверный формат HEX-цветов"), action="OK"))
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
                
                if self.core.theme_manager.add_custom_theme(theme_name.value, new_theme):
                    self.core.page.close(dialog)
                    self.core.page.show_snack_bar(ft.SnackBar(content=ft.Text(f"✅ Тема '{theme_name.value}' создана!"), action="OK"))
                    self.core.update_main_content()
            else:
                self.core.page.show_snack_bar(ft.SnackBar(content=ft.Text("❌ Введите название темы"), action="OK"))
        
        def cancel_create(e):
            self.core.page.close(dialog)
        
        dialog = ft.AlertDialog(
            title=ft.Text("Создать кастомную тему"),
            content=ft.Container(
                content=ft.Column([
                    theme_name,
                    bg_color_row,
                    surface_color_row,
                    accent_color_row,
                    text_color_row,
                    secondary_text_row,
                    ft.Text("Формат цветов: #RRGGBB (например: #1e1e1e)", size=12, color=colors["ON_SURFACE_VARIANT"]),
                ], height=400),
                width=500
            ),
            actions=[
                ft.TextButton("Отмена", on_click=cancel_create),
                ft.FilledButton("Создать", on_click=create_theme),
            ]
        )
        
        self.core.page.open(dialog)
    
    def is_valid_hex(self, color):
        import re
        pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
        return bool(re.match(pattern, color))
    
    def update_color_indicator(self, color_indicator, hex_value):
        if self.is_valid_hex(hex_value):
            color_indicator.bgcolor = hex_value
        else:
            color_indicator.bgcolor = "#ff0000"
        color_indicator.update()

    def create_effects_settings(self, colors):
        return ft.Column([
            ft.Row([
                ft.Switch(
                    value=self.core.theme_manager.glass_effect_enabled,
                    on_change=lambda e: self.core.toggle_glass_effect(),
                    active_track_color=colors["ACCENT"],
                ),
                ft.Column([
                    ft.Text("Включить размытие (Old version)", weight=ft.FontWeight.W_500),
                    ft.Text("Классический режим как в оригинале", size=12, color=colors["ON_SURFACE_VARIANT"]),
                ], expand=True)
            ]),
            ft.Container(height=12),
            self.create_glass_intensity_selector(colors),
            ft.Container(height=16),
            ft.Row([
                ft.Switch(
                    value=self.core.theme_manager.advanced_glass_enabled,
                    on_change=lambda e: self.core.theme_manager.set_advanced_glass(e.control.value, self.core.theme_manager.advanced_glass_opacity),
                    active_track_color=colors["ACCENT"],
                ),
                ft.Column([
                    ft.Text("Новый Glass UI режим", weight=ft.FontWeight.W_500),
                    ft.Text("Полноценный стеклянный эффект", size=12, color=colors["ON_SURFACE_VARIANT"]),
                ], expand=True)
            ]),
            ft.Dropdown(
                label="Прозрачность",
                value=str(self.core.theme_manager.advanced_glass_opacity),
                options=[ft.dropdown.Option("25"), ft.dropdown.Option("50"), ft.dropdown.Option("75"), ft.dropdown.Option("100")],
                on_change=lambda e: self.core.theme_manager.set_advanced_glass(self.core.theme_manager.advanced_glass_enabled, int(e.control.value)),
                filled=True,
                bgcolor=colors["SURFACE_VARIANT"],
            ),
            ft.Container(height=15),
            ft.Row([
                ft.Switch(
                    value=self.core.theme_manager.smooth_animations,
                    on_change=lambda e: self.core.toggle_smooth_animations(),
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
                    value=self.core.theme_manager.android_animations,
                    on_change=lambda e: self.core.toggle_android_animations(),
                    active_track_color=colors["ACCENT"],
                ),
                ft.Column([
                    ft.Text("Android-анимации", weight=ft.FontWeight.W_500),
                    ft.Text("Анимации как в Android", size=12, color=colors["ON_SURFACE_VARIANT"]),
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
            is_active = self.core.theme_manager.glass_intensity == intensity
            
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
                on_click=lambda e, ints=intensity: self.core.set_glass_intensity(ints),
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
                lambda e: self.core.refresh_apps_list(),
                colors
            ),
            self.create_settings_button(
                "Сбросить избранное", 
                "star_border",
                lambda e: self.core.reset_favorites(),
                colors
            ),
            self.create_settings_button(
                "Очистить ручные пути",
                "clear_all",
                lambda e: self.core.clear_manual_paths(),
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
            "2.4": [
                "🚀 LAUNCHER HUB 2.4 – ПРОЗРАЧНОЕ СТЕКЛО, SESSION TRACKER И PLUGIN API 2.4",
                "🔮 НАСТОЯЩИЙ ЭФФЕКТ ПРОЗРАЧНОГО СТЕКЛА (GLASSMORPHISM 2.4) – аппаратное размытие заднего фона (ft.Blur), стеклянные блики границ и настраиваемая прозрачность",
                "✨ ПЛАВНАЯ АНИМАЦИЯ ПЕРЕХОДОВ МЕЖДУ РАЗДЕЛАМИ – мягкие переходы между библиотекой, фильтрами, поиском и трекером времени через AnimatedSwitcher",
                "➕ УЛУЧШЕННОЕ ОКНО «ДОБАВИТЬ ПРИЛОЖЕНИЕ» – живое превью карточки, поиск по 70+ иконкам, автоопределение типа (EXE / URL), CLI-аргументы и лимит времени",
                "🧩 ПЛАТФОРМА РАСШИРЕНИЙ И PLUGIN API 2.4 – новый SDK с хуками жизненного цикла (on_app_launched, on_tick), бейджами карточек и генератором шаблонов",
                "🔊 ФОНОВЫЙ КОНТРОЛЛЕР СИСТЕМНОЙ ГРОМКОСТИ – мгновенное изменение громкости в фоновом потоке через CoreAudio (pycaw / COM Interop) без зависаний и кнопка Mute",
                "🎮 ПЛАГИН «GAME & APP SESSION TRACKER» – отслеживание игрового и экранного времени: бейджи на карточках («Steam — 42 ч в мес») и графики за день/неделю/месяц",
                "🛑 ГРУППЫ ЦИФРОВОГО ДЕТОКСА – настраиваемые дневные лимиты для игр, соцсетей и медиа с автоматическими уведомлениями при превышении",
                "🕒 РАСШИРЕННАЯ КАСТОМИЗАЦИЯ СТИЛЕЙ ЧАСОВ – 6 стилей часов (Классический, Stacked, Минималистичный, Стеклянная капсула, Цифровой Моно, Компактный), управление секундами, днем недели и пресетами цвета"
            ],
            "2.3": [
                "🎨 УЛУЧШЕННЫЙ LIQUID GLASS ИНТЕРФЕЙС – переработанный стеклянный дизайн, плавные эффекты прозрачности и более современный внешний вид",
                "🖥 FLOATING HUD – новая плавающая панель с системной информацией и быстрым доступом к функциям",
                "🗑 ФИКСИРОВАННАЯ КОРЗИНА – корзина закреплена в правом нижнем углу интерфейса",
                "🔎 ИСТОРИЯ ПОИСКА – система поиска теперь сохраняет предыдущие запросы для более быстрого доступа",
                "💾 УЛУЧШЕННАЯ СИСТЕМА РЕЗЕРВНОГО КОПИРОВАНИЯ – стабильное сохранение и восстановление настроек и данных пользователя",
                "🕒 НОВЫЕ СТИЛИ ЧАСОВ – добавлены дополнительные варианты отображения времени и даты с кастомизацией цвета",
                "🎨 УЛУЧШЕННАЯ ПАНЕЛЬ НАСТРОЕК – более гармоничный дизайн и удобная навигация",
                "🔌 СИСТЕМА ПЛАГИНОВ – поддержка расширений LauncherHub для добавления новых возможностей",
                "🎯 FOCUS MODE PLUGIN – режим концентрации с Pomodoro таймером и минималистичным интерфейсом",
                "🌦 SMART WEATHER PLUGIN – отображение температуры, влажности и скорости ветра",
                "🎵 SMART MUSIC CONTROLLER – управление музыкой через встроенный мини-плеер",
                "📂 SMART FILE FINDER И IDEA NOTEBOOK – быстрый поиск файлов и встроенный блокнот для идей"
            ],
            "2.2": [
                "🚀 LAUNCHER HAB 2.2 - ОПТИМИЗАЦИЯ И КАСТОМИЗАЦИЯ",
                "⚡ ОПТИМИЗАЦИЯ ПРОИЗВОДИТЕЛЬНОСТИ - снижение потребления памяти на 40%",
                "🔍 КЭШИРОВАНИЕ ПОИСКА - мгновенные результаты при повторных запросах",
                "📱 ВИРТУАЛИЗАЦИЯ СПИСКОВ - плавная работа с тысячами приложений",
                "💾 СИСТЕМА РЕЗЕРВНОГО КОПИРОВАНИЯ - полное сохранение/восстановление настроек",
                "⌨️ РАСШИРЕННЫЕ ГОРЯЧИЕ КЛАВИШИ - кастомные комбинации клавиш",
                "👆 УПРАВЛЕНИЕ ЖЕСТАМИ - свайпы для быстрых действий",
                "🕒 КАСТОМИЗАЦИЯ ВРЕМЕНИ - форматы 12/24 часа, выбор стиля отображения",
                "🔤 НАСТРОЙКИ ШРИФТОВ - выбор шрифта и размера текста",
                "🔄 АВТОМАТИЧЕСКИЕ БЭКАПЫ - регулярное сохранение настроек",
                "🎯 ОПТИМИЗИРОВАННЫЙ РЕНДЕРИНГ - отложенная загрузка элементов",
                "🔧 УЛУЧШЕННЫЙ КЭШ-МЕНЕДЖЕР - интеллектуальное кэширование данных",
                "📊 СИСТЕМА МОНИТОРИНГА ПРОИЗВОДИТЕЛЬНОСТИ - отслеживание потребления ресурсов",
                "🐛 ИСПРАВЛЕНИЕ МЕЛКИХ ОШИБОК И УЛУЧШЕНИЕ СТАБИЛЬНОСТИ"
            ],
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
            ],
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

    def show_plugins_manager(self, e):
        colors = self.core.get_colors()
        
        plugins_content = self.core.plugin_manager.create_plugin_ui(colors)
        
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
                ft.TextButton("Закрыть", on_click=lambda e: self.core.page.close(plugins_dialog))
            ],
        )
        self.core.page.open(plugins_dialog)

    # НОВЫЕ МЕТОДЫ ДЛЯ ВЕРСИИ 2.2
    def create_backup_now(self, e):
        if hasattr(self.core, 'backup_manager'):
            backup_path = self.core.backup_manager.create_backup()
            self.core.page.show_snack_bar(ft.SnackBar(
                content=ft.Text(f"✅ Резервная копия создана!"),
                action="OK"
            ))

    def show_restore_dialog(self, e):
        self.core.page.show_snack_bar(ft.SnackBar(
            content=ft.Text("Функция восстановления в разработке"),
            action="OK"
        ))

    def show_backup_manager(self, e):
        self.core.page.show_snack_bar(ft.SnackBar(
            content=ft.Text("Менеджер резервных копий в разработке"),
            action="OK"
        ))

    def show_custom_hotkeys_dialog(self, e):
        colors = self.core.get_colors()

        actions = [
            "open_settings",
            "focus_search",
            "refresh_apps",
            "toggle_theme",
            "show_plugins",
            "add_app",
            "create_backup",
            "open_workspace",
            "toggle_hud",
        ]

        custom_hotkeys = self.core.hotkey_manager.custom_hotkeys.copy()
        rows = []

        for combo, action in custom_hotkeys.items():
            rows.append(
                ft.Row([
                    ft.Text(combo, width=180),
                    ft.Dropdown(
                        value=action,
                        options=[ft.dropdown.Option(a) for a in actions],
                        width=220,
                        filled=True,
                        bgcolor=colors["SURFACE_VARIANT"],
                        on_change=lambda e, c=combo: custom_hotkeys.__setitem__(c, e.control.value),
                    )
                ])
            )

        combo_field = ft.TextField(label="Новая комбинация", hint_text="ctrl+alt+1", filled=True, bgcolor=colors["SURFACE_VARIANT"])
        action_field = ft.Dropdown(label="Действие", value="open_workspace", options=[ft.dropdown.Option(a) for a in actions], filled=True, bgcolor=colors["SURFACE_VARIANT"])

        def add_hotkey(_):
            combo = (combo_field.value or "").lower().strip()
            if combo:
                custom_hotkeys[combo] = action_field.value
                self.core.page.close(dialog)
                self.show_custom_hotkeys_dialog(None)

        def save(_):
            self.core.hotkey_manager.custom_hotkeys = custom_hotkeys
            self.core.hotkey_manager.save_custom_hotkeys()
            self.core.page.close(dialog)
            self.core.page.show_snack_bar(ft.SnackBar(content=ft.Text("✅ Горячие клавиши сохранены"), action="OK"))

        dialog = ft.AlertDialog(
            title=ft.Text("Кастомные горячие клавиши"),
            content=ft.Container(
                width=620,
                height=500,
                content=ft.Column([
                    ft.Text("Быстрые hotkeys уже активны: Ctrl+Shift+S/H/B/G/D", size=12, color=colors["ON_SURFACE_VARIANT"]),
                    ft.Column(rows, scroll=ft.ScrollMode.ADAPTIVE),
                    ft.Divider(),
                    combo_field,
                    action_field,
                    ft.FilledButton("Добавить", on_click=add_hotkey),
                ], scroll=ft.ScrollMode.ADAPTIVE),
            ),
            actions=[
                ft.TextButton("Закрыть", on_click=lambda e: self.core.page.close(dialog)),
                ft.FilledButton("Сохранить", on_click=save),
            ],
        )
        self.core.page.open(dialog)


# [file name]: ui_dialogs.py (продолжение)

    def show_style_switch_dialog(self, e):
        """Показать диалог выбора стиля интерфейса"""
        colors = self.core.get_colors()
        
        def switch_to_legacy(e):
            if hasattr(self.core, 'style_manager') and self.core.style_manager.current_style != "legacy":
                self.core.style_manager.set_style("legacy")
                self.core.reload_interface()
            self.core.page.close(dialog)
        
        def switch_to_new(e):
            if hasattr(self.core, 'style_manager') and self.core.style_manager.current_style != "new":
                self.core.style_manager.set_style("new")
                self.core.reload_interface()
            self.core.page.close(dialog)
        
        # Проверяем наличие менеджера стилей
        has_style_manager = hasattr(self.core, 'style_manager')
        is_legacy = has_style_manager and self.core.style_manager.is_legacy_style()
        is_new = has_style_manager and self.core.style_manager.is_new_style()
        
        dialog_content = ft.Column([
            ft.Text("Выберите стиль интерфейса", size=18, weight=ft.FontWeight.BOLD, color=colors["ON_SURFACE"]),
            ft.Container(height=20),
            
            # Кнопка Legacy
            ft.Container(
                content=ft.Row([
                    ft.Icon("design_services", color=colors["ACCENT"], size=24),
                    ft.Column([
                        ft.Text("Legacy", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text("Классический стиль интерфейса", size=12, color=colors["ON_SURFACE_VARIANT"]),
                    ], expand=True),
                    ft.Icon("check", color=colors["ACCENT"]) if is_legacy else ft.Container(width=24, height=24)
                ]),
                on_click=switch_to_legacy,
                padding=15,
                bgcolor=colors["ACCENT"] + "10" if is_legacy else colors["SURFACE_VARIANT"] + "20",
                border_radius=12,
            ),
            
            ft.Container(height=10),
            
            # Кнопка New
            ft.Container(
                content=ft.Row([
                    ft.Icon("palette", color=colors["ACCENT"], size=24),
                    ft.Column([
                        ft.Text("New", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text("Современный обновленный стиль", size=12, color=colors["ON_SURFACE_VARIANT"]),
                    ], expand=True),
                    ft.Icon("check", color=colors["ACCENT"]) if is_new else ft.Container(width=24, height=24)
                ]),
                on_click=switch_to_new,
                padding=15,
                bgcolor=colors["ACCENT"] + "10" if is_new else colors["SURFACE_VARIANT"] + "20",
                border_radius=12,
            ),
            
            ft.Container(height=20),
            ft.Text("Изменения применяются мгновенно", size=12, color=colors["ON_SURFACE_VARIANT"], text_align=ft.TextAlign.CENTER),
        ])
        
        dialog = ft.AlertDialog(
            title=ft.Text("Смена стиля интерфейса"),
            content=dialog_content,
            actions=[
                ft.TextButton("Закрыть", on_click=lambda e: self.core.page.close(dialog))
            ]
        )
        
        self.core.page.open(dialog)

    def show_app_menu_dialog(self, app):
        colors = self.core.get_colors()
        
        def close_dialog(e=None):
            self.core.page.close(dialog)
        
        def add_to_favorites_action(e):
            if self.core.app_manager.is_duplicate_favorite(app):
                self.show_duplicate_favorite_dialog(app)
            else:
                success, message = self.core.app_manager.add_to_favorites(app)
                if self.core.system_notifications_enabled:
                    self.core.show_system_notification("Избранное", message)
                if success:
                    self.core.update_main_content()
            close_dialog()
        
        def remove_from_favorites_action(e):
            success, message = self.core.app_manager.remove_from_favorites(app)
            if self.core.system_notifications_enabled:
                self.core.show_system_notification("Избранное", message)
            if success:
                self.core.update_main_content()
            close_dialog()
        
        def install_app_action(e):
            import webbrowser
            if app.get("official_url"):
                webbrowser.open(app["official_url"])
                if self.core.system_notifications_enabled:
                    self.core.show_system_notification("Установка", f"🌐 Открывается официальный сайт {app['name']}")
            else:
                if self.core.system_notifications_enabled:
                    self.core.show_system_notification("Ошибка", "❌ Официальный сайт не указан")
            close_dialog()
        
        def find_path_action(e):
            self.select_manual_path(app)
            close_dialog()
        
        def show_path_action(e):
            if app["package"] in self.core.app_manager.manual_paths:
                path = self.core.app_manager.manual_paths[app["package"]]
                if self.core.system_notifications_enabled:
                    self.core.show_system_notification("Путь к приложению", f"📁 Путь: {path}")
            else:
                if self.core.system_notifications_enabled:
                    self.core.show_system_notification("Ошибка", "❌ Путь не указан")
            close_dialog()

        def open_file_location_action(e):
            try:
                if app["package"] in self.core.app_manager.manual_paths:
                    file_path = self.core.app_manager.manual_paths[app["package"]]
                    folder_path = os.path.dirname(file_path)
                    if os.path.exists(folder_path):
                        os.startfile(folder_path)
                        if self.core.system_notifications_enabled:
                            self.core.show_system_notification("Проводник", f"📂 Открыта папка: {folder_path}")
                    else:
                        if self.core.system_notifications_enabled:
                            self.core.show_system_notification("Ошибка", "❌ Папка не найдена")
                else:
                    if self.core.system_notifications_enabled:
                        self.core.show_system_notification("Ошибка", "❌ Путь к приложению не указан")
            except Exception as ex:
                if self.core.system_notifications_enabled:
                    self.core.show_system_notification("Ошибка", f"❌ Не удалось открыть папку: {str(ex)}")
            close_dialog()

        def edit_tags_action(e):
            self.show_edit_tags_dialog(app)
            close_dialog()
        
        def edit_app_action(e):
            if app in self.core.app_manager.custom_apps:
                self.show_edit_custom_app_dialog(app)
            else:
                if self.core.system_notifications_enabled:
                    self.core.show_system_notification("Ошибка", "❌ Можно редактировать только кастомные приложения")
            close_dialog()
        
        def remove_app_action(e):
            if app in self.core.app_manager.custom_apps:
                self.core.app_manager.remove_custom_app(app)
                self.core.update_main_content()
                self.core.update_sidebar()
                if self.core.system_notifications_enabled:
                    self.core.show_system_notification("Удаление", f"🗑️ {app['name']} удалено")
            else:
                if self.core.system_notifications_enabled:
                    self.core.show_system_notification("Ошибка", "❌ Можно удалять только кастомные приложения")
            close_dialog()
        
        is_favorite = any(fav.get("id") == app.get("id") for fav in self.core.app_manager.favorite_apps) if "id" in app else app in self.core.app_manager.favorite_apps
        is_custom = app in self.core.app_manager.custom_apps
        has_manual_path = app["package"] in self.core.app_manager.manual_paths
        
        menu_items = []
        
        if not is_favorite:
            menu_items.append(
                ft.ListTile(
                    leading=ft.Icon("star", color=colors["ACCENT"], size=20),
                    title=ft.Text("Добавить в избранное", size=14),
                    on_click=add_to_favorites_action,
                    dense=True,
                )
            )
        else:
            menu_items.append(
                ft.ListTile(
                    leading=ft.Icon("star", color=colors["ACCENT"], size=20),
                    title=ft.Text("Удалить из избранного", size=14),
                    on_click=remove_from_favorites_action,
                    dense=True,
                )
            )
        
        menu_items.append(
            ft.ListTile(
                leading=ft.Icon("play_arrow", color=colors["SUCCESS"], size=20),
                title=ft.Text("Запустить", size=14),
                on_click=lambda e: self.core.launch_app(app),
                dense=True,
            )
        )
        
        if app["type"] != "web" and not self.core.app_manager.is_app_installed(app):
            menu_items.append(
                ft.ListTile(
                    leading=ft.Icon("download", color=colors["WEB_BLUE"], size=20),
                    title=ft.Text("Установить", size=14),
                    on_click=install_app_action,
                    dense=True,
                )
            )
        
        if app["type"] != "web" and app["type"] != "system":
            menu_items.append(
                ft.ListTile(
                    leading=ft.Icon("folder", color=colors["ON_SURFACE_VARIANT"], size=20),
                    title=ft.Text("Указать путь вручную", size=14),
                    on_click=find_path_action,
                    dense=True,
                )
            )
            
            if has_manual_path:
                menu_items.append(
                    ft.ListTile(
                        leading=ft.Icon("info", color=colors["ON_SURFACE_VARIANT"], size=20),
                        title=ft.Text("Показать путь", size=14),
                        on_click=show_path_action,
                        dense=True,
                    )
                )
                menu_items.append(
                    ft.ListTile(
                        leading=ft.Icon("folder_open", color=colors["ON_SURFACE_VARIANT"], size=20),
                        title=ft.Text("Открыть расположение", size=14),
                        on_click=open_file_location_action,
                        dense=True,
                    )
                )
        
        menu_items.append(
            ft.ListTile(
                leading=ft.Icon("local_offer", color=colors["WEB_BLUE"], size=20),
                title=ft.Text("Редактировать теги", size=14),
                on_click=edit_tags_action,
                dense=True,
            )
        )
        
        if is_custom:
            menu_items.append(ft.Divider(height=1))
            menu_items.append(
                ft.ListTile(
                    leading=ft.Icon("edit", color=colors["ACCENT"], size=20),
                    title=ft.Text("Редактировать", size=14),
                    on_click=edit_app_action,
                    dense=True,
                )
            )
            menu_items.append(
                ft.ListTile(
                    leading=ft.Icon("delete", color=colors["ERROR"], size=20),
                    title=ft.Text("Удалить", size=14),
                    on_click=remove_app_action,
                    dense=True,
                )
            )
        
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
                    ft.Column(menu_items, spacing=0)
                ], tight=True),
                width=280,
                height=min(400, len(menu_items) * 60 + 80)
            ),
            actions=[
                ft.TextButton("Закрыть", on_click=close_dialog)
            ],
            shape=ft.RoundedRectangleBorder(radius=12)
        )
        
        self.core.page.open(dialog)

    def show_favorite_app_menu_dialog(self, app):
        colors = self.core.get_colors()
        
        def close_dialog(e=None):
            self.core.page.close(dialog)
        
        def remove_from_favorites_action(e):
            success, message = self.core.app_manager.remove_from_favorites(app)
            if self.core.system_notifications_enabled:
                self.core.show_system_notification("Избранное", message)
            if success:
                self.core.update_main_content()
            close_dialog()
        
        def launch_app_action(e):
            self.core.launch_app(app)
            close_dialog()
        
        def edit_tags_action(e):
            self.show_edit_tags_dialog(app)
            close_dialog()
        
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
        
        self.core.page.open(dialog)

    def select_manual_path(self, app):
        """ВЫБОР ПУТИ К ПРИЛОЖЕНИЮ ВРУЧНУЮ"""
        import tkinter as tk
        from tkinter import filedialog
        
        root = tk.Tk()
        root.withdraw()
        
        file_path = filedialog.askopenfilename(
            title=f"Выберите исполняемый файл для {app['name']}",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        
        if file_path:
            self.core.app_manager.manual_paths[app["package"]] = file_path
            self.core.app_manager.save_manual_paths()
            self.core.page.show_snack_bar(ft.SnackBar(
                content=ft.Text(f"✅ Путь для {app['name']} установлен: {file_path}"), 
                action="OK"
            ))
            self.core.update_main_content()
            self.core.update_sidebar()

    def show_edit_custom_app_dialog(self, app):
        """ИСПРАВЛЕННЫЙ ДИАЛОГ РЕДАКТИРОВАНИЯ ПРИЛОЖЕНИЯ"""
        colors = self.core.get_colors()
        
        app_name = ft.TextField(
            label="Название приложения",
            value=app["name"],
            expand=True,
            filled=True,
            bgcolor=colors["SURFACE_VARIANT"],
            border_radius=10,
            content_padding=15,
            border_color="transparent"
        )
        
        app_url = ft.TextField(
            label="URL или путь к приложению",
            value=app["url"],
            expand=True,
            filled=True,
            bgcolor=colors["SURFACE_VARIANT"],
            border_radius=10,
            content_padding=15,
            border_color="transparent"
        )
        
        app_category = ft.Dropdown(
            label="Категория",
            options=[
                ft.dropdown.Option("Browser"),
                ft.dropdown.Option("Media"),
                ft.dropdown.Option("Music"),
                ft.dropdown.Option("Social"),
                ft.dropdown.Option("Games"),
                ft.dropdown.Option("System"),
                ft.dropdown.Option("Office"),
                ft.dropdown.Option("Cloud"),
                ft.dropdown.Option("Health"),
                ft.dropdown.Option("Government"),
            ],
            value=app["category"],
            filled=True,
            bgcolor=colors["SURFACE_VARIANT"],
            border_radius=10,
            content_padding=15,
            border_color="transparent"
        )
        
        app_icon = ft.Dropdown(
            label="Иконка",
            options=[
                ft.dropdown.Option("web"),
                ft.dropdown.Option("play_arrow"),
                ft.dropdown.Option("music_note"),
                ft.dropdown.Option("groups"),
                ft.dropdown.Option("sports_esports"),
                ft.dropdown.Option("computer"),
                ft.dropdown.Option("work"),
                ft.dropdown.Option("cloud"),
                ft.dropdown.Option("medical_services"),
                ft.dropdown.Option("verified_user"),
                ft.dropdown.Option("apps"),
            ],
            value=app["icon"],
            filled=True,
            bgcolor=colors["SURFACE_VARIANT"],
            border_radius=10,
            content_padding=15,
            border_color="transparent"
        )
        
        def save_changes(e):
            if app_name.value and app_url.value:
                # ИСПРАВЛЕНИЕ: Обновляем существующий объект, а не создаем новый
                app["name"] = app_name.value
                app["url"] = app_url.value
                app["category"] = app_category.value
                app["icon"] = app_icon.value
                app["type"] = "web" if app_url.value.startswith("http") else "app"
                app["official_url"] = app_url.value if app_url.value.startswith("http") else ""
                
                self.core.app_manager.save_custom_apps()
                
                self.core.page.close(dialog)
                self.core.page.show_snack_bar(ft.SnackBar(
                    content=ft.Text(f"✅ Приложение '{app_name.value}' обновлено!"), 
                    action="OK"
                ))
                self.core.update_main_content()
                self.core.update_sidebar()
            else:
                self.core.page.show_snack_bar(ft.SnackBar(
                    content=ft.Text("❌ Заполните все обязательные поля"), 
                    action="OK"
                ))
        
        def cancel_edit(e):
            self.core.page.close(dialog)
        
        dialog = ft.AlertDialog(
            title=ft.Text("Редактировать приложение"),
            content=ft.Container(
                content=ft.Column([
                    app_name,
                    app_url,
                    app_category,
                    app_icon,
                ], height=250),
                width=500
            ),
            actions=[
                ft.TextButton("Отмена", on_click=cancel_edit),
                ft.FilledButton("Сохранить", on_click=save_changes),
            ]
        )
        
        self.core.page.open(dialog)

    def show_edit_tags_dialog(self, app):
        colors = self.core.get_colors()
        
        tags_info = self.core.app_manager.get_app_tags(app)
        
        tags_field = ft.TextField(
            label="Теги (через запятую)",
            value=tags_info.get("tags", ""),
            hint_text="работа, документы, важное",
            expand=True,
            filled=True,
            bgcolor=colors["SURFACE_VARIANT"],
            border_radius=10,
            content_padding=15,
            border_color="transparent"
        )
        
        notes_field = ft.TextField(
            label="Заметки",
            value=tags_info.get("notes", ""),
            hint_text="Дополнительная информация о приложении",
            multiline=True,
            min_lines=3,
            max_lines=5,
            expand=True,
            filled=True,
            bgcolor=colors["SURFACE_VARIANT"],
            border_radius=10,
            content_padding=15,
            border_color="transparent"
        )
        
        def save_tags(e):
            self.core.app_manager.save_app_tags(app, tags_field.value, notes_field.value)
            self.core.page.close(dialog)
            self.core.page.show_snack_bar(ft.SnackBar(
                content=ft.Text(f"✅ Теги для '{app['name']}' сохранены!"), 
                action="OK"
            ))
        
        def cancel_tags(e):
            self.core.page.close(dialog)
        
        dialog = ft.AlertDialog(
            title=ft.Text(f"Теги для {app['name']}"),
            content=ft.Container(
                content=ft.Column([
                    tags_field,
                    notes_field,
                ], height=250),
                width=500
            ),
            actions=[
                ft.TextButton("Отмена", on_click=cancel_tags),
                ft.FilledButton("Сохранить", on_click=save_tags),
            ]
        )
        
        self.core.page.open(dialog)

    def show_duplicate_favorite_dialog(self, app):
        colors = self.core.get_colors()
        
        similar_apps = self.core.app_manager.get_similar_favorites(app)
        
        def close_dialog(e=None):
            self.core.page.close(dialog)
        
        def replace_existing(e, existing_app):
            self.core.app_manager.remove_from_favorites(existing_app)
            success, message = self.core.app_manager.add_to_favorites(app)
            if self.core.system_notifications_enabled:
                self.core.show_system_notification("Избранное", message)
            if success:
                self.core.update_main_content()
            close_dialog()
        
        def add_anyway(e):
            success, message = self.core.app_manager.add_to_favorites(app)
            if self.core.system_notifications_enabled:
                self.core.show_system_notification("Избранное", message)
            if success:
                self.core.update_main_content()
            close_dialog()
        
        content_controls = [
            ft.Text("Похожее приложение уже в избранном", size=16, weight=ft.FontWeight.BOLD),
            ft.Text(f"'{app['name']}' похоже на:", size=14, color=colors["ON_SURFACE_VARIANT"]),
            ft.Container(height=10),
        ]
        
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
        
        self.core.page.open(dialog)

    # ДОПОЛНИТЕЛЬНЫЕ МЕТОДЫ ДЛЯ УПРАВЛЕНИЯ ПЛАГИНАМИ
    def show_plugin_info_dialog(self, plugin_name, plugin_info):
        """Показать информацию о плагине"""
        colors = self.core.get_colors()
        
        def close_dialog(e=None):
            self.core.page.close(dialog)
        
        def toggle_plugin(e):
            if plugin_info.get("enabled", False):
                self.core.plugin_manager.disable_plugin(plugin_name)
            else:
                self.core.plugin_manager.enable_plugin(plugin_name)
            close_dialog()
            self.core.page.show_snack_bar(ft.SnackBar(
                content=ft.Text(f"✅ Состояние плагина {plugin_name} изменено"),
                action="OK"
            ))
        
        content = ft.Column([
            ft.Container(
                content=ft.Row([
                    ft.Icon("extension", color=colors["ACCENT"], size=32),
                    ft.Text(plugin_name, size=20, weight=ft.FontWeight.BOLD),
                ], spacing=12),
                padding=ft.padding.only(bottom=15)
            ),
            
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("Статус:", weight=ft.FontWeight.W_500),
                        ft.Text("🟢 Загружен" if plugin_name in self.core.plugin_manager.loaded_plugins else "🔴 Выключен", 
                               color=colors["SUCCESS"] if plugin_name in self.core.plugin_manager.loaded_plugins else colors["ERROR"])
                    ]),
                    ft.Row([
                        ft.Text("Включен:", weight=ft.FontWeight.W_500),
                        ft.Text("Да" if plugin_info.get("enabled", False) else "Нет")
                    ]),
                    ft.Row([
                        ft.Text("Путь:", weight=ft.FontWeight.W_500),
                        ft.Text(plugin_info.get("path", "Неизвестно"), size=12, color=colors["ON_SURFACE_VARIANT"])
                    ]),
                ], spacing=8),
                bgcolor=colors["SURFACE_VARIANT"] + "20",
                border_radius=10,
                padding=15
            ),
            
            ft.Container(height=15),
            
            ft.Row([
                ft.FilledButton(
                    "Включить" if not plugin_info.get("enabled", False) else "Выключить",
                    on_click=toggle_plugin,
                    icon="toggle_on" if plugin_info.get("enabled", False) else "toggle_off"
                ),
                ft.FilledButton(
                    "Перезагрузить",
                    on_click=lambda e: self.reload_plugin(plugin_name, e),
                    icon="refresh"
                ),
            ], spacing=10),
        ])
        
        dialog = ft.AlertDialog(
            title=ft.Text("Информация о плагине"),
            content=content,
            actions=[
                ft.TextButton("Закрыть", on_click=close_dialog)
            ]
        )
        
        self.core.page.open(dialog)

    def reload_plugin(self, plugin_name, e):
        """Перезагрузить плагин"""
        self.core.plugin_manager.unload_plugin(plugin_name)
        self.core.plugin_manager.load_plugin(plugin_name)
        self.core.page.show_snack_bar(ft.SnackBar(
            content=ft.Text(f"✅ Плагин {plugin_name} перезагружен"),
            action="OK"
        ))

    # МЕТОДЫ ДЛЯ УПРАВЛЕНИЯ ТЕМАМИ
    def show_theme_preview_dialog(self, theme_name, theme_data):
        """Показать превью темы"""
        colors = self.core.get_colors()
        
        def close_dialog(e=None):
            self.core.page.close(dialog)
        
        def apply_theme(e):
            self.core.apply_theme_settings(theme_name)
            close_dialog()
        
        # Создаем превью элементов интерфейса в стиле темы
        preview_content = ft.Container(
            content=ft.Column([
                ft.Text("Превью темы", size=16, weight=ft.FontWeight.BOLD, color=theme_data["ON_SURFACE"]),
                ft.Container(height=10),
                
                # Превью кнопки
                ft.Container(
                    content=ft.FilledButton(
                        "Пример кнопки",
                        on_click=lambda e: None,
                        style=ft.ButtonStyle(
                            color=theme_data["ON_SURFACE"],
                            bgcolor=theme_data["ACCENT"]
                        )
                    ),
                    bgcolor=theme_data["SURFACE"],
                    padding=15,
                    border_radius=12
                ),
                
                ft.Container(height=10),
                
                # Превью карточки
                ft.Container(
                    content=ft.Column([
                        ft.Text("Пример карточки", color=theme_data["ON_SURFACE"], weight=ft.FontWeight.W_500),
                        ft.Text("Это пример текста в карточке", color=theme_data["ON_SURFACE_VARIANT"], size=12),
                    ]),
                    bgcolor=theme_data["SURFACE_VARIANT"],
                    padding=15,
                    border_radius=12
                ),
                
                ft.Container(height=10),
                
                # Превью индикаторов
                ft.Row([
                    ft.Container(
                        content=ft.Icon("check_circle", color=theme_data["SUCCESS"], size=20),
                        bgcolor=theme_data["SUCCESS"] + "20",
                        padding=10,
                        border_radius=8
                    ),
                    ft.Container(
                        content=ft.Icon("error", color=theme_data["ERROR"], size=20),
                        bgcolor=theme_data["ERROR"] + "20",
                        padding=10,
                        border_radius=8
                    ),
                    ft.Container(
                        content=ft.Icon("info", color=theme_data["ACCENT"], size=20),
                        bgcolor=theme_data["ACCENT"] + "20",
                        padding=10,
                        border_radius=8
                    ),
                ], spacing=10),
            ]),
            bgcolor=theme_data["BG"],
            padding=20,
            border_radius=15
        )
        
        dialog = ft.AlertDialog(
            title=ft.Text(f"Превью темы: {theme_data['NAME']}"),
            content=preview_content,
            actions=[
                ft.TextButton("Закрыть", on_click=close_dialog),
                ft.FilledButton("Применить тему", on_click=apply_theme),
            ]
        )
        
        self.core.page.open(dialog)

    # МЕТОДЫ ДЛЯ СИСТЕМНЫХ УВЕДОМЛЕНИЙ
    def show_system_info_dialog(self, title, message, message_type="info"):
        """Показать системное информационное сообщение"""
        colors = self.core.get_colors()
        
        # Выбор иконки в зависимости от типа сообщения
        icon_map = {
            "info": ("info", colors["ACCENT"]),
            "success": ("check_circle", colors["SUCCESS"]),
            "warning": ("warning", colors["ERROR"]),
            "error": ("error", colors["ERROR"])
        }
        
        icon_name, icon_color = icon_map.get(message_type, ("info", colors["ACCENT"]))
        
        def close_dialog(e=None):
            self.core.page.close(dialog)
        
        dialog = ft.AlertDialog(
            title=ft.Row([
                ft.Icon(icon_name, color=icon_color, size=24),
                ft.Text(title, weight=ft.FontWeight.BOLD),
            ], spacing=12),
            content=ft.Text(message, color=colors["ON_SURFACE_VARIANT"]),
            actions=[
                ft.FilledButton("OK", on_click=close_dialog)
            ]
        )
        
        self.core.page.open(dialog)

    # МЕТОДЫ ДЛЯ РАБОТЫ С ПРИЛОЖЕНИЯМИ
    def show_bulk_actions_dialog(self, apps_list):
        """Показать диалог массовых действий"""
        colors = self.core.get_colors()
        
        selected_apps = []
        
        def close_dialog(e=None):
            self.core.page.close(dialog)
        
        def toggle_app_selection(app, checkbox):
            if checkbox.value:
                selected_apps.append(app)
            else:
                if app in selected_apps:
                    selected_apps.remove(app)
        
        def add_selected_to_favorites(e):
            for app in selected_apps:
                if not self.core.app_manager.is_duplicate_favorite(app):
                    self.core.app_manager.add_to_favorites(app)
            self.core.page.show_snack_bar(ft.SnackBar(
                content=ft.Text(f"✅ Добавлено {len(selected_apps)} приложений в избранное"),
                action="OK"
            ))
            close_dialog()
            self.core.update_main_content()
        
        # Создаем список приложений с чекбоксами
        apps_list_content = ft.Column(
            [
                ft.Container(
                    content=ft.Row([
                        ft.Checkbox(
                            on_change=lambda e, app=app: toggle_app_selection(app, e.control)
                        ),
                        ft.Icon(app["icon"], color=colors["ACCENT"], size=20),
                        ft.Text(app["name"], expand=True),
                        ft.Text(app["category"], size=12, color=colors["ON_SURFACE_VARIANT"]),
                    ]),
                    padding=10,
                    bgcolor=colors["SURFACE_VARIANT"] + "10",
                    border_radius=8,
                    margin=ft.margin.only(bottom=5),
                )
                for app in apps_list
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            height=300
        )
        
        dialog = ft.AlertDialog(
            title=ft.Text("Массовые действия"),
            content=ft.Column([
                ft.Text(f"Выберите приложения для действий ({len(apps_list)} доступно)"),
                ft.Container(height=10),
                apps_list_content,
            ]),
            actions=[
                ft.TextButton("Отмена", on_click=close_dialog),
                ft.FilledButton(
                    "Добавить выбранные в избранное", 
                    on_click=add_selected_to_favorites,
                    disabled=len(selected_apps) == 0
                ),
            ]
        )
        
        self.core.page.open(dialog)

    # МЕТОДЫ ДЛЯ РАБОТЫ С НАСТРОЙКАМИ
    def show_reset_settings_dialog(self):
        """Показать диалог сброса настроек"""
        colors = self.core.get_colors()
        
        def close_dialog(e=None):
            self.core.page.close(dialog)
        
        def reset_settings(e):
            # Сброс всех настроек к значениям по умолчанию
            self.core.theme_manager.current_theme = "dark"
            self.core.theme_manager.glass_effect_enabled = True
            self.core.theme_manager.glass_intensity = "medium"
            self.core.theme_manager.smooth_animations = True
            self.core.theme_manager.android_animations = True
            
            # Сброс новых настроек версии 2.2
            self.core.theme_manager.time_format = "24"
            self.core.theme_manager.date_format = "dd.mm.yyyy"
            self.core.theme_manager.font_family = "Segoe UI"
            self.core.theme_manager.font_size = 14
            self.core.theme_manager.time_font_size = 18
            self.core.theme_manager.date_font_size = 12
            self.core.theme_manager.time_font_family = "Segoe UI"
            self.core.theme_manager.date_font_family = "Segoe UI"
            self.core.theme_manager.backup_auto = True
            self.core.theme_manager.backup_interval = 7
            self.core.theme_manager.search_cache_enabled = True
            self.core.theme_manager.virtualization_enabled = True
            
            self.core.theme_manager.save_settings()
            
            # Сброс системных настроек
            self.core.auto_update_enabled = True
            self.core.system_notifications_enabled = True
            
            self.core.page.show_snack_bar(ft.SnackBar(
                content=ft.Text("✅ Все настройки сброшены к значениям по умолчанию"),
                action="OK"
            ))
            
            # Обновление интерфейса
            self.core.apply_initial_theme()
            close_dialog()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Сброс настроек"),
            content=ft.Column([
                ft.Icon("warning", color=colors["ERROR"], size=48),
                ft.Text("Вы уверены, что хотите сбросить все настройки?", 
                       size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Text("Это действие нельзя отменить. Все ваши кастомные настройки будут потеряны.",
                       size=14, color=colors["ON_SURFACE_VARIANT"], text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
            actions=[
                ft.TextButton("Отмена", on_click=close_dialog),
                ft.FilledButton(
                    "Сбросить настройки", 
                    on_click=reset_settings,
                    style=ft.ButtonStyle(color=colors["ON_ERROR"], bgcolor=colors["ERROR"])
                ),
            ]
        )
        
        self.core.page.open(dialog)

    # МЕТОД ДЛЯ ОБРАБОТКИ ОШИБОК
    def show_error_dialog(self, error_title, error_message, technical_details=None):
        """Показать диалог ошибки"""
        colors = self.core.get_colors()
        
        def close_dialog(e=None):
            self.core.page.close(dialog)
        
        def copy_error_details(e):
            import pyperclip
            details = f"{error_title}\n{error_message}"
            if technical_details:
                details += f"\n\nТехнические детали:\n{technical_details}"
            pyperclip.copy(details)
            self.core.page.show_snack_bar(ft.SnackBar(
                content=ft.Text("✅ Детали ошибки скопированы в буфер обмена"),
                action="OK"
            ))
        
        content_controls = [
            ft.Text(error_message, color=colors["ON_SURFACE_VARIANT"]),
        ]
        
        if technical_details:
            content_controls.extend([
                ft.Container(height=10),
                ft.Text("Технические детали:", size=12, weight=ft.FontWeight.W_500),
                ft.Container(
                    content=ft.Text(technical_details, size=10, color=colors["ON_SURFACE_VARIANT"]),
                    bgcolor=colors["SURFACE_VARIANT"] + "20",
                    padding=10,
                    border_radius=8
                )
            ])
        
        dialog = ft.AlertDialog(
            title=ft.Row([
                ft.Icon("error", color=colors["ERROR"], size=24),
                ft.Text(error_title, weight=ft.FontWeight.BOLD),
            ], spacing=12),
            content=ft.Column(content_controls),
            actions=[
                ft.TextButton("Копировать детали", on_click=copy_error_details),
                ft.FilledButton("OK", on_click=close_dialog),
            ]
        )
        
