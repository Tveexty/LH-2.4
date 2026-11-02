# -*- coding: utf-8 -*-
"""
Luma Beta — Модуль WidgetService (Luma_Core/core/widget_service.py)
Отвечает за периодический сбор телеметрии (CPU / RAM раз в 1 секунду)
и поставку данных живым плиткам/виджетам по запросу {"method": "widgets.get_data"}.
"""

from luma_core import SystemMetricsCollector, SystemMetricsSnapshot

__all__ = ["SystemMetricsCollector", "SystemMetricsSnapshot"]
