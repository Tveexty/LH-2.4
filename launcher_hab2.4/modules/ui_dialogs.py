# [file name]: ui_dialogs.py
import flet as ft
import json
import os
from .glass_morphism import GlassMorphism
from .ui_dialogs_add_app import AddAppDialogMixin
from .ui_dialogs_workspace import WorkspaceDialogMixin


class UIDialogs(AddAppDialogMixin, WorkspaceDialogMixin):
    def __init__(self, ui_core):
        self.core = ui_core

    def _alpha(self, hex_color: str, opacity: float) -> str:
        return GlassMorphism._apply_opacity(hex_color, opacity)

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
            self.core.update_sidebar()
            close_dialog()

        filter_options = [
            ("all", "apps", "Все приложения и плагины"),
            ("plugin", "extension", "Плагины и расширения"),
            ("web", "public", "Веб-приложения"),
            ("app", "desktop_windows", "Локальные приложения"),
            ("system", "computer", "Системные приложения"),
            ("custom", "star", "Мои приложения"),
        ]

        menu_items = []
        for filter_type, icon, text in filter_options:
            is_active = self.core.current_filter == filter_type
            menu_items.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(icon, color=colors["ACCENT"] if is_active else colors["ON_SURFACE_VARIANT"]),
                            ft.Text(
                                text,
                                expand=True,
                                color=colors["ON_SURFACE"],
                                weight=ft.FontWeight.W_600 if is_active else ft.FontWeight.NORMAL,
                            ),
                            ft.Icon("check", color=colors["ACCENT"], size=16)
                            if is_active
                            else ft.Container(width=16, height=16),
                        ]
                    ),
                    on_click=lambda e, ft_val=filter_type: apply_selected_filter(ft_val, e),
                    padding=14,
                    bgcolor=self._alpha(colors["ACCENT"], 0.16) if is_active else "transparent",
                    border_radius=10,
                )
            )

        dialog_content = ft.Column(
            [
                ft.Text("Фильтры библиотеки", size=18, weight=ft.FontWeight.BOLD, color=colors["ON_SURFACE"]),
                ft.Container(height=8),
                *menu_items,
            ],
            tight=True,
        )

        dialog = ft.AlertDialog(
            modal=True,
            content=ft.Container(content=dialog_content, padding=16, bgcolor=colors["SURFACE"], border_radius=14, width=360),
            actions=[ft.TextButton("Закрыть", on_click=close_dialog)],
            shape=ft.RoundedRectangleBorder(radius=14),
        )
        self.core.page.open(dialog)

    def show_settings(self, e):
        colors = self.core.get_colors()
        settings_content = self.create_modern_settings(colors)

        settings_dialog = ft.AlertDialog(
            title=ft.Container(
                content=ft.Row(
                    [
                        ft.Icon("tune", color=colors["ACCENT"], size=24),
                        ft.Text("Настройки Launcher Hab 2.4", size=20, weight=ft.FontWeight.BOLD),
                    ]
                ),
                padding=ft.padding.only(bottom=6),
            ),
            content=ft.Container(
                content=settings_content,
                width=760,
                height=620,
            ),
            actions=[
                ft.TextButton(
                    "Сбросить все настройки",
                    icon="restart_alt",
                    on_click=lambda e: self.show_reset_settings_dialog(),
                ),
                ft.FilledButton("Готово (сохранено)", on_click=lambda e: self.core.page.close(settings_dialog)),
            ],
        )
        self.core.page.open(settings_dialog)

    def create_modern_settings(self, colors):
        return ft.Tabs(
            selected_index=0,
            animation_duration=280,
            tabs=[
                ft.Tab(
                    text="Внешний вид и Часы",
                    icon=ft.Icon("palette"),
                    content=self.create_appearance_settings(colors),
                ),
                ft.Tab(
                    text="Приложения и Трекер",
                    icon=ft.Icon("apps"),
                    content=self.create_apps_settings(colors),
                ),
                ft.Tab(
                    text="Плагины и Магазин",
                    icon=ft.Icon("extension"),
                    content=self.create_plugins_settings(colors),
                ),
                ft.Tab(
                    text="Система и Бэкапы",
                    icon=ft.Icon("settings"),
                    content=self.create_system_settings_tab(colors),
                ),
                ft.Tab(
                    text="История версий",
                    icon=ft.Icon("history_edu"),
                    content=self.create_version_history(colors),
                ),
            ],
            expand=1,
        )

    def create_appearance_settings(self, colors):
        return ft.Container(
            content=ft.Column(
                [
                    self.create_settings_section(
                        "Тема оформления",
                        "Основная темная тема Midnight Slate (как на скриншоте 2), AMOLED Оникс и кастомные схемы",
                        self.create_theme_selector(colors),
                        colors,
                    ),
                    self.create_settings_section(
                        "🕒 Вертикальные часы Android 14 и стили часов",
                        "Настройте вертикальные часы как на Android, Flip-часы, капсулу и цвета",
                        self.create_customization_settings(colors),
                        colors,
                    ),
                    self.create_settings_section(
                        "Эффекты прозрачного стекла (Glassmorphism 2.4)",
                        "Управление размытием, прозрачностью и плавными анимациями",
                        self.create_effects_settings(colors),
                        colors,
                    ),
                    self.create_settings_section(
                        "Кастомные темы",
                        "Создавайте, экспортируйте и удаляйте собственные темы",
                        self.create_custom_themes_management(colors),
                        colors,
                    ),
                ],
                scroll=ft.ScrollMode.ADAPTIVE,
            ),
            padding=16,
        )

    def create_apps_settings(self, colors):
        return ft.Container(
            content=ft.Column(
                [
                    self.create_settings_section(
                        "Управление запуском, сеткой и плагинами",
                        "Настройте отображение плагинов в списке запуска, размер сетки и поведение при старте",
                        self.create_apps_management(colors),
                        colors,
                    ),
                ],
                scroll=ft.ScrollMode.ADAPTIVE,
            ),
            padding=16,
        )

    def create_plugins_settings(self, colors):
        return ft.Container(
            content=ft.Column(
                [
                    self.create_settings_section(
                        "Центр плагинов и расширений (API 2.4)",
                        "Скачивайте новые плагины, меняйте их настройки, включайте в список запуска или удаляйте",
                        self.core.plugin_manager.create_plugin_ui(colors),
                        colors,
                    ),
                ],
                scroll=ft.ScrollMode.ADAPTIVE,
            ),
            padding=16,
        )

    def create_system_settings_tab(self, colors):
        return ft.Container(
            content=ft.Column(
                [
                    self.create_settings_section(
                        "Smart Workspace",
                        "Пресеты одновременного запуска игр, браузеров и рабочих программ",
                        ft.Column(
                            [
                                self.create_settings_button(
                                    "Открыть менеджер Smart Workspace",
                                    "rocket_launch",
                                    lambda e: self.show_workspace_manager(e),
                                    colors,
                                ),
                            ]
                        ),
                        colors,
                    ),
                    self.create_settings_section(
                        "Поведение окна и уведомления",
                        "Режим рабочего стола, автообновление и системные уведомления",
                        ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Switch(
                                            value=self.core.theme_manager.desktop_mode_enabled,
                                            on_change=lambda e: (
                                                self.core.theme_manager.set_desktop_mode(e.control.value),
                                                self.core.show_toast("✅ Настройка режима окна сохранена"),
                                            ),
                                            active_track_color=colors["ACCENT"],
                                        ),
                                        ft.Text("Режим замены рабочего стола (возвращать окно после сворачивания)", expand=True),
                                    ]
                                ),
                                ft.Row(
                                    [
                                        ft.Switch(
                                            value=self.core.system_notifications_enabled,
                                            on_change=self.core.toggle_system_notifications,
                                            active_track_color=colors["ACCENT"],
                                        ),
                                        ft.Text("Системные всплывающие уведомления при запуске", expand=True),
                                    ]
                                ),
                                self.create_auto_update_settings(colors),
                            ],
                            spacing=10,
                        ),
                        colors,
                    ),
                    self.create_settings_section(
                        "🎯 Оптимизация производительности",
                        "Кэширование поиска и виртуализация списков",
                        self.create_performance_settings(colors),
                        colors,
                    ),
                    self.create_settings_section(
                        "💾 Система резервного копирования",
                        "Создание, восстановление и удаление резервных копий настроек",
                        self.create_backup_settings(colors),
                        colors,
                    ),
                    self.create_settings_section(
                        "⌨️ Горячие клавиши",
                        "Быстрые комбинации клавиш для управления лаунчером",
                        self.create_hotkey_settings(colors),
                        colors,
                    ),
                ],
                scroll=ft.ScrollMode.ADAPTIVE,
            ),
            padding=16,
        )

    def create_performance_settings(self, colors):
        return ft.Column(
            [
                ft.Row(
                    [
                        ft.Switch(
                            value=self.core.theme_manager.search_cache_enabled,
                            on_change=lambda e: (
                                self.core.set_performance_settings(
                                    e.control.value, self.core.theme_manager.virtualization_enabled
                                ),
                                self.core.show_toast("✅ Настройки кэша сохранены"),
                            ),
                            active_track_color=colors["ACCENT"],
                        ),
                        ft.Column(
                            [
                                ft.Text("Кэширование поиска", weight=ft.FontWeight.W_500),
                                ft.Text("Мгновенные результаты при повторных запросах", size=12, color=colors["ON_SURFACE_VARIANT"]),
                            ],
                            expand=True,
                        ),
                    ]
                ),
                ft.Row(
                    [
                        ft.Switch(
                            value=self.core.theme_manager.virtualization_enabled,
                            on_change=lambda e: (
                                self.core.set_performance_settings(
                                    self.core.theme_manager.search_cache_enabled, e.control.value
                                ),
                                self.core.show_toast("✅ Настройки виртуализации сохранены"),
                            ),
                            active_track_color=colors["ACCENT"],
                        ),
                        ft.Column(
                            [
                                ft.Text("Виртуализация списков", weight=ft.FontWeight.W_500),
                                ft.Text("Плавная работа с большим списком приложений", size=12, color=colors["ON_SURFACE_VARIANT"]),
                            ],
                            expand=True,
                        ),
                    ]
                ),
            ],
            spacing=12,
        )

    def create_backup_settings(self, colors):
        return ft.Column(
            [
                ft.Row(
                    [
                        ft.Switch(
                            value=self.core.theme_manager.backup_auto,
                            on_change=lambda e: (
                                self.core.theme_manager.set_backup_settings(
                                    e.control.value, self.core.theme_manager.backup_interval
                                ),
                                self.core.show_toast("✅ Авто-бэкап сохранен"),
                            ),
                            active_track_color=colors["ACCENT"],
                        ),
                        ft.Column(
                            [
                                ft.Text("Автоматическое резервное копирование", weight=ft.FontWeight.W_500),
                                ft.Text("Регулярное сохранение всех настроек", size=12, color=colors["ON_SURFACE_VARIANT"]),
                            ],
                            expand=True,
                        ),
                    ]
                ),
                ft.Text("Интервал автоматического бэкапа:", size=13, weight=ft.FontWeight.W_500),
                ft.Dropdown(
                    value=str(self.core.theme_manager.backup_interval),
                    options=[
                        ft.dropdown.Option("1", "Ежедневно"),
                        ft.dropdown.Option("3", "Каждые 3 дня"),
                        ft.dropdown.Option("7", "Еженедельно"),
                        ft.dropdown.Option("30", "Ежемесячно"),
                    ],
                    on_change=lambda e: (
                        self.core.theme_manager.set_backup_settings(
                            self.core.theme_manager.backup_auto, int(e.control.value)
                        ),
                        self.core.show_toast("✅ Интервал бэкапа сохранен"),
                    ),
                    filled=True,
                    bgcolor=colors["SURFACE_VARIANT"],
                    border_radius=10,
                    border_color="transparent",
                ),
                ft.Row(
                    [
                        ft.FilledButton(
                            "Создать резервную копию",
                            icon="backup",
                            on_click=lambda e: self.core.create_backup_now(e),
                        ),
                        ft.OutlinedButton(
                            "Управление копиями и восстановление",
                            icon="restore",
                            on_click=lambda e: self.show_backup_manager(e),
                        ),
                    ],
                    spacing=10,
                ),
            ],
            spacing=10,
        )

    def create_hotkey_settings(self, colors):
        return ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row([ft.Text("Ctrl + F", weight=ft.FontWeight.W_600, width=120), ft.Text("Фокус в поиск")]),
                            ft.Row([ft.Text("Ctrl + R", weight=ft.FontWeight.W_600, width=120), ft.Text("Обновить библиотеку")]),
                            ft.Row([ft.Text("Ctrl + ,", weight=ft.FontWeight.W_600, width=120), ft.Text("Открыть настройки")]),
                            ft.Row([ft.Text("Ctrl + Alt + N", weight=ft.FontWeight.W_600, width=120), ft.Text("Быстрая заметка Idea Notebook")]),
                            ft.Row([ft.Text("Escape", weight=ft.FontWeight.W_600, width=120), ft.Text("Очистить поиск")]),
                        ],
                        spacing=6,
                    ),
                    bgcolor=self._alpha(colors["SURFACE_VARIANT"], 0.55),
                    border_radius=10,
                    padding=14,
                ),
                self.create_settings_button(
                    "Настроить собственные горячие клавиши",
                    "keyboard",
                    lambda e: self.show_custom_hotkeys_dialog(e),
                    colors,
                ),
            ],
            spacing=10,
        )

    def create_customization_settings(self, colors):
        """Расширенные настройки часов (включая вертикальные часы Android 14 и популярные стили)."""
        clock_styles = list(self.core.theme_manager.CLOCK_STYLES.items())

        style_buttons = []
        for s_key, s_label in clock_styles:
            is_sel = getattr(self.core.theme_manager, "clock_style", "android_vertical") == s_key
            style_buttons.append(
                ft.FilledButton(
                    s_label,
                    on_click=lambda e, k=s_key: self.set_clock_preferences(style=k),
                    style=ft.ButtonStyle(
                        color="#ffffff" if is_sel else colors["ON_SURFACE_VARIANT"],
                        bgcolor=colors["ACCENT"] if is_sel else colors["SURFACE_VARIANT"],
                    ),
                )
            )

        color_presets = ["#f1f5f9", "#60a5fa", "#10b981", "#fbbf24", "#f472b6", "#c084fc"]
        preset_chips = [
            ft.Container(
                width=28,
                height=28,
                bgcolor=hex_c,
                border_radius=14,
                border=ft.border.all(2, colors["ACCENT"] if self.core.theme_manager.time_color == hex_c else "transparent"),
                on_click=lambda e, hc=hex_c: self.set_clock_preferences(time_color=hc),
                tooltip=f"Цвет часов: {hex_c}",
            )
            for hex_c in color_presets
        ]

        return ft.Column(
            [
                ft.Row(
                    [
                        ft.Switch(
                            value=getattr(self.core.theme_manager, "show_android_clock_widget", True),
                            on_change=lambda e: self.set_clock_preferences(show_android_clock_widget=e.control.value),
                            active_track_color=colors["ACCENT"],
                        ),
                        ft.Column(
                            [
                                ft.Text("Крупный вертикальный виджет часов Android 14 на главном экране", weight=ft.FontWeight.W_600),
                                ft.Text("Вертикальные часы (Часы сверху / Минуты снизу) как на экране блокировки Android", size=12, color=colors["ON_SURFACE_VARIANT"]),
                            ],
                            expand=True,
                        ),
                    ]
                ),
                ft.Text("Стиль часов:", size=14, weight=ft.FontWeight.W_600),
                ft.Row(style_buttons, wrap=True, spacing=8, run_spacing=8),
                ft.Row(
                    [
                        ft.FilledButton(
                            "24-часовой формат",
                            on_click=lambda e: self.core.set_time_format("24"),
                            style=ft.ButtonStyle(
                                color="#ffffff" if self.core.theme_manager.time_format == "24" else colors["ON_SURFACE_VARIANT"],
                                bgcolor=colors["ACCENT"] if self.core.theme_manager.time_format == "24" else colors["SURFACE_VARIANT"],
                            ),
                        ),
                        ft.FilledButton(
                            "12-часовой (AM/PM)",
                            on_click=lambda e: self.core.set_time_format("12"),
                            style=ft.ButtonStyle(
                                color="#ffffff" if self.core.theme_manager.time_format == "12" else colors["ON_SURFACE_VARIANT"],
                                bgcolor=colors["ACCENT"] if self.core.theme_manager.time_format == "12" else colors["SURFACE_VARIANT"],
                            ),
                        ),
                    ],
                    spacing=10,
                ),
                ft.Row(
                    [
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
                    ]
                ),
                ft.Row(
                    [
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
                        ft.Text("Стеклянная рамка часов", expand=True),
                    ]
                ),
                ft.Row(
                    [
                        ft.Text("Размер шрифта часов:", size=13),
                        ft.Slider(
                            value=getattr(self.core.theme_manager, "time_font_size", 22),
                            min=14,
                            max=42,
                            divisions=28,
                            label="{value}px",
                            active_color=colors["ACCENT"],
                            on_change=lambda e: self.set_clock_preferences(time_font_size=int(e.control.value)),
                            expand=True,
                        ),
                    ]
                ),
                ft.Row([ft.Text("Быстрый цвет часов:", size=13), *preset_chips], spacing=8),
                ft.Row(
                    [
                        ft.Dropdown(
                            label="Шрифт интерфейса",
                            value=self.core.theme_manager.font_family,
                            options=[
                                ft.dropdown.Option("Segoe UI"),
                                ft.dropdown.Option("Arial"),
                                ft.dropdown.Option("Consolas"),
                                ft.dropdown.Option("Tahoma"),
                                ft.dropdown.Option("Verdana"),
                            ],
                            on_change=lambda e: (
                                self.core.set_font_family(e.control.value),
                                self.core.show_toast(f"✅ Шрифт {e.control.value} сохранен"),
                            ),
                            expand=True,
                            filled=True,
                            bgcolor=colors["SURFACE_VARIANT"],
                            border_radius=10,
                            border_color="transparent",
                        ),
                        ft.Dropdown(
                            label="Формат даты",
                            value=self.core.theme_manager.date_format,
                            options=[
                                ft.dropdown.Option("dd.mm.yyyy", "ДД.ММ.ГГГГ"),
                                ft.dropdown.Option("yyyy-mm-dd", "ГГГГ-ММ-ДД"),
                                ft.dropdown.Option("mm/dd/yyyy", "ММ/ДД/ГГГГ"),
                            ],
                            on_change=lambda e: (
                                self.core.theme_manager.set_date_format(e.control.value),
                                self.core.update_time(),
                                self.core.show_toast("✅ Формат даты сохранен"),
                            ),
                            width=180,
                            filled=True,
                            bgcolor=colors["SURFACE_VARIANT"],
                            border_radius=10,
                            border_color="transparent",
                        ),
                    ],
                    spacing=10,
                ),
            ],
            spacing=10,
        )

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
        show_android_clock_widget=None,
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
            show_android_clock_widget=show_android_clock_widget,
        )
        self.core.update_header()
        self.core.update_main_content()
        self.core.update_time()
        self.core.show_toast("✅ Настройки часов сохранены")

    def create_auto_update_settings(self, colors):
        return ft.Row(
            [
                ft.Switch(
                    value=self.core.auto_update_enabled,
                    on_change=self.core.toggle_auto_update,
                    active_track_color=colors["ACCENT"],
                ),
                ft.Text("Автоматическое обновление интерфейса при изменениях", expand=True),
            ]
        )

    def create_settings_section(self, title, subtitle, content, colors):
        return ft.Container(
            content=ft.Column(
                [
                    ft.ListTile(
                        title=ft.Text(title, weight=ft.FontWeight.BOLD, size=16),
                        subtitle=ft.Text(subtitle, color=colors["ON_SURFACE_VARIANT"], size=12),
                    ),
                    ft.Container(
                        content=content,
                        bgcolor=colors["SETTINGS_CARD"],
                        border=ft.border.all(1, colors["OUTLINE"]),
                        border_radius=14,
                        padding=18,
                    ),
                ],
                spacing=8,
            ),
            margin=ft.margin.only(bottom=16),
        )

    def create_theme_selector(self, colors):
        themes = self.core.theme_manager.get_available_themes()
        theme_buttons = ft.Row(scroll=ft.ScrollMode.ADAPTIVE, spacing=12)

        for theme_name, theme_data in themes.items():
            is_current = theme_name == self.core.theme_manager.current_theme

            theme_button = ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Icon("palette", color=theme_data["ACCENT"], size=24),
                            width=64,
                            height=56,
                            bgcolor=theme_data["BG"],
                            border=ft.border.all(2, theme_data["ACCENT"] if is_current else theme_data["OUTLINE"]),
                            border_radius=12,
                            alignment=ft.alignment.center,
                        ),
                        ft.Text(theme_data["NAME"], size=11, text_align=ft.TextAlign.CENTER, max_lines=1),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=6,
                ),
                on_click=lambda e, tn=theme_name: self.core.apply_theme_settings(tn),
                padding=10,
                bgcolor=self._alpha(colors["ACCENT"], 0.16) if is_current else self._alpha(colors["SURFACE_VARIANT"], 0.45),
                border=ft.border.all(1.5, colors["ACCENT"] if is_current else "transparent"),
                border_radius=12,
                width=128,
            )
            theme_buttons.controls.append(theme_button)

        return theme_buttons

    def create_custom_themes_management(self, colors):
        def _export_current_theme(_):
            cur_name = self.core.theme_manager.current_theme
            cur_data = self.core.theme_manager.get_current_theme()
            export_file = f"exported_theme_{cur_name}.json"
            try:
                with open(export_file, "w", encoding="utf-8") as f:
                    json.dump({cur_name: cur_data}, f, ensure_ascii=False, indent=2)
                self.core.show_toast(f"✅ Тема экспортирована в файл {export_file}")
            except Exception:
                self.core.show_toast("❌ Не удалось экспортировать тему")

        return ft.Column(
            [
                self.create_settings_button(
                    "Создать новую кастомную тему",
                    "palette",
                    lambda e: self.show_create_theme_dialog(),
                    colors,
                ),
                self.create_settings_button(
                    "Экспортировать текущую тему в JSON",
                    "file_download",
                    _export_current_theme,
                    colors,
                ),
            ],
            spacing=10,
        )

    def show_create_theme_dialog(self):
        colors = self.core.get_colors()

        theme_name = ft.TextField(
            label="Название темы",
            hint_text="Моя тема",
            filled=True,
            bgcolor=colors["SURFACE_VARIANT"],
            border_radius=10,
            border_color="transparent",
        )
        bg_field = ft.TextField(label="Основной фон (#RRGGBB)", value="#0d111a", filled=True, bgcolor=colors["SURFACE_VARIANT"], border_color="transparent")
        surface_field = ft.TextField(label="Поверхность карточек (#RRGGBB)", value="#151b26", filled=True, bgcolor=colors["SURFACE_VARIANT"], border_color="transparent")
        accent_field = ft.TextField(label="Акцентный цвет (#RRGGBB)", value="#3b82f6", filled=True, bgcolor=colors["SURFACE_VARIANT"], border_color="transparent")

        def create_theme(_):
            name_val = (theme_name.value or "").strip()
            if not name_val:
                self.core.show_toast("❌ Введите название темы")
                return
            bg_c = (bg_field.value or "#0d111a").strip()
            surf_c = (surface_field.value or "#151b26").strip()
            acc_c = (accent_field.value or "#3b82f6").strip()

            new_theme = {
                "NAME": name_val,
                "BG": bg_c,
                "SURFACE": surf_c,
                "SURFACE_VARIANT": "#1e2636",
                "ON_SURFACE": "#f1f5f9",
                "ON_SURFACE_VARIANT": "#8b9bb4",
                "OUTLINE": "#263042",
                "ACCENT": acc_c,
                "ACCENT_GLOW": self._alpha(acc_c, 0.25),
                "ERROR": "#ef4444",
                "SUCCESS": "#10b981",
                "WEB_BLUE": acc_c,
                "GLASS_BG": self._alpha(surf_c, 0.75),
                "GLASS_BORDER": "#18ffffff",
                "GLASS_SHADOW": "#66000000",
                "GLASS_BG_LIGHT": self._alpha(surf_c, 0.45),
                "SETTINGS_BG": bg_c,
                "SETTINGS_SURFACE": surf_c,
                "SETTINGS_CARD": "#1b2230",
            }
            if self.core.theme_manager.add_custom_theme(name_val, new_theme):
                self.core.page.close(dialog)
                self.core.apply_theme_settings(name_val)

        dialog = ft.AlertDialog(
            title=ft.Text("Создать кастомную тему"),
            content=ft.Container(
                width=480,
                content=ft.Column([theme_name, bg_field, surface_field, accent_field], spacing=10, tight=True),
            ),
            actions=[
                ft.TextButton("Отмена", on_click=lambda e: self.core.page.close(dialog)),
                ft.FilledButton("Создать и применить", on_click=create_theme),
            ],
        )
        self.core.page.open(dialog)

    def create_effects_settings(self, colors):
        return ft.Column(
            [
                ft.Row(
                    [
                        ft.Switch(
                            value=self.core.theme_manager.glass_effect_enabled,
                            on_change=lambda e: self.core.toggle_glass_effect(),
                            active_track_color=colors["ACCENT"],
                        ),
                        ft.Column(
                            [
                                ft.Text("Эффект матового стекла (Glassmorphism 2.4)", weight=ft.FontWeight.W_600),
                                ft.Text("Размытие заднего плана ft.Blur и полупрозрачные панели", size=12, color=colors["ON_SURFACE_VARIANT"]),
                            ],
                            expand=True,
                        ),
                    ]
                ),
                self.create_glass_intensity_selector(colors),
                ft.Row(
                    [
                        ft.Text("Плотность фона карточек (%):", size=13),
                        ft.Slider(
                            value=self.core.theme_manager.advanced_glass_opacity,
                            min=25,
                            max=95,
                            divisions=14,
                            label="{value}%",
                            active_color=colors["ACCENT"],
                            on_change=lambda e: (
                                self.core.theme_manager.set_advanced_glass(True, int(e.control.value)),
                                self.core.update_main_content(),
                                self.core.update_sidebar(),
                            ),
                            expand=True,
                        ),
                    ]
                ),
                ft.Row(
                    [
                        ft.Switch(
                            value=self.core.theme_manager.smooth_animations,
                            on_change=lambda e: self.core.toggle_smooth_animations(),
                            active_track_color=colors["ACCENT"],
                        ),
                        ft.Text("Плавные переходы между разделами (AnimatedSwitcher)", expand=True),
                    ]
                ),
            ],
            spacing=12,
        )

    def create_glass_intensity_selector(self, colors):
        intensities = [
            ("light", "blur_on", "Легкая"),
            ("medium", "blur_medium", "Средняя"),
            ("strong", "blur_off", "Глубокая"),
        ]
        intensity_buttons = ft.Row(spacing=10)
        for intensity, icon, title in intensities:
            is_active = self.core.theme_manager.glass_intensity == intensity
            intensity_buttons.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(icon, color=colors["ACCENT"] if is_active else colors["ON_SURFACE_VARIANT"], size=18),
                            ft.Text(title, size=12, weight=ft.FontWeight.W_600),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    on_click=lambda e, ints=intensity: self.core.set_glass_intensity(ints),
                    padding=12,
                    bgcolor=self._alpha(colors["ACCENT"], 0.18) if is_active else self._alpha(colors["SURFACE_VARIANT"], 0.5),
                    border=ft.border.all(1.5, colors["ACCENT"] if is_active else "transparent"),
                    border_radius=10,
                    expand=True,
                )
            )
        return intensity_buttons

    def create_apps_management(self, colors):
        def _reset_tracker(_):
            if hasattr(self.core.plugin_manager, "get_plugin_instance"):
                tracker = self.core.plugin_manager.get_plugin_instance("session_tracker_plugin")
                if tracker and hasattr(tracker, "reset_all_stats"):
                    tracker.reset_all_stats()
            self.core.update_main_content()
            self.core.update_sidebar()
            self.core.show_toast("✅ Все таймеры и счетчики Session Tracker сброшены в 0")

        return ft.Column(
            [
                ft.Row(
                    [
                        ft.Switch(
                            value=getattr(self.core.theme_manager, "show_plugins_in_grid", True),
                            on_change=lambda e: (
                                self.core.theme_manager.set_program_preferences(show_plugins_in_grid=e.control.value),
                                self.core.update_main_content(),
                                self.core.update_sidebar(),
                                self.core.show_toast("✅ Настройка отображения плагинов в списке сохранена"),
                            ),
                            active_track_color=colors["ACCENT"],
                        ),
                        ft.Column(
                            [
                                ft.Text("Отображать активные плагины в списке запуска", weight=ft.FontWeight.W_600),
                                ft.Text("Плагины доступны прямо в библиотеке и категории «Плагины»", size=12, color=colors["ON_SURFACE_VARIANT"]),
                            ],
                            expand=True,
                        ),
                    ]
                ),
                ft.Row(
                    [
                        ft.Switch(
                            value=getattr(self.core.theme_manager, "detox_notifications", True),
                            on_change=lambda e: (
                                self.core.theme_manager.set_program_preferences(detox_notifications=e.control.value),
                                self.core.show_toast("✅ Настройка уведомлений детокса сохранена"),
                            ),
                            active_track_color=colors["ACCENT"],
                        ),
                        ft.Column(
                            [
                                ft.Text("Уведомления цифрового детокса при превышении лимита", weight=ft.FontWeight.W_600),
                                ft.Text("Предупреждать, когда время в играх или соцсетях превышает дневной лимит", size=12, color=colors["ON_SURFACE_VARIANT"]),
                            ],
                            expand=True,
                        ),
                    ]
                ),
                ft.Row(
                    [
                        ft.Dropdown(
                            label="Колонок карточек в ряду",
                            value=str(getattr(self.core.theme_manager, "card_columns", 6)),
                            options=[
                                ft.dropdown.Option("4", "4 колонки (Крупные)"),
                                ft.dropdown.Option("5", "5 колонок"),
                                ft.dropdown.Option("6", "6 колонок (Стандарт)"),
                                ft.dropdown.Option("7", "7 колонок"),
                                ft.dropdown.Option("8", "8 колонок (Компактные)"),
                            ],
                            on_change=lambda e: (
                                self.core.theme_manager.set_program_preferences(card_columns=int(e.control.value)),
                                self.core.update_main_content(),
                                self.core.show_toast("✅ Размер сетки сохранен"),
                            ),
                            expand=True,
                            filled=True,
                            bgcolor=colors["SURFACE_VARIANT"],
                            border_radius=10,
                            border_color="transparent",
                        ),
                        ft.Dropdown(
                            label="При запуске приложения",
                            value=getattr(self.core.theme_manager, "launch_behavior", "keep"),
                            options=[
                                ft.dropdown.Option("keep", "Оставлять лаунчер открытым"),
                                ft.dropdown.Option("minimize", "Сворачивать лаунчер в фон"),
                            ],
                            on_change=lambda e: (
                                self.core.theme_manager.set_program_preferences(launch_behavior=e.control.value),
                                self.core.show_toast("✅ Поведение при запуске сохранено"),
                            ),
                            expand=True,
                            filled=True,
                            bgcolor=colors["SURFACE_VARIANT"],
                            border_radius=10,
                            border_color="transparent",
                        ),
                    ],
                    spacing=10,
                ),
                self.create_settings_button(
                    "Обновить список приложений и плагинов",
                    "refresh",
                    lambda e: self.core.refresh_apps_list(),
                    colors,
                ),
                self.create_settings_button(
                    "Сбросить время Session Tracker в 0",
                    "timer_off",
                    _reset_tracker,
                    colors,
                ),
                self.create_settings_button(
                    "Сбросить избранное",
                    "star_border",
                    lambda e: self.core.reset_favorites(),
                    colors,
                ),
                self.create_settings_button(
                    "Очистить ручные пути (.exe)",
                    "clear_all",
                    lambda e: self.core.clear_manual_paths(),
                    colors,
                ),
            ],
            spacing=12,
        )

    def create_settings_button(self, text, icon, on_click, colors):
        button = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, color=colors["ACCENT"], size=20),
                    ft.Text(text, expand=True),
                    ft.Icon("chevron_right", color=colors["ON_SURFACE_VARIANT"], size=16),
                ]
            ),
            on_click=on_click,
            padding=14,
            bgcolor=self._alpha(colors["SURFACE_VARIANT"], 0.55),
            border=ft.border.all(1, colors["OUTLINE"]),
            border_radius=10,
        )

        def on_hover(e):
            button.bgcolor = self._alpha(colors["ACCENT"], 0.16) if e.data == "true" else self._alpha(colors["SURFACE_VARIANT"], 0.55)
            button.update()

        button.on_hover = on_hover
        return button

    def create_version_history(self, colors):
        versions = {
            "2.4": [
                "🚀 LAUNCHER HAB 2.4 — DARK SLATE PRO, LIVE SESSION TRACKER (С 0) И ANDROID 14 ЧАСЫ",
                "🎨 ИСПРАВЛЕНЫ ЦВЕТА И РАМКИ (#AARRGGBB) — убраны желтые полосы, внедрен графитовый стиль Midnight Slate",
                "🔐 ИСПРАВЛЕНО СОХРАНЕНИЕ И ШИФРОВАНИЕ НАСТРОЕК — валидный 32-байтовый ключ Fernet без потери данных",
                "⏱️ GAME & APP SESSION TRACKER С 0 — честный отсчет времени с 00:00 при запуске приложения и живой таймер на карточках",
                "🧩 ПЛАГИНЫ В СПИСКЕ ЗАПУСКА И МАГАЗИН РАСШИРЕНИЙ — скачивание, настройка, включение и удаление плагинов в 1 клик",
                "🕒 ВЕРТИКАЛЬНЫЕ ЧАСЫ ANDROID 14 — крупный вертикальный виджет часов (HH / MM) и 8 современных стилей",
                "🔊 ФОНОВЫЙ КОНТРОЛЛЕР СИСТЕМНОЙ ГРОМКОСТИ — плавная регулировка громкости в фоновом потоке",
            ],
            "2.3": [
                "🎨 Liquid Glass интерфейс и плавающая панель Floating HUD",
                "🔌 Система плагинов (Focus Mode, Smart Weather, Smart Music, Idea Notebook)",
            ],
            "2.2": [
                "⚡ Кэширование поиска, виртуализация списков и система резервного копирования",
            ],
        }

        version_items = []
        for version, features in versions.items():
            version_items.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(f"Версия {version}", weight=ft.FontWeight.BOLD, size=16, color=colors["ACCENT"]),
                                    ft.Container(
                                        content=ft.Text(f"{len(features)} изменений", size=11, color=colors["ON_SURFACE_VARIANT"]),
                                        bgcolor=self._alpha(colors["SURFACE_VARIANT"], 0.6),
                                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                        border_radius=8,
                                    ),
                                ]
                            ),
                            ft.Column([ft.Text(feature, size=13, color=colors["ON_SURFACE_VARIANT"]) for feature in features], spacing=4),
                        ],
                        spacing=10,
                    ),
                    bgcolor=colors["SETTINGS_CARD"],
                    border=ft.border.all(1, colors["OUTLINE"]),
                    border_radius=12,
                    padding=18,
                    margin=ft.margin.only(bottom=12),
                )
            )

        return ft.Column(
            [
                ft.Text("История обновлений Launcher Hab", size=18, weight=ft.FontWeight.BOLD),
                *version_items,
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
        )

    def show_plugins_manager(self, e):
        colors = self.core.get_colors()
        plugins_content = self.core.plugin_manager.create_plugin_ui(colors)

        plugins_dialog = ft.AlertDialog(
            title=ft.Container(
                content=ft.Row(
                    [
                        ft.Icon("extension", color=colors["ACCENT"], size=24),
                        ft.Text("Центр плагинов и магазин расширений (API 2.4)", size=19, weight=ft.FontWeight.BOLD),
                    ]
                ),
                padding=ft.padding.only(bottom=8),
            ),
            content=ft.Container(
                content=plugins_content,
                width=740,
                height=580,
            ),
            actions=[ft.FilledButton("Закрыть", on_click=lambda e: self.core.page.close(plugins_dialog))],
        )
        self.core.page.open(plugins_dialog)

    def show_restore_dialog(self, e):
        self.show_backup_manager(e)

    def show_backup_manager(self, e):
        """Полноценный рабочий менеджер резервных копий (создание, восстановление, удаление)."""
        colors = self.core.get_colors()
        list_col = ft.Column(spacing=8, scroll=ft.ScrollMode.ADAPTIVE, height=340)

        def rebuild_backups():
            list_col.controls.clear()
            backups = self.core.get_backup_list()
            if not backups:
                list_col.controls.append(
                    ft.Text("Резервных копий пока нет. Нажмите «Создать копию».", color=colors["ON_SURFACE_VARIANT"])
                )
                return
            for b in backups:
                fname = b.get("filename", "")
                fpath = b.get("path", "")
                list_col.controls.append(
                    ft.Container(
                        bgcolor=colors["SETTINGS_CARD"],
                        border=ft.border.all(1, colors["OUTLINE"]),
                        border_radius=10,
                        padding=12,
                        content=ft.Row(
                            [
                                ft.Icon("folder_zip", color=colors["ACCENT"]),
                                ft.Column(
                                    [
                                        ft.Text(fname, weight=ft.FontWeight.BOLD, size=13),
                                        ft.Text(f"Файлов: {b.get('files_count', 0)}", size=11, color=colors["ON_SURFACE_VARIANT"]),
                                    ],
                                    spacing=2,
                                    expand=True,
                                ),
                                ft.FilledButton(
                                    "Восстановить",
                                    icon="restore",
                                    on_click=lambda ev, p=fpath: (
                                        self.core.restore_from_backup(p),
                                        self.core.page.close(dialog),
                                    ),
                                ),
                                ft.IconButton(
                                    icon="delete_outline",
                                    icon_color=colors["ERROR"],
                                    tooltip="Удалить копию",
                                    on_click=lambda ev, fn=fname: (
                                        self.core.delete_backup(fn),
                                        rebuild_backups(),
                                        list_col.update(),
                                    ),
                                ),
                            ]
                        ),
                    )
                )

        rebuild_backups()

        dialog = ft.AlertDialog(
            title=ft.Text("Менеджер резервных копий"),
            content=ft.Container(
                width=580,
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.FilledButton(
                                    "Создать копию сейчас",
                                    icon="add",
                                    on_click=lambda ev: (
                                        self.core.create_backup_now(),
                                        rebuild_backups(),
                                        list_col.update(),
                                    ),
                                ),
                            ]
                        ),
                        list_col,
                    ],
                    spacing=10,
                    tight=True,
                ),
            ),
            actions=[ft.TextButton("Закрыть", on_click=lambda ev: self.core.page.close(dialog))],
        )
        self.core.page.open(dialog)

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
                ft.Row(
                    [
                        ft.Text(combo, width=180, weight=ft.FontWeight.W_600),
                        ft.Dropdown(
                            value=action,
                            options=[ft.dropdown.Option(a) for a in actions],
                            width=240,
                            filled=True,
                            bgcolor=colors["SURFACE_VARIANT"],
                            border_color="transparent",
                            on_change=lambda ev, c=combo: custom_hotkeys.__setitem__(c, ev.control.value),
                        ),
                    ]
                )
            )

        combo_field = ft.TextField(label="Новая комбинация", hint_text="ctrl+alt+1", filled=True, bgcolor=colors["SURFACE_VARIANT"], border_color="transparent")
        action_field = ft.Dropdown(label="Действие", value="open_workspace", options=[ft.dropdown.Option(a) for a in actions], filled=True, bgcolor=colors["SURFACE_VARIANT"], border_color="transparent")

        def add_hotkey(_):
            combo = (combo_field.value or "").lower().strip()
            if combo:
                custom_hotkeys[combo] = action_field.value
                self.core.hotkey_manager.custom_hotkeys = custom_hotkeys
                self.core.hotkey_manager.save_custom_hotkeys()
                self.core.page.close(dialog)
                self.show_custom_hotkeys_dialog(None)

        def save(_):
            self.core.hotkey_manager.custom_hotkeys = custom_hotkeys
            self.core.hotkey_manager.save_custom_hotkeys()
            self.core.page.close(dialog)
            self.core.show_toast("✅ Горячие клавиши сохранены")

        dialog = ft.AlertDialog(
            title=ft.Text("Кастомные горячие клавиши"),
            content=ft.Container(
                width=580,
                height=440,
                content=ft.Column(
                    [
                        ft.Column(rows, scroll=ft.ScrollMode.ADAPTIVE),
                        ft.Divider(color=colors["OUTLINE"]),
                        combo_field,
                        action_field,
                        ft.FilledButton("Добавить комбинацию", icon="add", on_click=add_hotkey),
                    ],
                    scroll=ft.ScrollMode.ADAPTIVE,
                    spacing=8,
                ),
            ),
            actions=[
                ft.TextButton("Закрыть", on_click=lambda ev: self.core.page.close(dialog)),
                ft.FilledButton("Сохранить", on_click=save),
            ],
        )
        self.core.page.open(dialog)

    def show_app_menu_dialog(self, app):
        colors = self.core.get_colors()

        if app.get("type") == "plugin":
            self.core.plugin_manager.show_plugin_settings_modal(app["package"])
            return

        def close_dialog(e=None):
            self.core.page.close(dialog)

        def toggle_tracker_timer(_):
            if hasattr(self.core.plugin_manager, "get_plugin_instance"):
                tracker = self.core.plugin_manager.get_plugin_instance("session_tracker_plugin")
                if tracker and hasattr(tracker, "toggle_session"):
                    started = tracker.toggle_session(app["package"], app["name"], app.get("category", "Games"))
                    self.core.update_main_content()
                    self.core.update_sidebar()
                    self.core.show_toast(
                        f"🟢 Таймер для {app['name']} запущен" if started else f"⏹ Таймер для {app['name']} остановлен"
                    )
            close_dialog()

        def add_to_favorites_action(e):
            if self.core.app_manager.is_duplicate_favorite(app):
                self.show_duplicate_favorite_dialog(app)
            else:
                success, message = self.core.app_manager.add_to_favorites(app)
                self.core.show_toast(message)
                if success:
                    self.core.update_main_content()
            close_dialog()

        def remove_from_favorites_action(e):
            success, message = self.core.app_manager.remove_from_favorites(app)
            self.core.show_toast(message)
            if success:
                self.core.update_main_content()
            close_dialog()

        def install_app_action(e):
            import webbrowser

            if app.get("official_url"):
                webbrowser.open(app["official_url"])
                self.core.show_toast(f"🌐 Открывается официальный сайт {app['name']}")
            else:
                self.core.show_toast("❌ Официальный сайт не указан")
            close_dialog()

        def find_path_action(e):
            close_dialog()
            self.select_manual_path(app)

        def edit_tags_action(e):
            close_dialog()
            self.show_edit_tags_dialog(app)

        def edit_app_action(e):
            close_dialog()
            if app in self.core.app_manager.custom_apps:
                self.show_edit_custom_app_dialog(app)
            else:
                self.core.show_toast("Можно редактировать только добавленные приложения")

        def remove_app_action(e):
            if app in self.core.app_manager.custom_apps:
                self.core.app_manager.remove_custom_app(app)
                self.core.update_main_content()
                self.core.update_sidebar()
                self.core.show_toast(f"🗑️ {app['name']} удалено")
            close_dialog()

        is_favorite = (
            any(fav.get("id") == app.get("id") for fav in self.core.app_manager.favorite_apps)
            if "id" in app
            else app in self.core.app_manager.favorite_apps
        )
        is_custom = app in self.core.app_manager.custom_apps
        is_running = (
            self.core.plugin_manager.is_app_running(app)
            if hasattr(self.core.plugin_manager, "is_app_running")
            else False
        )

        menu_items = [
            ft.ListTile(
                leading=ft.Icon("play_arrow", color=colors["SUCCESS"], size=20),
                title=ft.Text("Запустить приложение", size=14),
                on_click=lambda e: (close_dialog(), self.core.launch_app(app)),
                dense=True,
            ),
            ft.ListTile(
                leading=ft.Icon("timer", color=colors["ERROR"] if is_running else colors["ACCENT"], size=20),
                title=ft.Text("Остановить таймер сессии" if is_running else "Запустить таймер сессии (с 0)", size=14),
                on_click=toggle_tracker_timer,
                dense=True,
            ),
            ft.ListTile(
                leading=ft.Icon("star", color="#f59e0b", size=20),
                title=ft.Text("Удалить из избранного" if is_favorite else "Добавить в избранное", size=14),
                on_click=remove_from_favorites_action if is_favorite else add_to_favorites_action,
                dense=True,
            ),
        ]

        if app["type"] != "web" and not self.core.app_manager.is_app_installed(app):
            menu_items.append(
                ft.ListTile(
                    leading=ft.Icon("download", color=colors["WEB_BLUE"], size=20),
                    title=ft.Text("Скачать с официального сайта", size=14),
                    on_click=install_app_action,
                    dense=True,
                )
            )

        if app["type"] not in ("web", "system"):
            menu_items.append(
                ft.ListTile(
                    leading=ft.Icon("folder", color=colors["ON_SURFACE_VARIANT"], size=20),
                    title=ft.Text("Указать путь к .exe вручную", size=14),
                    on_click=find_path_action,
                    dense=True,
                )
            )

        menu_items.append(
            ft.ListTile(
                leading=ft.Icon("local_offer", color=colors["WEB_BLUE"], size=20),
                title=ft.Text("Редактировать теги и заметки", size=14),
                on_click=edit_tags_action,
                dense=True,
            )
        )

        if is_custom:
            menu_items.append(ft.Divider(height=1, color=colors["OUTLINE"]))
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
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Icon(app["icon"], size=24, color=colors["ACCENT"]),
                                ft.Text(app["name"], size=16, weight=ft.FontWeight.BOLD, color=colors["ON_SURFACE"]),
                            ],
                            spacing=10,
                        ),
                        ft.Divider(color=colors["OUTLINE"], height=8),
                        ft.Column(menu_items, spacing=0, tight=True),
                    ],
                    tight=True,
                ),
                width=310,
            ),
            actions=[ft.TextButton("Закрыть", on_click=close_dialog)],
            shape=ft.RoundedRectangleBorder(radius=14),
        )
        self.core.page.open(dialog)

    def show_favorite_app_menu_dialog(self, app):
        self.show_app_menu_dialog(app)

    def select_manual_path(self, app):
        def on_pick(ev: ft.FilePickerResultEvent):
            if ev.files:
                file_path = ev.files[0].path
                self.core.app_manager.manual_paths[app["package"]] = file_path
                self.core.app_manager.save_manual_paths()
                self.core.show_toast(f"✅ Путь для {app['name']} сохранен: {file_path}")
                self.core.update_main_content()
                self.core.update_sidebar()

        picker = ft.FilePicker(on_result=on_pick)
        if picker not in self.core.page.overlay:
            self.core.page.overlay.append(picker)
        self.core.page.update()
        try:
            picker.pick_files(allow_multiple=False)
        except Exception:
            self.core.show_toast("Не удалось открыть диалог выбора файла")

    def show_edit_custom_app_dialog(self, app):
        colors = self.core.get_colors()
        app_name = ft.TextField(label="Название приложения", value=app["name"], filled=True, bgcolor=colors["SURFACE_VARIANT"], border_color="transparent")
        app_url = ft.TextField(label="URL или путь к приложению", value=app["url"], filled=True, bgcolor=colors["SURFACE_VARIANT"], border_color="transparent")

        def save_changes(_):
            if app_name.value and app_url.value:
                app["name"] = app_name.value.strip()
                app["url"] = app_url.value.strip()
                app["type"] = "web" if app["url"].startswith("http") else "app"
                self.core.app_manager.save_custom_apps()
                self.core.page.close(dialog)
                self.core.show_toast(f"✅ Приложение «{app['name']}» обновлено")
                self.core.update_main_content()
                self.core.update_sidebar()

        dialog = ft.AlertDialog(
            title=ft.Text("Редактировать приложение"),
            content=ft.Container(width=480, content=ft.Column([app_name, app_url], spacing=10, tight=True)),
            actions=[
                ft.TextButton("Отмена", on_click=lambda e: self.core.page.close(dialog)),
                ft.FilledButton("Сохранить", on_click=save_changes),
            ],
        )
        self.core.page.open(dialog)

    def show_edit_tags_dialog(self, app):
        colors = self.core.get_colors()
        tags_info = self.core.app_manager.get_app_tags(app)
        tags_field = ft.TextField(label="Теги (через запятую)", value=tags_info.get("tags", ""), filled=True, bgcolor=colors["SURFACE_VARIANT"], border_color="transparent")
        notes_field = ft.TextField(label="Заметки", value=tags_info.get("notes", ""), multiline=True, min_lines=3, filled=True, bgcolor=colors["SURFACE_VARIANT"], border_color="transparent")

        def save_tags(_):
            self.core.app_manager.save_app_tags(app, tags_field.value, notes_field.value)
            self.core.page.close(dialog)
            self.core.show_toast(f"✅ Теги для «{app['name']}» сохранены")

        dialog = ft.AlertDialog(
            title=ft.Text(f"Теги для {app['name']}"),
            content=ft.Container(width=460, content=ft.Column([tags_field, notes_field], spacing=10, tight=True)),
            actions=[
                ft.TextButton("Отмена", on_click=lambda e: self.core.page.close(dialog)),
                ft.FilledButton("Сохранить", on_click=save_tags),
            ],
        )
        self.core.page.open(dialog)

    def show_duplicate_favorite_dialog(self, app):
        colors = self.core.get_colors()
        similar_apps = self.core.app_manager.get_similar_favorites(app)

        def add_anyway(_):
            success, message = self.core.app_manager.add_to_favorites(app)
            self.core.show_toast(message)
            if success:
                self.core.update_main_content()
            self.core.page.close(dialog)

        dialog = ft.AlertDialog(
            title=ft.Text("Похожее приложение уже в избранном"),
            content=ft.Text(
                f"Найдено похожее: {', '.join(s['name'] for s in similar_apps)}. Добавить «{app['name']}» всё равно?",
                color=colors["ON_SURFACE_VARIANT"],
            ),
            actions=[
                ft.TextButton("Отмена", on_click=lambda e: self.core.page.close(dialog)),
                ft.FilledButton("Добавить", on_click=add_anyway),
            ],
        )
        self.core.page.open(dialog)

    def show_reset_settings_dialog(self):
        colors = self.core.get_colors()

        def reset_settings(_):
            self.core.theme_manager.current_theme = "dark"
            self.core.theme_manager.glass_effect_enabled = True
            self.core.theme_manager.glass_intensity = "medium"
            self.core.theme_manager.clock_style = "android_vertical"
            self.core.theme_manager.show_android_clock_widget = True
            self.core.theme_manager.show_plugins_in_grid = True
            self.core.theme_manager.save_settings()
            self.core.apply_initial_theme()
            self.core.update_header()
            self.core.update_main_content()
            self.core.update_sidebar()
            self.core.page.close(dialog)
            self.core.show_toast("✅ Все настройки сброшены к значениям по умолчанию")

        dialog = ft.AlertDialog(
            title=ft.Text("Сброс настроек"),
            content=ft.Text("Сбросить все настройки темы, часов и интерфейса к стандартным значениям v2.4?", color=colors["ON_SURFACE_VARIANT"]),
            actions=[
                ft.TextButton("Отмена", on_click=lambda e: self.core.page.close(dialog)),
                ft.FilledButton("Сбросить", on_click=reset_settings, style=ft.ButtonStyle(bgcolor=colors["ERROR"], color="#ffffff")),
            ],
        )
        self.core.page.open(dialog)
