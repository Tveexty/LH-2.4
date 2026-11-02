import time
import threading
import subprocess
import sys
import flet as ft


class FocusModePlugin:
    def __init__(self):
        self.context = None
        self.running = False
        self.remaining = 25 * 60
        self.timer_text = ft.Text("25:00", size=26, weight=ft.FontWeight.BOLD)

    def set_context(self, context):
        self.context = context

    def _stop_distracting_apps(self):
        targets = ["discord", "telegram"]
        try:
            if sys.platform.startswith("win"):
                for app in targets:
                    subprocess.run(["taskkill", "/F", "/IM", f"{app}.exe"], capture_output=True, text=True)
            else:
                for app in targets:
                    subprocess.run(["pkill", "-f", app], capture_output=True, text=True)
        except Exception:
            pass

    def _run_timer(self):
        while self.running and self.remaining > 0:
            mins, secs = divmod(self.remaining, 60)
            self.timer_text.value = f"{mins:02d}:{secs:02d}"
            self.timer_text.update()
            time.sleep(1)
            self.remaining -= 1

    def toggle_focus(self, _=None):
        self.running = not self.running
        if self.running:
            self._stop_distracting_apps()
            threading.Thread(target=self._run_timer, daemon=True).start()

    def get_ui_component(self):
        return ft.Container(
            content=ft.Column([
                ft.Text("Focus Mode", size=16, weight=ft.FontWeight.BOLD),
                self.timer_text,
                ft.FilledButton("Start / Pause", on_click=self.toggle_focus),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=12,
            border_radius=12,
        )


def initialize_plugin():
    return FocusModePlugin()