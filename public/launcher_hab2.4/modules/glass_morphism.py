# [file name]: glass_morphism.py
import flet as ft


class GlassMorphism:
    """Улучшенный модуль прозрачного стекла (Glassmorphism 2.4) с реальным размытием ft.Blur и плавной анимацией."""

    GLASS_STYLES = {
        "light": {
            "bg_blur": 8,
            "bg_opacity": 0.12,
            "border_opacity": 0.16,
            "highlight_opacity": 0.08,
            "shadow_blur": 12,
        },
        "medium": {
            "bg_blur": 16,
            "bg_opacity": 0.20,
            "border_opacity": 0.24,
            "highlight_opacity": 0.14,
            "shadow_blur": 20,
        },
        "strong": {
            "bg_blur": 28,
            "bg_opacity": 0.30,
            "border_opacity": 0.34,
            "highlight_opacity": 0.20,
            "shadow_blur": 28,
        },
    }

    @staticmethod
    def _apply_opacity(color: str, opacity: float) -> str:
        """Применяет прозрачность (0.0 - 1.0) к HEX цвету (#RRGGBB или #RRGGBBAA)."""
        if not isinstance(color, str):
            return "#2d2d2d33"
        clean = color.strip()
        if clean.startswith("#"):
            if len(clean) == 9:
                clean = clean[:7]
            if len(clean) == 7:
                alpha = max(0, min(255, int(round(opacity * 255))))
                return f"{clean}{alpha:02x}"
        return color

    @staticmethod
    def _make_blur(sigma: float):
        """Создает объект размытия Flet с защитой от старых версий."""
        try:
            return ft.Blur(sigma, sigma, ft.BlurTileMode.MIRROR)
        except Exception:
            return None

    @staticmethod
    def create_container(
        content,
        colors,
        intensity="medium",
        border=True,
        shadow=True,
        border_radius=18,
        padding=16,
        margin=5,
        custom_opacity=None,
    ):
        """Создание контейнера с настоящим эффектом прозрачного матового стекла."""
        style = GlassMorphism.GLASS_STYLES.get(intensity, GlassMorphism.GLASS_STYLES["medium"])
        opacity = (custom_opacity / 100.0) if custom_opacity is not None else style["bg_opacity"]

        bg_color = GlassMorphism._apply_opacity(colors.get("SURFACE", "#2d2d2d"), opacity)
        border_color = (
            GlassMorphism._apply_opacity(colors.get("ON_SURFACE", "#ffffff"), style["border_opacity"])
            if border
            else None
        )

        container = ft.Container(
            content=content,
            bgcolor=bg_color,
            blur=GlassMorphism._make_blur(style["bg_blur"]),
            border=ft.border.all(1, border_color) if border else None,
            border_radius=border_radius,
            padding=padding,
            margin=margin,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=style["shadow_blur"],
                color=colors.get("GLASS_SHADOW", "#00000040"),
                offset=ft.Offset(0, 6),
            )
            if shadow
            else None,
            animate=ft.Animation(280, ft.AnimationCurve.EASE_OUT_CUBIC),
            animate_opacity=ft.Animation(240, ft.AnimationCurve.EASE_IN_OUT),
            animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )
        return container

    @staticmethod
    def create_app_button(
        app,
        colors,
        is_installed,
        is_favorite=False,
        glass_effect=True,
        on_click=None,
        on_long_press=None,
        session_badge_text=None,
        is_running=False,
        intensity="medium",
    ):
        """Создание карточки-плитки приложения с поддержкой бейджа трекера времени и прозрачного стекла."""
        style = GlassMorphism.GLASS_STYLES.get(intensity, GlassMorphism.GLASS_STYLES["medium"])

        if app.get("type") == "web":
            icon_color = colors.get("WEB_BLUE", colors["ACCENT"])
        else:
            icon_color = colors["ON_SURFACE"] if is_installed else colors["ERROR"]

        if glass_effect:
            tile_bg = GlassMorphism._apply_opacity(colors["SURFACE"], style["bg_opacity"])
            tile_border = ft.border.all(
                1,
                colors["ACCENT"]
                if is_running
                else GlassMorphism._apply_opacity(colors["ON_SURFACE"], style["border_opacity"]),
            )
            tile_blur = GlassMorphism._make_blur(style["bg_blur"])
        else:
            tile_bg = GlassMorphism._apply_opacity(colors["SURFACE_VARIANT"], 0.25)
            tile_border = ft.border.all(1, colors["ACCENT"]) if is_running else None
            tile_blur = None

        status_icon = (
            ft.Icon(name="play_circle_fill", size=16, color=colors["SUCCESS"])
            if is_running
            else (
                ft.Icon(name="star", size=16, color=colors["ACCENT"])
                if is_favorite
                else ft.Icon(
                    name="check_circle" if is_installed else "error",
                    size=15,
                    color=colors["SUCCESS"] if is_installed else colors["ERROR"],
                )
            )
        )

        icon_container = ft.Container(
            content=ft.Stack(
                [
                    ft.Container(
                        content=ft.Icon(name=app.get("icon", "apps"), size=38, color=icon_color),
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        content=status_icon,
                        alignment=ft.alignment.bottom_right,
                        padding=ft.padding.only(right=4, bottom=4),
                    ),
                ]
            ),
            width=76,
            height=76,
            alignment=ft.alignment.center,
            bgcolor=tile_bg,
            blur=tile_blur,
            border_radius=16,
            border=tile_border,
            shadow=ft.BoxShadow(
                blur_radius=12,
                color=colors.get("GLASS_SHADOW", "#00000035"),
                offset=ft.Offset(0, 4),
            ),
            animate=ft.Animation(220, ft.AnimationCurve.EASE_OUT),
        )

        subtitle_controls = [
            ft.Text(
                app.get("name", "App"),
                size=12,
                weight=ft.FontWeight.W_600,
                color=icon_color,
                text_align=ft.TextAlign.CENTER,
                max_lines=1,
                overflow=ft.TextOverflow.ELLIPSIS,
            )
        ]

        if session_badge_text:
            subtitle_controls.append(
                ft.Text(
                    session_badge_text,
                    size=10,
                    color=colors["ACCENT"] if is_running else colors["ON_SURFACE_VARIANT"],
                    text_align=ft.TextAlign.CENTER,
                    max_lines=1,
                    overflow=ft.TextOverflow.ELLIPSIS,
                )
            )
        else:
            subtitle_controls.append(
                ft.Text(
                    app.get("type", "app").upper(),
                    size=9,
                    color=colors["ON_SURFACE_VARIANT"],
                    text_align=ft.TextAlign.CENTER,
                )
            )

        app_content = ft.Column(
            [
                icon_container,
                ft.Container(
                    content=ft.Column(
                        subtitle_controls,
                        spacing=1,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    height=38,
                    alignment=ft.alignment.top_center,
                    padding=ft.padding.only(top=4),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
            height=124,
        )

        tooltip_lines = [f"Запустить {app.get('name', '')}"]
        if session_badge_text:
            tooltip_lines.append(f"Активность: {session_badge_text}")

        app_container = ft.Container(
            content=app_content,
            width=116,
            height=142,
            padding=8,
            on_click=on_click,
            on_long_press=on_long_press,
            tooltip="\n".join(tooltip_lines),
            border_radius=14,
            bgcolor="transparent",
            scale=1.0,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            animate_scale=ft.Animation(180, ft.AnimationCurve.EASE_OUT),
        )

        return app_container

    @staticmethod
    def create_card(content, colors, hover_effect=True, intensity="medium", custom_opacity=None):
        """Создание секционной карточки с настоящим прозрачным стеклом (Glassmorphism 2.4)."""
        style = GlassMorphism.GLASS_STYLES.get(intensity, GlassMorphism.GLASS_STYLES["medium"])
        opacity = (custom_opacity / 100.0) if custom_opacity is not None else style["bg_opacity"]

        base_bg = GlassMorphism._apply_opacity(colors.get("SURFACE", "#2d2d2d"), opacity)
        base_border = GlassMorphism._apply_opacity(colors.get("ON_SURFACE", "#ffffff"), style["border_opacity"])

        card = ft.Container(
            content=content,
            bgcolor=base_bg,
            blur=GlassMorphism._make_blur(style["bg_blur"]),
            border=ft.border.all(1.2, base_border),
            border_radius=20,
            padding=20,
            margin=10,
            scale=1.0,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=style["shadow_blur"],
                color=colors.get("GLASS_SHADOW", "#00000040"),
                offset=ft.Offset(0, 8),
            ),
            animate=ft.Animation(280, ft.AnimationCurve.EASE_OUT_CUBIC),
            animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )

        if hover_effect:
            def on_hover(e):
                if e.data == "true":
                    card.scale = 1.01
                    card.bgcolor = GlassMorphism._apply_opacity(colors["ACCENT"], 0.14)
                    card.border = ft.border.all(1.2, GlassMorphism._apply_opacity(colors["ACCENT"], 0.45))
                else:
                    card.scale = 1.0
                    card.bgcolor = base_bg
                    card.border = ft.border.all(1.2, base_border)
                card.update()

            card.on_hover = on_hover

        return card