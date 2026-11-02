# [file name]: ui_panels.py
import flet as ft
from datetime import datetime
from .glass_morphism import GlassMorphism


class UIPanels:
    WEEKDAYS_RU = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

    def _with_opacity(self, hex_color: str, percent: int) -> str:
        if not isinstance(hex_color, str) or not hex_color.startswith("#"):
            return hex_color
        clean = hex_color[:7] if len(hex_color) >= 7 else hex_color
        if len(clean) != 7:
            return hex_color
        alpha = max(0, min(255, int(percent * 2.55)))
        return f"{clean}{alpha:02x}"

    def __init__(self, ui_core):
        self.core = ui_core
        self.current_time_text = None
        self.current_date_text = None
        self.clock_container = None
        self.devices_container = None
        self.volume_slider_container = None
        self.audio_button = None
        self.search_field = None
        self.apps_list = None
        self.animated_switcher = None

    def create_header(self):
        colors = self.core.get_colors()
        self.create_time_elements()

        clock_frame_enabled = getattr(self.core.theme_manager, "clock_glass_frame", True)
        clock_style = getattr(self.core.theme_manager, "clock_style", "standard")

        if clock_style == "pill_glass":
            time_inner = ft.Row(
                [
                    ft.Icon("schedule", size=16, color=colors["ACCENT"]),
                    self.current_time_text,
                    ft.Text("•", size=12, color=colors["ON_SURFACE_VARIANT"]),
                    self.current_date_text,
                ],
                spacing=6,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True,
            )
        else:
            time_inner = ft.Column(
                [self.current_time_text, self.current_date_text],
                spacing=1,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True,
            )

        self.clock_container = ft.Container(
            content=time_inner,
            padding=ft.padding.symmetric(horizontal=14, vertical=8),
            alignment=ft.alignment.center,
            bgcolor=GlassMorphism._apply_opacity(colors["SURFACE_VARIANT"], 0.35) if clock_frame_enabled else "transparent",
            border=ft.border.all(1, GlassMorphism._apply_opacity(colors["ON_SURFACE"], 0.14)) if clock_frame_enabled else None,
            border_radius=14,
            on_click=self.core.show_settings,
            tooltip="Нажмите для настройки стиля часов",
        )

        # Навигационный переключатель разделов с плавной анимацией (v2.4)
        active_sec = getattr(self.core, "active_section", "apps")
        section_switcher = ft.Container(
            bgcolor=GlassMorphism._apply_opacity(colors["SURFACE_VARIANT"], 0.35),
            border=ft.border.all(1, GlassMorphism._apply_opacity(colors["ON_SURFACE"], 0.12)),
            border_radius=12,
            padding=3,
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon("grid_view", size=15, color=colors["ON_SURFACE"] if active_sec == "apps" else colors["ON_SURFACE_VARIANT"]),
                                ft.Text("Приложения", size=12, weight=ft.FontWeight.W_600 if active_sec == "apps" else ft.FontWeight.NORMAL, color=colors["ON_SURFACE"] if active_sec == "apps" else colors["ON_SURFACE_VARIANT"]),
                            ],
                            spacing=5,
                        ),
                        bgcolor=GlassMorphism._apply_opacity(colors["ACCENT"], 0.28) if active_sec == "apps" else "transparent",
                        border_radius=9,
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                        on_click=lambda e: self.core.switch_section("apps"),
                    ),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon("insights", size=15, color=colors["ON_SURFACE"] if active_sec == "tracker" else colors["ON_SURFACE_VARIANT"]),
                                ft.Text("Трекер времени", size=12, weight=ft.FontWeight.W_600 if active_sec == "tracker" else ft.FontWeight.NORMAL, color=colors["ON_SURFACE"] if active_sec == "tracker" else colors["ON_SURFACE_VARIANT"]),
                            ],
                            spacing=5,
                        ),
                        bgcolor=GlassMorphism._apply_opacity(colors["ACCENT"], 0.28) if active_sec == "tracker" else "transparent",
                        border_radius=9,
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                        on_click=lambda e: self.core.switch_section("tracker"),
                    ),
                ],
                spacing=4,
                tight=True,
            ),
        )

        # Устройства
        self.devices_container = ft.Container(
            content=self.core.system_monitor.create_devices_header(colors),
            padding=8,
            alignment=ft.alignment.center,
        )

        # Кнопка плагинов
        plugins_button = ft.IconButton(
            icon="extension",
            icon_color=colors["ON_SURFACE"],
            on_click=self.core.show_plugins_manager,
            tooltip="Платформа плагинов и расширений (API 2.4)",
        )

        # Кнопка звука
        current_vol = self.core.audio_controller.get_volume_level()
        self.audio_button = ft.IconButton(
            icon="volume_off" if current_vol == 0 else ("volume_down" if current_vol < 50 else "volume_up"),
            icon_color=colors["ON_SURFACE"],
            on_click=self.core.toggle_volume_slider,
            tooltip="Системная громкость (фоновый контроллер)",
        )

        # Слайдер громкости с поддержкой Mute
        vol_value_label = ft.Text(f"{current_vol}%", size=11, color=colors["ON_SURFACE"], width=34)

        def _handle_vol_slider(ev):
            v = int(ev.control.value)
            vol_value_label.value = f"{v}%"
            if self.audio_button:
                self.audio_button.icon = "volume_off" if v == 0 else ("volume_down" if v < 50 else "volume_up")
                self.audio_button.update()
            vol_value_label.update()
            self.core.on_volume_change(ev)

        def _handle_mute_click(ev):
            if hasattr(self.core.audio_controller, "toggle_mute"):
                muted = self.core.audio_controller.toggle_mute()
                if self.audio_button:
                    self.audio_button.icon = "volume_off" if muted else "volume_up"
                    self.audio_button.icon_color = colors["ERROR"] if muted else colors["ON_SURFACE"]
                    self.audio_button.update()

        self.volume_slider_container = ft.Container(
            content=ft.Row(
                [
                    ft.IconButton(
                        icon="volume_mute",
                        icon_size=16,
                        icon_color=colors["ON_SURFACE_VARIANT"],
                        tooltip="Выключить/включить звук",
                        on_click=_handle_mute_click,
                    ),
                    ft.Container(
                        content=ft.Slider(
                            value=current_vol,
                            min=0,
                            max=100,
                            divisions=100,
                            label="{value}%",
                            on_change=_handle_vol_slider,
                            active_color=colors["ACCENT"],
                            inactive_color=colors["SURFACE_VARIANT"],
                            width=130,
                        ),
                        padding=ft.padding.symmetric(horizontal=2),
                    ),
                    vol_value_label,
                ],
                spacing=2,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=GlassMorphism._apply_opacity(colors["SURFACE_VARIANT"], 0.75),
            blur=GlassMorphism._make_blur(14),
            border=ft.border.all(1, GlassMorphism._apply_opacity(colors["ON_SURFACE"], 0.14)),
            border_radius=12,
            padding=ft.padding.symmetric(horizontal=8, vertical=2),
            visible=self.core.volume_slider_visible,
            animate_opacity=250,
        )

        workspace_button = ft.IconButton(
            icon="rocket_launch",
            icon_color=colors["ACCENT"],
            tooltip="Smart Workspace",
            on_click=self.core.dialogs.show_workspace_manager,
        )

        hud_button = ft.IconButton(
            icon="monitor_heart",
            icon_color=colors["ACCENT"] if self.core.floating_hud_visible else colors["ON_SURFACE"],
            tooltip="Floating HUD",
            on_click=lambda e: self.core.toggle_floating_hud(),
        )

        header_content = [
            ft.Row(
                [
                    workspace_button,
                    ft.Text("Launcher Hab 2.4", size=22, weight=ft.FontWeight.BOLD, color=colors["ON_SURFACE"]),
                    ft.Container(width=10),
                    section_switcher,
                ],
                spacing=8,
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            self.devices_container,
            self.clock_container,
            plugins_button,
            ft.Row([self.audio_button, self.volume_slider_container], spacing=4),
            hud_button,
            ft.IconButton(
                icon="settings",
                icon_color=colors["ON_SURFACE"],
                on_click=self.core.show_settings,
                tooltip="Настройки",
            ),
        ]

        return ft.Container(
            content=ft.Row(header_content, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=GlassMorphism._apply_opacity(colors["SURFACE"], 0.82) if self.core.theme_manager.glass_effect_enabled else colors["SURFACE"],
            blur=GlassMorphism._make_blur(18) if self.core.theme_manager.glass_effect_enabled else None,
            border=ft.border.only(bottom=ft.BorderSide(1, GlassMorphism._apply_opacity(colors["ON_SURFACE"], 0.1))),
            padding=ft.padding.symmetric(horizontal=16, vertical=10),
            margin=0,
        )

    def create_time_elements(self):
        colors = self.core.get_colors()
        clock_style = getattr(self.core.theme_manager, "clock_style", "standard")
        base_size = getattr(self.core.theme_manager, "time_font_size", 20)

        if clock_style == "stacked":
            font_size = max(26, base_size + 8)
        elif clock_style == "pill_glass":
            font_size = max(14, base_size - 2)
        else:
            font_size = base_size

        self.current_time_text = ft.Text(
            "",
            size=font_size,
            font_family="Consolas" if clock_style == "cyber_mono" else getattr(self.core.theme_manager, "time_font_family", self.core.theme_manager.font_family),
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.BOLD,
            color=getattr(self.core.theme_manager, "time_color", colors["ON_SURFACE"]),
        )
        self.current_date_text = ft.Text(
            "",
            size=getattr(self.core.theme_manager, "date_font_size", 12),
            font_family=getattr(self.core.theme_manager, "date_font_family", self.core.theme_manager.font_family),
            text_align=ft.TextAlign.CENTER,
            color=getattr(self.core.theme_manager, "date_color", colors["ON_SURFACE_VARIANT"]),
            visible=getattr(self.core.theme_manager, "show_date", True),
        )

    def create_sidebar(self):
        colors = self.core.get_colors()
        return ft.Container(
            content=self.create_sidebar_content(),
            width=350,
            bgcolor=GlassMorphism._apply_opacity(colors["SURFACE"], 0.72) if self.core.theme_manager.glass_effect_enabled else colors["SURFACE"],
            blur=GlassMorphism._make_blur(18) if self.core.theme_manager.glass_effect_enabled else None,
            padding=0,
            margin=0,
        )

    def create_sidebar_content(self):
        colors = self.core.get_colors()

        self.search_field = ft.TextField(
            hint_text="Поиск приложений...",
            prefix_icon="search",
            filled=True,
            bgcolor=GlassMorphism._apply_opacity(colors["SURFACE_VARIANT"], 0.55),
            border_radius=12,
            on_change=self.core.filter_apps,
            content_padding=14,
            expand=True,
            border_color=GlassMorphism._apply_opacity(colors["ON_SURFACE"], 0.1),
        )

        filter_button = self.create_filter_button()
        self.apps_list = self.create_apps_list()

        return ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon("apps", color=colors["ACCENT"], size=20),
                            ft.Text("Библиотека", size=17, weight=ft.FontWeight.BOLD, color=colors["ON_SURFACE"], expand=True),
                            ft.Text(f"{self.core.get_apps_count()} прил.", size=12, color=colors["ON_SURFACE_VARIANT"]),
                        ]
                    ),
                    padding=ft.padding.only(left=20, right=20, top=16, bottom=6),
                ),
                ft.Container(
                    content=ft.Row([self.search_field, filter_button], spacing=10),
                    padding=ft.padding.symmetric(horizontal=15, vertical=8),
                ),
                ft.Divider(color=GlassMorphism._apply_opacity(colors["ON_SURFACE"], 0.1), height=1),
                ft.Container(content=self.apps_list, expand=True),
                ft.Divider(color=GlassMorphism._apply_opacity(colors["ON_SURFACE"], 0.1), height=1),
                ft.Container(
                    content=self.create_add_app_button(),
                    padding=ft.padding.symmetric(horizontal=15, vertical=10),
                ),
            ]
        )

    def create_apps_list(self):
        apps_list = ft.ListView(expand=True, spacing=4, padding=8)

        all_apps = self.core.app_manager.all_apps + self.core.app_manager.custom_apps
        filtered_apps = self.filter_apps_by_type(all_apps)

        for app in filtered_apps:
            apps_list.controls.append(self.create_app_list_item(app))

        return apps_list

    def create_app_list_item(self, app):
        colors = self.core.get_colors()
        is_installed = self.core.app_manager.is_app_installed(app)
        badge_text = (
            self.core.plugin_manager.get_app_card_badge(app)
            if hasattr(self.core.plugin_manager, "get_app_card_badge")
            else None
        )

        if self.core.theme_manager.advanced_glass_enabled:
            bg_color = self._with_opacity(colors["SURFACE"], self.core.theme_manager.advanced_glass_opacity)
        else:
            bg_color = GlassMorphism._apply_opacity(colors["SURFACE_VARIANT"], 0.25)

        subtitle_str = f"{app['category']} • {badge_text}" if badge_text else f"{app['category']} • {'Установлено' if is_installed else 'Не установлено'}"

        app_item = ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(
                            app["icon"],
                            color=colors["WEB_BLUE"]
                            if app["type"] == "web"
                            else (colors["ON_SURFACE"] if is_installed else colors["ERROR"]),
                            size=26,
                        ),
                        width=46,
                        height=46,
                        alignment=ft.alignment.center,
                        bgcolor=GlassMorphism._apply_opacity(colors["SURFACE"], 0.45),
                        border=ft.border.all(1, GlassMorphism._apply_opacity(colors["ON_SURFACE"], 0.12)),
                        border_radius=12,
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                f"{app['name']} — {badge_text}" if badge_text and app.get("category") == "Games" else app["name"],
                                color=colors["ON_SURFACE"] if is_installed else colors["ERROR"],
                                size=13,
                                weight=ft.FontWeight.W_600,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            ft.Text(
                                subtitle_str,
                                color=colors["ON_SURFACE_VARIANT"] if is_installed else colors["ERROR"],
                                size=11,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                        ],
                        expand=True,
                        spacing=2,
                    ),
                    ft.IconButton(
                        icon="more_vert",
                        icon_size=18,
                        icon_color=colors["ON_SURFACE_VARIANT"],
                        on_click=lambda e, app=app: self.core.show_app_menu_dialog(app),
                        tooltip="Меню приложения",
                        style=ft.ButtonStyle(padding=ft.padding.all(6), bgcolor="transparent"),
                    ),
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=12, vertical=10),
            border_radius=12,
            border=ft.border.all(1, GlassMorphism._apply_opacity(colors["ON_SURFACE"], 0.08)),
            on_click=lambda e, app=app: self.core.launch_app(app),
            tooltip=f"Запустить {app['name']}",
            bgcolor=bg_color,
            margin=ft.margin.symmetric(vertical=2),
            animate=ft.Animation(180, ft.AnimationCurve.EASE_OUT),
        )

        def on_hover(e):
            if e.data == "true":
                app_item.bgcolor = GlassMorphism._apply_opacity(colors["ACCENT"], 0.18)
                app_item.border = ft.border.all(1, GlassMorphism._apply_opacity(colors["ACCENT"], 0.4))
            else:
                app_item.bgcolor = bg_color
                app_item.border = ft.border.all(1, GlassMorphism._apply_opacity(colors["ON_SURFACE"], 0.08))
            app_item.update()

        app_item.on_hover = on_hover
        return app_item

    def create_add_app_button(self):
        colors = self.core.get_colors()
        bg_color = GlassMorphism._apply_opacity(colors["ACCENT"], 0.14)

        add_button = ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon("add", color=colors["ACCENT"], size=26),
                        width=48,
                        height=48,
                        alignment=ft.alignment.center,
                        bgcolor=GlassMorphism._apply_opacity(colors["ACCENT"], 0.22),
                        border_radius=12,
                    ),
                    ft.Column(
                        [
                            ft.Text("Добавить приложение", color=colors["ON_SURFACE"], size=14, weight=ft.FontWeight.W_600),
                            ft.Text("EXE, URI или веб-сервис + трекер", color=colors["ON_SURFACE_VARIANT"], size=11),
                        ],
                        expand=True,
                        spacing=2,
                    ),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=14, vertical=10),
            border_radius=12,
            border=ft.border.all(1, GlassMorphism._apply_opacity(colors["ACCENT"], 0.35)),
            on_click=self.core.show_add_custom_app_dialog,
            tooltip="Добавить новое приложение",
            bgcolor=bg_color,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )

        def on_hover(e):
            if e.data == "true":
                add_button.bgcolor = GlassMorphism._apply_opacity(colors["ACCENT"], 0.26)
            else:
                add_button.bgcolor = bg_color
            add_button.update()

        add_button.on_hover = on_hover
        return add_button

    def create_filter_button(self):
        colors = self.core.get_colors()
        filter_btn = ft.Container(
            content=ft.Icon("filter_list", color=colors["ON_SURFACE"], size=20),
            width=44,
            height=44,
            alignment=ft.alignment.center,
            bgcolor=GlassMorphism._apply_opacity(colors["SURFACE_VARIANT"], 0.55),
            border=ft.border.all(1, GlassMorphism._apply_opacity(colors["ON_SURFACE"], 0.1)),
            border_radius=12,
            on_click=self.core.show_filter_menu,
            tooltip="Фильтровать по типу",
        )
        return filter_btn

    def create_main_content(self):
        """Оборачивает основной контент в ft.AnimatedSwitcher для плавной анимации переходов между разделами."""
        inner = self.create_main_content_internal()
        self.animated_switcher = ft.AnimatedSwitcher(
            content=inner,
            transition=ft.AnimatedSwitcherTransition.FADE,
            duration=300,
            reverse_duration=220,
            switch_in_curve=ft.AnimationCurve.EASE_OUT_CUBIC,
            switch_out_curve=ft.AnimationCurve.EASE_IN_CUBIC,
        )
        return ft.Container(
            content=self.animated_switcher,
            expand=True,
            padding=10,
            margin=0,
        )

    def create_main_content_internal(self):
        colors = self.core.get_colors()

        # Если открыта вкладка «Трекер времени» (Game & App Session Tracker)
        if getattr(self.core, "active_section", "apps") == "tracker":
            tracker_ui = None
            if hasattr(self.core.plugin_manager, "get_plugin_ui"):
                tracker_ui = self.core.plugin_manager.get_plugin_ui("session_tracker_plugin")
            if not tracker_ui:
                from plugins.session_tracker_plugin import GameAppSessionTrackerPlugin
                temp_plugin = GameAppSessionTrackerPlugin()
                temp_plugin.set_context(self.core)
                tracker_ui = temp_plugin.get_ui_component()

            tracker_card = GlassMorphism.create_card(
                tracker_ui,
                colors,
                hover_effect=False,
                intensity=self.core.theme_manager.glass_intensity,
                custom_opacity=self.core.theme_manager.advanced_glass_opacity if self.core.theme_manager.advanced_glass_enabled else None,
            )
            return ft.Container(
                key="section_tracker",
                content=ft.Column([tracker_card], scroll=ft.ScrollMode.ADAPTIVE),
                expand=True,
            )

        favorites_content = self.create_favorites_panel()
        category_sections = self.create_category_sections()

        main_content_list = [favorites_content]

        if category_sections:
            main_content_list.extend(category_sections)
        elif self.core.current_filter != "all":
            no_apps_content = ft.Column(
                [
                    ft.Icon("search_off", size=64, color=colors["ON_SURFACE_VARIANT"]),
                    ft.Text("Нет приложений по выбранному фильтру", size=18, color=colors["ON_SURFACE_VARIANT"], weight=ft.FontWeight.W_500),
                    ft.Text("Попробуйте выбрать другой фильтр или добавьте свои приложения", size=14, color=colors["ON_SURFACE_VARIANT"]),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            )
            no_apps_card = (
                GlassMorphism.create_card(no_apps_content, colors, hover_effect=False, intensity=self.core.theme_manager.glass_intensity)
                if self.core.theme_manager.glass_effect_enabled
                else ft.Container(content=no_apps_content, padding=80, alignment=ft.alignment.center)
            )
            main_content_list.append(no_apps_card)

        main_column = ft.Column(main_content_list, scroll=ft.ScrollMode.ADAPTIVE)

        if self.core.floating_hud_visible:
            perf = self.core.system_monitor.get_performance_info()
            self.core.floating_hud_cpu_text = ft.Text(f"CPU {perf['cpu']}%", size=11, color=colors["ON_SURFACE"])
            self.core.floating_hud_ram_text = ft.Text(f"RAM {perf['ram']}%", size=11, color=colors["ON_SURFACE"])
            self.core.floating_hud_apps_text = ft.Text(f"Избранных: {len(self.core.app_manager.favorite_apps)}", size=11, color=colors["ON_SURFACE"])
            hud = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Floating HUD 2.4", weight=ft.FontWeight.BOLD, size=12, color=colors["ACCENT"]),
                        self.core.floating_hud_cpu_text,
                        self.core.floating_hud_ram_text,
                        self.core.floating_hud_apps_text,
                    ],
                    spacing=2,
                ),
                right=14,
                top=14,
                padding=12,
                bgcolor=GlassMorphism._apply_opacity(colors["SURFACE"], 0.65),
                blur=GlassMorphism._make_blur(18),
                border_radius=14,
                border=ft.border.all(1, GlassMorphism._apply_opacity(colors["ON_SURFACE"], 0.18)),
            )
            return ft.Container(key=f"section_apps_{self.core.current_filter}_hud", content=ft.Stack([main_column, hud]), expand=True)

        self.core.floating_hud_cpu_text = None
        self.core.floating_hud_ram_text = None
        self.core.floating_hud_apps_text = None
        return ft.Container(key=f"section_apps_{self.core.current_filter}", content=main_column, expand=True)

    def create_favorites_panel(self):
        colors = self.core.get_colors()
        favorite_apps = self.core.app_manager.favorite_apps

        favorites_counter = ft.Container(
            content=ft.Text(
                f"{len(favorite_apps)}/10",
                size=12,
                color=colors["ON_SURFACE_VARIANT"],
                weight=ft.FontWeight.W_500,
            ),
            bgcolor=GlassMorphism._apply_opacity(colors["SURFACE_VARIANT"], 0.45),
            padding=ft.padding.symmetric(horizontal=10, vertical=4),
            border_radius=8,
        )

        if not favorite_apps:
            empty_content = ft.Column(
                [
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon("star", color=colors["ACCENT"], size=20),
                                ft.Text("Избранное", size=16, weight=ft.FontWeight.BOLD, color=colors["ON_SURFACE"]),
                                favorites_counter,
                            ]
                        ),
                        padding=ft.padding.symmetric(horizontal=15, vertical=10),
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Icon("star_border", size=32, color=colors["ON_SURFACE_VARIANT"]),
                                ft.Text("Добавьте приложения в избранное", size=12, color=colors["ON_SURFACE_VARIANT"], text_align=ft.TextAlign.CENTER),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=8,
                        ),
                        padding=15,
                        alignment=ft.alignment.center,
                    ),
                ]
            )
            return (
                GlassMorphism.create_card(empty_content, colors, hover_effect=False, intensity=self.core.theme_manager.glass_intensity)
                if self.core.theme_manager.glass_effect_enabled
                else ft.Container(content=empty_content, bgcolor=colors["SURFACE"], border_radius=12, margin=ft.margin.symmetric(horizontal=10, vertical=5))
            )

        favorites_grid = ft.GridView(
            runs_count=6,
            max_extent=130,
            child_aspect_ratio=0.86,
            spacing=15,
            run_spacing=20,
            padding=16,
        )

        for app in favorite_apps:
            is_installed = self.core.app_manager.is_app_installed(app)
            badge = (
                self.core.plugin_manager.get_app_card_badge(app)
                if hasattr(self.core.plugin_manager, "get_app_card_badge")
                else None
            )
            running = (
                self.core.plugin_manager.is_app_running(app)
                if hasattr(self.core.plugin_manager, "is_app_running")
                else False
            )

            app_container = GlassMorphism.create_app_button(
                app=app,
                colors=colors,
                is_installed=is_installed,
                is_favorite=True,
                glass_effect=self.core.theme_manager.glass_effect_enabled,
                on_click=lambda e, app=app: self.core.launch_app(app),
                on_long_press=lambda e, app=app: self.core.show_favorite_app_menu_dialog(app),
                session_badge_text=badge,
                is_running=running,
                intensity=self.core.theme_manager.glass_intensity,
            )

            def create_hover_handler(button):
                def on_hover(e):
                    if e.data == "true":
                        button.scale = 1.05
                    else:
                        button.scale = 1.0
                    button.update()
                return on_hover

            app_container.on_hover = create_hover_handler(app_container)
            favorites_grid.controls.append(app_container)

        favorites_content = ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon("star", color=colors["ACCENT"], size=20),
                            ft.Text("Избранное", size=18, weight=ft.FontWeight.BOLD, color=colors["ON_SURFACE"]),
                            favorites_counter,
                        ]
                    ),
                    padding=ft.padding.symmetric(horizontal=15, vertical=6),
                ),
                favorites_grid,
            ]
        )

        return (
            GlassMorphism.create_card(
                favorites_content,
                colors,
                hover_effect=False,
                intensity=self.core.theme_manager.glass_intensity,
                custom_opacity=self.core.theme_manager.advanced_glass_opacity if self.core.theme_manager.advanced_glass_enabled else None,
            )
            if self.core.theme_manager.glass_effect_enabled
            else ft.Container(content=favorites_content, bgcolor=colors["SURFACE"], border_radius=12, margin=ft.margin.symmetric(horizontal=10, vertical=5))
        )

    def create_category_sections(self):
        colors = self.core.get_colors()
        all_available_apps = self.core.app_manager.all_apps + self.core.app_manager.custom_apps
        filtered_apps = self.filter_apps_by_type(all_available_apps)

        categories = {}
        for app in filtered_apps:
            if app["category"] not in categories:
                categories[app["category"]] = []
            categories[app["category"]].append(app)

        category_sections = []
        for category, apps in categories.items():
            if apps:
                apps_grid = ft.GridView(
                    runs_count=6,
                    max_extent=130,
                    child_aspect_ratio=0.86,
                    spacing=15,
                    run_spacing=20,
                    padding=16,
                )

                for app in apps:
                    is_installed = self.core.app_manager.is_app_installed(app)
                    badge = (
                        self.core.plugin_manager.get_app_card_badge(app)
                        if hasattr(self.core.plugin_manager, "get_app_card_badge")
                        else None
                    )
                    running = (
                        self.core.plugin_manager.is_app_running(app)
                        if hasattr(self.core.plugin_manager, "is_app_running")
                        else False
                    )

                    app_button = GlassMorphism.create_app_button(
                        app,
                        colors,
                        is_installed,
                        glass_effect=self.core.theme_manager.glass_effect_enabled,
                        on_click=lambda e, app=app: self.core.launch_app(app),
                        on_long_press=lambda e, app=app: self.core.show_app_menu_dialog(app),
                        session_badge_text=badge,
                        is_running=running,
                        intensity=self.core.theme_manager.glass_intensity,
                    )

                    def create_hover_handler(button):
                        def on_hover(e):
                            if e.data == "true":
                                button.scale = 1.05
                            else:
                                button.scale = 1.0
                            button.update()
                        return on_hover

                    app_button.on_hover = create_hover_handler(app_button)
                    apps_grid.controls.append(app_button)

                category_header = ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(self.get_category_icon(category), color=colors["ACCENT"], size=20),
                            ft.Text(category, size=18, weight=ft.FontWeight.BOLD, color=colors["ON_SURFACE"]),
                            ft.Container(
                                content=ft.Text(f"{len(apps)}", size=12, color=colors["ON_SURFACE_VARIANT"], weight=ft.FontWeight.W_500),
                                bgcolor=GlassMorphism._apply_opacity(colors["SURFACE_VARIANT"], 0.45),
                                padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                border_radius=10,
                            ),
                        ]
                    ),
                    padding=ft.padding.only(left=16, top=8, bottom=6, right=16),
                )

                category_content = ft.Column([category_header, apps_grid])

                if self.core.theme_manager.glass_effect_enabled:
                    category_card = GlassMorphism.create_card(
                        category_content,
                        colors,
                        hover_effect=False,
                        intensity=self.core.theme_manager.glass_intensity,
                        custom_opacity=self.core.theme_manager.advanced_glass_opacity if self.core.theme_manager.advanced_glass_enabled else None,
                    )
                else:
                    category_card = ft.Container(
                        content=category_content,
                        shadow=ft.BoxShadow(blur_radius=8, color=colors["GLASS_SHADOW"], offset=ft.Offset(0, 2)),
                        margin=ft.margin.only(bottom=20),
                        border_radius=14,
                        bgcolor=colors["SURFACE"],
                    )

                category_sections.append(category_card)

        return category_sections

    def filter_apps_by_type(self, apps_list):
        if self.core.current_filter == "all":
            return apps_list
        elif self.core.current_filter == "web":
            return [app for app in apps_list if app["type"] == "web"]
        elif self.core.current_filter == "app":
            return [app for app in apps_list if app["type"] == "app"]
        elif self.core.current_filter == "system":
            return [app for app in apps_list if app["type"] == "system"]
        elif self.core.current_filter == "custom":
            return [app for app in apps_list if app in self.core.app_manager.custom_apps]
        return apps_list

    def get_category_icon(self, category):
        icons = {
            "Browser": "web",
            "Media": "play_arrow",
            "Music": "music_note",
            "Social": "groups",
            "Games": "sports_esports",
            "System": "computer",
            "Office": "work",
            "Cloud": "cloud",
            "Health": "medical_services",
            "Government": "verified_user",
            "Utilities": "apps",
            "Development": "code",
        }
        return icons.get(category, "apps")

    def show_search_results(self, results, query):
        colors = self.core.get_colors()

        if not results:
            no_results_content = ft.Column(
                [
                    ft.Icon("search_off", size=64, color=colors["ON_SURFACE_VARIANT"]),
                    ft.Text("Ничего не найдено", size=18, color=colors["ON_SURFACE_VARIANT"], weight=ft.FontWeight.W_500),
                    ft.Text(f"По запросу: '{query}'", size=14, color=colors["ON_SURFACE_VARIANT"]),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            )
            new_view = ft.Container(
                key=f"search_empty_{query}",
                content=ft.Column(
                    [
                        self.create_favorites_panel(),
                        GlassMorphism.create_card(no_results_content, colors, hover_effect=False)
                        if self.core.theme_manager.glass_effect_enabled
                        else ft.Container(content=no_results_content, padding=80, alignment=ft.alignment.center),
                    ],
                    scroll=ft.ScrollMode.ADAPTIVE,
                ),
            )
        else:
            results_header = ft.Container(
                content=ft.Row(
                    [
                        ft.Icon("search", color=colors["ACCENT"], size=20),
                        ft.Text("Результаты поиска", size=18, weight=ft.FontWeight.BOLD, color=colors["ON_SURFACE"]),
                        ft.Container(
                            content=ft.Text(f"{len(results)} найдено", size=12, color=colors["ON_SURFACE_VARIANT"]),
                            bgcolor=colors["SURFACE_VARIANT"],
                            padding=ft.padding.symmetric(horizontal=10, vertical=4),
                            border_radius=12,
                        ),
                    ]
                ),
                padding=ft.padding.only(left=20, top=12, bottom=10, right=20),
            )

            results_grid = ft.GridView(
                runs_count=6,
                max_extent=130,
                child_aspect_ratio=0.86,
                spacing=15,
                run_spacing=20,
                padding=16,
            )

            for app in results:
                is_installed = self.core.app_manager.is_app_installed(app)
                badge = (
                    self.core.plugin_manager.get_app_card_badge(app)
                    if hasattr(self.core.plugin_manager, "get_app_card_badge")
                    else None
                )
                app_button = GlassMorphism.create_app_button(
                    app,
                    colors,
                    is_installed,
                    glass_effect=self.core.theme_manager.glass_effect_enabled,
                    on_click=lambda e, app=app: self.core.launch_app(app),
                    session_badge_text=badge,
                    intensity=self.core.theme_manager.glass_intensity,
                )
                results_grid.controls.append(app_button)

            search_results_content = ft.Column([results_header, results_grid])
            search_card = (
                GlassMorphism.create_card(search_results_content, colors, hover_effect=False, intensity=self.core.theme_manager.glass_intensity)
                if self.core.theme_manager.glass_effect_enabled
                else ft.Container(content=search_results_content, border_radius=12, bgcolor=colors["SURFACE"])
            )

            new_view = ft.Container(
                key=f"search_results_{query}",
                content=ft.Column([self.create_favorites_panel(), search_card], scroll=ft.ScrollMode.ADAPTIVE),
            )

        if self.animated_switcher:
            self.animated_switcher.content = new_view
        else:
            self.core.main_content.content = new_view

        if hasattr(self.core, "page"):
            self.core.page.update()

    def create_loading_progress(self):
        colors = self.core.get_colors()
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon("rocket_launch", size=40, color=colors["ACCENT"]),
                    ft.Text("Запуск приложения...", size=14, color=colors["ON_SURFACE"], weight=ft.FontWeight.W_500),
                    ft.Container(
                        content=ft.ProgressBar(value=0, color=colors["ACCENT"], bgcolor=colors["SURFACE_VARIANT"], height=8, border_radius=4),
                        width=250,
                        padding=ft.padding.only(top=10),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor=colors["SURFACE"],
            border_radius=15,
            padding=25,
            visible=False,
            width=320,
            height=140,
            top=100,
            alignment=ft.alignment.top_center,
            shadow=ft.BoxShadow(blur_radius=15, color=colors["GLASS_SHADOW"], offset=ft.Offset(0, 5)),
        )