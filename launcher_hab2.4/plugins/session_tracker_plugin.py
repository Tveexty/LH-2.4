# [file name]: plugins/session_tracker_plugin.py
import json
import os
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional
import flet as ft

try:
    import psutil
except ImportError:
    psutil = None


class GameAppSessionTrackerPlugin:
    """
    Плагин «Game & App Session Tracker» (Трекер активности и игрового времени) для Launcher Hab 2.4.
    Суть: Отслеживает, сколько времени пользователь проводит в каждом запущенном приложении или игре
    (аналог статистики Steam или «Экранного времени»).

    Функционал:
    - Отображение общего времени в карточке приложения (например: «Steam — 42 ч в месяц»).
    - Графики активности на день, неделю или месяц в окне плагина или на отдельной вкладке.
    - Уведомления при превышении лимита (для групп цифрового детокса).
    """

    PLUGIN_META = {
        "id": "session_tracker_plugin",
        "name": "Game & App Session Tracker",
        "version": "2.4.0",
        "author": "Launcher Hab Team",
        "description": "Трекер игрового и экранного времени: бейджи на карточках («42 ч в месяц»), графики на день/неделю/месяц и лимиты цифрового детокса.",
        "icon": "insights",
    }

    def __init__(self):
        self.context = None
        self.api = None
        self.data_file = Path("session_tracker_data.json")
        self.active_sessions: Dict[str, float] = {}  # package -> timestamp старта
        self.notified_limits_today: set = set()
        self.selected_period = "month"  # "day" | "week" | "month"
        self.data = self._load_data()

    def _default_data(self) -> Dict[str, Any]:
        today = datetime.now().strftime("%Y-%m-%d")
        return {
            "apps": {
                "steam": {
                    "name": "Steam",
                    "category": "Games",
                    "month_minutes": 2520,  # 42 ч в месяц
                    "week_minutes": 840,    # 14 ч в неделю
                    "today_minutes": 95,
                    "daily_limit_minutes": 180,
                    "detox_group": "Игры",
                },
                "chrome": {
                    "name": "Chrome",
                    "category": "Browser",
                    "month_minutes": 1980,  # 33 ч в месяц
                    "week_minutes": 520,
                    "today_minutes": 75,
                    "daily_limit_minutes": 240,
                    "detox_group": "Браузеры",
                },
                "telegram": {
                    "name": "Telegram",
                    "category": "Social",
                    "month_minutes": 1140,  # 19 ч в месяц
                    "week_minutes": 310,
                    "today_minutes": 52,
                    "daily_limit_minutes": 60,
                    "detox_group": "Соцсети и мессенджеры",
                },
                "vk": {
                    "name": "VK",
                    "category": "Social",
                    "month_minutes": 660,   # 11 ч в месяц
                    "week_minutes": 175,
                    "today_minutes": 35,
                    "daily_limit_minutes": 60,
                    "detox_group": "Соцсети и мессенджеры",
                },
                "vlc": {
                    "name": "VLC",
                    "category": "Media",
                    "month_minutes": 480,   # 8 ч в месяц
                    "week_minutes": 120,
                    "today_minutes": 20,
                    "daily_limit_minutes": 180,
                    "detox_group": "Медиа",
                },
                "youtube": {
                    "name": "YouTube",
                    "category": "Media",
                    "month_minutes": 1560,  # 26 ч в месяц
                    "week_minutes": 410,
                    "today_minutes": 65,
                    "daily_limit_minutes": 90,
                    "detox_group": "Медиа",
                },
            },
            "detox_groups": {
                "Игры": {"daily_limit_minutes": 180, "enabled": True},
                "Соцсети и мессенджеры": {"daily_limit_minutes": 90, "enabled": True},
                "Медиа": {"daily_limit_minutes": 120, "enabled": True},
                "Браузеры": {"daily_limit_minutes": 240, "enabled": False},
            },
            "daily_history": {
                "Пн": 210,
                "Вт": 185,
                "Ср": 260,
                "Чт": 195,
                "Пт": 310,
                "Сб": 390,
                "Вс": 277,
            },
            "last_updated_date": today,
        }

    def _load_data(self) -> Dict[str, Any]:
        try:
            if self.data_file.exists():
                with self.data_file.open("r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    if isinstance(loaded, dict) and "apps" in loaded:
                        return loaded
        except Exception:
            pass
        default = self._default_data()
        self._save_data(default)
        return default

    def _save_data(self, data: Optional[Dict[str, Any]] = None):
        target = data or self.data
        try:
            with self.data_file.open("w", encoding="utf-8") as f:
                json.dump(target, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def set_context(self, context):
        self.context = context

    def on_load(self, api):
        self.api = api
        self.context = getattr(api, "core", self.context)

    def cleanup(self):
        # Завершаем активные сессии при выгрузке
        for pkg in list(self.active_sessions.keys()):
            self.stop_session(pkg)
        self._save_data()

    # --- Хуки жизненного цикла приложений ---
    def on_app_launched(self, app: Dict[str, Any]):
        pkg = str(app.get("package", app.get("name", "app"))).lower()
        name = app.get("name", pkg)
        category = app.get("category", "Custom")

        if pkg not in self.data["apps"]:
            self.data["apps"][pkg] = {
                "name": name,
                "category": category,
                "month_minutes": 0,
                "week_minutes": 0,
                "today_minutes": 0,
                "daily_limit_minutes": 120 if category == "Games" else 180,
                "detox_group": "Игры" if category == "Games" else ("Соцсети и мессенджеры" if category == "Social" else "Браузеры"),
            }

        self.active_sessions[pkg] = time.time()
        self._check_detox_limits(pkg)
        self._save_data()

    def stop_session(self, package: str):
        pkg = package.lower()
        if pkg in self.active_sessions:
            started_at = self.active_sessions.pop(pkg)
            elapsed_min = max(1, int((time.time() - started_at) / 60))
            self.add_minutes(pkg, elapsed_min)

    def add_minutes(self, package: str, minutes: int, app_name: str = None, category: str = "Games"):
        pkg = package.lower()
        if pkg not in self.data["apps"]:
            self.data["apps"][pkg] = {
                "name": app_name or package,
                "category": category,
                "month_minutes": 0,
                "week_minutes": 0,
                "today_minutes": 0,
                "daily_limit_minutes": 120,
                "detox_group": "Игры" if category == "Games" else "Медиа",
            }
        entry = self.data["apps"][pkg]
        entry["today_minutes"] = int(entry.get("today_minutes", 0)) + minutes
        entry["week_minutes"] = int(entry.get("week_minutes", 0)) + minutes
        entry["month_minutes"] = int(entry.get("month_minutes", 0)) + minutes
        self._save_data()
        self._check_detox_limits(pkg)

    def on_tick(self):
        """Вызывается раз в минуту фоновым монитором для учета открытых процессов."""
        now = time.time()
        # Проверяем запущенные сессии и процессы ОС через psutil
        if psutil is not None:
            try:
                running_names = {p.info["name"].lower().replace(".exe", "") for p in psutil.process_iter(["name"]) if p.info.get("name")}
                for pkg in list(self.data.get("apps", {}).keys()):
                    if pkg in running_names and pkg not in self.active_sessions:
                        self.active_sessions[pkg] = now
            except Exception:
                pass

        for pkg, start_ts in list(self.active_sessions.items()):
            if now - start_ts >= 60:
                self.active_sessions[pkg] = now
                self.add_minutes(pkg, 1)

    def _check_detox_limits(self, package: str):
        """Проверка превышения лимита приложения или группы детокса и отправка уведомления."""
        pkg = package.lower()
        app_entry = self.data["apps"].get(pkg)
        if not app_entry:
            return

        today_min = int(app_entry.get("today_minutes", 0))
        app_limit = int(app_entry.get("daily_limit_minutes", 0))
        group_name = app_entry.get("detox_group", "")

        # 1. Индивидуальный лимит приложения
        if app_limit > 0 and today_min >= app_limit and f"app_{pkg}" not in self.notified_limits_today:
            self.notified_limits_today.add(f"app_{pkg}")
            self._notify(
                f"⚠️ Лимит времени: {app_entry['name']}",
                f"Вы провели в {app_entry['name']} уже {self.format_duration(today_min)} сегодня (лимит: {self.format_duration(app_limit)}).",
            )

        # 2. Групповой лимит детокса
        group_cfg = self.data.get("detox_groups", {}).get(group_name)
        if group_cfg and group_cfg.get("enabled", False):
            group_limit = int(group_cfg.get("daily_limit_minutes", 120))
            group_total = sum(
                int(a.get("today_minutes", 0))
                for a in self.data["apps"].values()
                if a.get("detox_group") == group_name
            )
            if group_total >= group_limit and f"group_{group_name}" not in self.notified_limits_today:
                self.notified_limits_today.add(f"group_{group_name}")
                self._notify(
                    f"🛑 Цифровой детокс: группа «{group_name}»",
                    f"Дневной лимит группы «{group_name}» превышен ({self.format_duration(group_total)} из {self.format_duration(group_limit)}). Рекомендуем сделать перерыв!",
                )

    def _notify(self, title: str, message: str):
        if self.context and hasattr(self.context, "show_system_notification"):
            try:
                self.context.show_system_notification(title, message)
            except Exception:
                pass

    @staticmethod
    def format_hours_month(minutes: int) -> str:
        hours = minutes / 60.0
        if hours >= 10:
            return f"{int(round(hours))} ч в мес"
        elif hours >= 1:
            return f"{hours:.1f} ч в мес"
        elif minutes > 0:
            return f"{minutes} мин в мес"
        return "0 ч в мес"

    @staticmethod
    def format_duration(minutes: int) -> str:
        h, m = divmod(int(minutes), 60)
        if h > 0 and m > 0:
            return f"{h} ч {m} мин"
        elif h > 0:
            return f"{h} ч"
        return f"{m} мин"

    # --- Контракт плагина для карточек приложений ---
    def get_app_card_badge(self, app: Dict[str, Any]) -> Optional[str]:
        """Возвращает строку для отображения в карточке приложения (например: «42 ч в мес»)."""
        pkg = str(app.get("package", "")).lower()
        entry = self.data.get("apps", {}).get(pkg)
        if not entry:
            # Поиск по имени
            for k, v in self.data.get("apps", {}).items():
                if v.get("name", "").lower() == str(app.get("name", "")).lower():
                    entry = v
                    break
        if not entry:
            return None
        month_min = int(entry.get("month_minutes", 0))
        if month_min <= 0:
            return None
        return self.format_hours_month(month_min)

    def is_app_running(self, app: Dict[str, Any]) -> bool:
        pkg = str(app.get("package", "")).lower()
        return pkg in self.active_sessions

    # --- Полноценный UI компонент плагина (для вкладки «Трекер активности» и окна плагина) ---
    def get_ui_component(self):
        colors = (
            self.context.get_colors()
            if self.context and hasattr(self.context, "get_colors")
            else {
                "SURFACE": "#222630",
                "SURFACE_VARIANT": "#2f3542",
                "ON_SURFACE": "#f8fafc",
                "ON_SURFACE_VARIANT": "#94a3b8",
                "ACCENT": "#4285f4",
                "SUCCESS": "#4caf50",
                "ERROR": "#ff6b6b",
                "OUTLINE": "#3b4252",
            }
        )

        period_state = {"value": self.selected_period}
        bars_column = ft.Column(spacing=10)
        summary_text = ft.Text("", size=13, color=colors["ON_SURFACE_VARIANT"])

        def build_bars():
            bars_column.controls.clear()
            period = period_state["value"]
            field_map = {
                "day": ("today_minutes", "за сегодня"),
                "week": ("week_minutes", "за неделю"),
                "month": ("month_minutes", "в месяц"),
            }
            field_key, label_suffix = field_map.get(period, ("month_minutes", "в месяц"))

            apps_list = sorted(
                self.data.get("apps", {}).items(),
                key=lambda kv: int(kv[1].get(field_key, 0)),
                reverse=True,
            )
            max_val = max([int(v.get(field_key, 0)) for _, v in apps_list] + [60])
            total_min = sum(int(v.get(field_key, 0)) for _, v in apps_list)
            summary_text.value = f"Общее экранное время ({label_suffix}): {self.format_duration(total_min)}"

            for pkg, info in apps_list:
                mins = int(info.get(field_key, 0))
                limit_min = int(info.get("daily_limit_minutes", 180))
                ratio = min(1.0, mins / max(1, max_val))
                is_over_limit = (period == "day" and limit_min > 0 and mins >= limit_min)

                hours_str = (
                    f"{int(round(mins / 60.0))} ч в месяц"
                    if period == "month" and mins >= 60
                    else self.format_duration(mins)
                )

                bars_column.controls.append(
                    ft.Container(
                        bgcolor=colors["SURFACE_VARIANT"] + "40",
                        border_radius=10,
                        padding=10,
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Icon(
                                            "sports_esports" if info.get("category") == "Games" else "apps",
                                            size=18,
                                            color=colors["ERROR"] if is_over_limit else colors["ACCENT"],
                                        ),
                                        ft.Text(
                                            f"{info.get('name', pkg)} — {hours_str}",
                                            weight=ft.FontWeight.W_600,
                                            size=13,
                                            color=colors["ON_SURFACE"],
                                            expand=True,
                                        ),
                                        ft.Text(
                                            f"Детокс: {info.get('detox_group', '—')}",
                                            size=11,
                                            color=colors["ERROR"] if is_over_limit else colors["ON_SURFACE_VARIANT"],
                                        ),
                                        ft.IconButton(
                                            icon="add_alarm",
                                            icon_size=16,
                                            tooltip="+30 мин (тест сессии и лимита детокса)",
                                            on_click=lambda e, p=pkg: _simulate_session(p, 30),
                                        ),
                                    ]
                                ),
                                ft.ProgressBar(
                                    value=ratio,
                                    height=7,
                                    border_radius=4,
                                    color=colors["ERROR"] if is_over_limit else colors["ACCENT"],
                                    bgcolor=colors["SURFACE"],
                                ),
                            ],
                            spacing=6,
                        ),
                    )
                )

        def _simulate_session(pkg_key: str, add_mins: int):
            self.add_minutes(pkg_key, add_mins)
            build_bars()
            bars_column.update()
            summary_text.update()
            if self.context and hasattr(self.context, "update_main_content"):
                self.context.update_main_content()

        def set_period(p: str):
            period_state["value"] = p
            self.selected_period = p
            build_bars()
            bars_column.update()
            summary_text.update()

        build_bars()

        # Блок настройки групп детокса
        detox_rows = []
        for g_name, g_cfg in self.data.get("detox_groups", {}).items():
            detox_rows.append(
                ft.Row(
                    [
                        ft.Switch(
                            value=bool(g_cfg.get("enabled", True)),
                            active_track_color=colors["ACCENT"],
                            on_change=lambda e, gn=g_name: _toggle_detox_group(gn, e.control.value),
                        ),
                        ft.Text(g_name, size=13, expand=True, color=colors["ON_SURFACE"]),
                        ft.Text(
                            f"Лимит: {self.format_duration(g_cfg.get('daily_limit_minutes', 120))}/день",
                            size=12,
                            color=colors["ON_SURFACE_VARIANT"],
                        ),
                    ]
                )
            )

        def _toggle_detox_group(group_name: str, enabled: bool):
            if group_name in self.data["detox_groups"]:
                self.data["detox_groups"][group_name]["enabled"] = bool(enabled)
                self._save_data()

        return ft.Container(
            padding=14,
            border_radius=14,
            bgcolor=colors["SURFACE"] + "80",
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon("insights", color=colors["ACCENT"], size=22),
                            ft.Column(
                                [
                                    ft.Text(
                                        "Game & App Session Tracker",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        color=colors["ON_SURFACE"],
                                    ),
                                    summary_text,
                                ],
                                spacing=2,
                                expand=True,
                            ),
                        ]
                    ),
                    ft.Row(
                        [
                            ft.FilledButton("День", on_click=lambda e: set_period("day")),
                            ft.FilledButton("Неделя", on_click=lambda e: set_period("week")),
                            ft.FilledButton("Месяц", on_click=lambda e: set_period("month")),
                        ],
                        spacing=8,
                    ),
                    bars_column,
                    ft.Divider(color=colors["OUTLINE"], height=12),
                    ft.Text(
                        "Группы цифрового детокса (уведомления при превышении лимита)",
                        size=13,
                        weight=ft.FontWeight.W_600,
                        color=colors["ON_SURFACE"],
                    ),
                    *detox_rows,
                ],
                spacing=10,
            ),
        )


def initialize_plugin():
    return GameAppSessionTrackerPlugin()
