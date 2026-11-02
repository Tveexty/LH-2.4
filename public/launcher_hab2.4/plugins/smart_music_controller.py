import flet as ft


class SmartMusicController:
    def __init__(self):
        self.current_track = ft.Text("Трек: ничего не воспроизводится", size=12)
        self.status = ft.Text("Статус: пауза", size=12)
        self.volume = 50

    def _set_track(self, name: str):
        self.current_track.value = f"Трек: {name}"
        self.status.value = "Статус: воспроизведение"
        self.current_track.update()
        self.status.update()

    def _toggle_pause(self, _):
        if "пауза" in self.status.value:
            self.status.value = "Статус: воспроизведение"
        else:
            self.status.value = "Статус: пауза"
        self.status.update()

    def _on_volume_change(self, e):
        self.volume = int(e.control.value)

    def get_ui_component(self):
        return ft.Container(
            content=ft.Column([
                ft.Text("Smart Music Controller", size=16, weight=ft.FontWeight.BOLD),
                self.current_track,
                self.status,
                ft.Row([
                    ft.IconButton(icon="skip_previous", on_click=lambda e: self._set_track("Предыдущий трек")),
                    ft.IconButton(icon="play_arrow", on_click=lambda e: self._set_track("Случайный трек")),
                    ft.IconButton(icon="pause", on_click=self._toggle_pause),
                    ft.IconButton(icon="skip_next", on_click=lambda e: self._set_track("Следующий трек")),
                ], tight=True),
                ft.Text("Громкость", size=12),
                ft.Slider(min=0, max=100, value=self.volume, divisions=20, label="{value}%", on_change=self._on_volume_change),
            ], spacing=6),
            padding=12,
            border_radius=12,
        )


def initialize_plugin():
    return SmartMusicController()