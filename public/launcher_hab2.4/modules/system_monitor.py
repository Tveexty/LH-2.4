import psutil
import flet as ft

class SystemMonitor:
    def get_battery_info(self):
        """Получить информацию о батарее"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {
                    "percent": int(battery.percent),
                    "power_plugged": battery.power_plugged,
                    "time_left": battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else None
                }
        except Exception:
            pass
        return {"percent": 0, "power_plugged": False, "time_left": None}
    
    def get_network_info(self):
        """Получить информацию о сети"""
        try:
            interfaces = psutil.net_if_stats()
            addresses = psutil.net_if_addrs()
            
            for interface, stats in interfaces.items():
                if stats.isup and interface in addresses:
                    for addr in addresses[interface]:
                        if addr.family == 2:  # IPv4
                            if interface.lower().startswith(('wi-fi', 'wifi', 'беспроводная', 'wireless', 'wlan')):
                                return {"type": "Wi-Fi", "name": interface, "status": "Connected", "ip": addr.address}
                            elif interface.lower().startswith(('ethernet', 'подключение по локальной сети', 'lan', 'eth')):
                                return {"type": "Ethernet", "name": interface, "status": "Connected", "ip": addr.address}
        except Exception:
            pass
        return {"type": "No connection", "name": "Offline", "status": "Disconnected", "ip": None}
    
    def create_devices_header(self, colors):
        """Создать панель устройств для header"""
        battery_info = self.get_battery_info()
        network_info = self.get_network_info()
        
        # Батарея
        battery_percent = battery_info["percent"]
        if battery_percent >= 80:
            battery_icon = "battery_full"
        elif battery_percent >= 60:
            battery_icon = "battery_6_bar"
        elif battery_percent >= 40:
            battery_icon = "battery_4_bar"
        elif battery_percent >= 20:
            battery_icon = "battery_2_bar"
        else:
            battery_icon = "battery_alert"
            
        if battery_info["power_plugged"]:
            battery_icon = "battery_charging_full"
            
        battery_text = f"{battery_percent}%"
        battery_color = colors["SUCCESS"] if battery_percent > 50 else colors["ERROR"] if battery_percent < 20 else colors["ON_SURFACE"]
        
        # Сеть
        network_icon = "wifi" if "Wi-Fi" in network_info["type"] else "lan" if "Ethernet" in network_info["type"] else "wifi_off"
        network_color = colors["SUCCESS"] if network_info["status"] == "Connected" else colors["ERROR"]
        network_text = network_info["type"]
        
        devices_row = ft.Row([], spacing=15)
        
        # Батарея
        battery_item = ft.Column([
            ft.Icon(battery_icon, color=battery_color, size=20),
            ft.Text(battery_text, size=12, color=battery_color)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2)
        
        # Сеть
        network_item = ft.Column([
            ft.Icon(network_icon, color=network_color, size=20),
            ft.Text(network_text, size=12, color=network_color)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2)
        
        devices_row.controls.append(battery_item)
        devices_row.controls.append(network_item)
        
        return devices_row

    def get_performance_info(self):
        """CPU/RAM для HUD"""
        try:
            return {
                "cpu": int(psutil.cpu_percent(interval=0.1)),
                "ram": int(psutil.virtual_memory().percent),
            }
        except Exception:
            return {"cpu": 0, "ram": 0}