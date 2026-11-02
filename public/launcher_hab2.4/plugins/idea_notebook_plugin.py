import flet as ft
from pathlib import Path
from datetime import datetime


class IdeaNotebookPlugin:
    def __init__(self):
        self.file = Path("idea_notes.txt")

    def save_idea(self, textfield, page):
        idea = (textfield.value or "").strip()
        if not idea:
            return
        with self.file.open("a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {idea}\n")
        textfield.value = ""
        textfield.update()
        page.show_snack_bar(ft.SnackBar(content=ft.Text("Идея сохранена")))

    def get_ui_component(self):
        field = ft.TextField(hint_text="New idea:")
        return ft.Container(
            content=ft.Column([
                ft.Text("Idea Notebook Plugin", size=16, weight=ft.FontWeight.BOLD),
                field,
                ft.FilledButton("Сохранить идею", on_click=lambda e: self.save_idea(field, e.page)),
                ft.Text("Горячая клавиша: Ctrl + Alt + N", size=12),
            ]),
            padding=12,
            border_radius=12,
        )


def initialize_plugin():
    return IdeaNotebookPlugin()