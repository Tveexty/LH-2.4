from pathlib import Path
import flet as ft


class SmartFileFinder:
    def __init__(self):
        self.results = ft.Column(spacing=4)

    def search(self, e):
        query = (e.control.value or "").lower().strip()
        self.results.controls.clear()
        if not query:
            self.results.update()
            return
        count = 0
        for path in Path('.').glob(f"**/*{query}*"):
            if path.is_file():
                self.results.controls.append(ft.Text(str(path)))
                count += 1
                if count >= 10:
                    break
        self.results.update()

    def get_ui_component(self):
        return ft.Container(
            content=ft.Column([
                ft.Text("Smart File Finder", size=16, weight=ft.FontWeight.BOLD),
                ft.TextField(hint_text="invoice", on_change=self.search),
                self.results,
            ]),
            padding=12,
            border_radius=12,
        )


def initialize_plugin():
    return SmartFileFinder()