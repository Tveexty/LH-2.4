import random
import flet as ft


class SmartWeatherPlugin:
    def get_ui_component(self):
        temp = random.randint(-5, 32)
        humidity = random.randint(30, 90)
        wind = random.randint(1, 15)
        return ft.Container(
            content=ft.Column([
                ft.Text("Smart Weather", size=16, weight=ft.FontWeight.BOLD),
                ft.Text(f"Температура: {temp}°C"),
                ft.Text(f"Влажность: {humidity}%"),
                ft.Text(f"Ветер: {wind} м/с"),
            ]),
            padding=12,
            border_radius=12,
        )


def initialize_plugin():
    return SmartWeatherPlugin()