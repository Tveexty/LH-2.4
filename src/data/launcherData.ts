export type ThemeKey = 'dark' | 'amoled' | 'light' | 'purple' | 'spring';
export type ClockStyleKey =
  | 'android_vertical'
  | 'stacked'
  | 'standard'
  | 'pill_glass'
  | 'split_flip'
  | 'cyber_mono'
  | 'minimal'
  | 'compact_badge';
export type GlassIntensity = 'light' | 'medium' | 'strong';
export type AppType = 'app' | 'web' | 'system' | 'plugin';

export interface AppItem {
  id: string;
  name: string;
  package: string;
  category: string;
  icon: string;
  url: string;
  args?: string;
  type: AppType;
  installed: boolean;
  favorite: boolean;
  custom?: boolean;
  monthMinutes: number;
  weekMinutes: number;
  todayMinutes: number;
  elapsedSeconds: number;
  dailyLimitMinutes: number;
  detoxGroup: string;
  isRunning?: boolean;
  pluginId?: string;
}

export interface DetoxGroup {
  name: string;
  dailyLimitMinutes: number;
  enabled: boolean;
}

export interface PluginItem {
  id: string;
  name: string;
  version: string;
  author?: string;
  category?: string;
  icon?: string;
  description: string;
  enabled: boolean;
  file: string;
  hooks: string[];
  showInLauncher?: boolean;
  customIntervalSec?: number;
  notificationsEnabled?: boolean;
}

export interface CatalogPluginItem {
  id: string;
  name: string;
  version: string;
  author: string;
  category: string;
  icon: string;
  description: string;
  file: string;
  hooks: string[];
}

export interface WorkspacePreset {
  id: string;
  name: string;
  hotkey: string;
  closeProcesses: string[];
  launchApps: string[];
}

export interface BackupRecord {
  id: string;
  filename: string;
  createdAt: string;
  sizeKb: string;
}

export const THEMES: Record<
  ThemeKey,
  {
    name: string;
    isDark: boolean;
    bgGradient: string;
    surfaceRgba: string;
    cardHex: string;
    accent: string;
    accentHex: string;
  }
> = {
  dark: {
    name: 'Темная (Midnight Slate)',
    isDark: true,
    bgGradient:
      'radial-gradient(circle at 16% 12%, rgba(59, 130, 246, 0.11), transparent 40%), radial-gradient(circle at 85% 82%, rgba(16, 185, 129, 0.06), transparent 45%), linear-gradient(155deg, #0b0f17 0%, #0d111a 55%, #111723 100%)',
    surfaceRgba: 'rgba(21, 27, 38, 0.88)',
    cardHex: '#151b26',
    accent: 'blue',
    accentHex: '#3b82f6',
  },
  amoled: {
    name: 'Черный Оникс (AMOLED)',
    isDark: true,
    bgGradient:
      'radial-gradient(circle at 20% 15%, rgba(16, 185, 129, 0.08), transparent 40%), linear-gradient(155deg, #05070b 0%, #080b11 60%, #0c1018 100%)',
    surfaceRgba: 'rgba(13, 17, 24, 0.92)',
    cardHex: '#0d1118',
    accent: 'emerald',
    accentHex: '#10b981',
  },
  light: {
    name: 'Светлая',
    isDark: false,
    bgGradient:
      'radial-gradient(circle at 20% 15%, rgba(59, 130, 246, 0.12), transparent 45%), radial-gradient(circle at 80% 85%, rgba(14, 165, 233, 0.10), transparent 45%), linear-gradient(145deg, #eef2f7 0%, #f8fafc 60%, #e2e8f0 100%)',
    surfaceRgba: 'rgba(255, 255, 255, 0.82)',
    cardHex: '#ffffff',
    accent: 'blue',
    accentHex: '#2563eb',
  },
  purple: {
    name: 'Фиолетовая',
    isDark: true,
    bgGradient:
      'radial-gradient(circle at 22% 18%, rgba(168, 85, 247, 0.18), transparent 45%), radial-gradient(circle at 80% 78%, rgba(217, 70, 239, 0.12), transparent 45%), linear-gradient(145deg, #0f0b1d 0%, #17122b 55%, #120e24 100%)',
    surfaceRgba: 'rgba(26, 20, 48, 0.86)',
    cardHex: '#1a1430',
    accent: 'purple',
    accentHex: '#a855f7',
  },
  spring: {
    name: 'Весна',
    isDark: false,
    bgGradient:
      'radial-gradient(circle at 22% 18%, rgba(236, 72, 153, 0.14), transparent 45%), radial-gradient(circle at 80% 78%, rgba(244, 114, 182, 0.12), transparent 45%), linear-gradient(145deg, #fff5f8 0%, #fce7f3 60%, #fbcfe8 100%)',
    surfaceRgba: 'rgba(255, 245, 250, 0.82)',
    cardHex: '#ffffff',
    accent: 'pink',
    accentHex: '#ec4899',
  },
};

export const CLOCK_STYLE_OPTIONS: {
  id: ClockStyleKey;
  label: string;
  sample: string;
  description: string;
}[] = [
  {
    id: 'android_vertical',
    label: 'Android 14 Вертикальный (HH / MM)',
    sample: '14 / 32',
    description: 'Крупные вертикальные часы в стиле экрана блокировки Android 14 / Pixel',
  },
  {
    id: 'stacked',
    label: 'Двухэтажный (Stacked Compact)',
    sample: '14 : 32',
    description: 'Компактные часы в два этажа с датой сбоку',
  },
  {
    id: 'standard',
    label: 'Классический (Горизонтальный)',
    sample: '14:32:08',
    description: 'Традиционные цифровые часы с секундами и датой снизу',
  },
  {
    id: 'pill_glass',
    label: 'Стеклянная капсула (OneUI Pill)',
    sample: '14:32 • Пн, 02.11',
    description: 'Стильная капсула в одну строку с иконкой и датой',
  },
  {
    id: 'split_flip',
    label: 'Раздельные карточки (Flip Clock)',
    sample: '[14] [32] [08]',
    description: 'Часы и минуты на отдельных темных карточках',
  },
  {
    id: 'cyber_mono',
    label: 'Кибер-Моно (Терминал)',
    sample: '[ 14 : 32 : 08 ]',
    description: 'Моноширинный киберпанк-стиль в квадратных скобках',
  },
  {
    id: 'minimal',
    label: 'Минималистичный (Чистый)',
    sample: '14:32',
    description: 'Чистое время без лишних рамок',
  },
  {
    id: 'compact_badge',
    label: 'Компактный бейдж с днем недели',
    sample: 'Пн • 14:32',
    description: 'Акцентный бейдж дня недели и текущее время',
  },
];

// All apps start at 0 minutes / 0 seconds. Timer starts counting in real time when launched!
export const INITIAL_APPS: AppItem[] = [
  {
    id: 'steam',
    name: 'Steam',
    package: 'steam',
    category: 'Games',
    icon: 'Gamepad2',
    url: 'steam://',
    type: 'app',
    installed: true,
    favorite: true,
    monthMinutes: 0,
    weekMinutes: 0,
    todayMinutes: 0,
    elapsedSeconds: 0,
    dailyLimitMinutes: 180,
    detoxGroup: 'Игры',
    isRunning: false,
  },
  {
    id: 'chrome',
    name: 'Chrome',
    package: 'chrome',
    category: 'Browser',
    icon: 'Globe',
    url: 'https://google.com',
    type: 'web',
    installed: true,
    favorite: true,
    monthMinutes: 0,
    weekMinutes: 0,
    todayMinutes: 0,
    elapsedSeconds: 0,
    dailyLimitMinutes: 240,
    detoxGroup: 'Браузеры',
    isRunning: false,
  },
  {
    id: 'telegram',
    name: 'Telegram',
    package: 'telegram',
    category: 'Social',
    icon: 'MessageSquare',
    url: 'tg://',
    type: 'app',
    installed: true,
    favorite: true,
    monthMinutes: 0,
    weekMinutes: 0,
    todayMinutes: 0,
    elapsedSeconds: 0,
    dailyLimitMinutes: 60,
    detoxGroup: 'Соцсети и мессенджеры',
    isRunning: false,
  },
  {
    id: 'vk',
    name: 'VK',
    package: 'vk',
    category: 'Social',
    icon: 'Users',
    url: 'https://vk.com',
    type: 'web',
    installed: true,
    favorite: true,
    monthMinutes: 0,
    weekMinutes: 0,
    todayMinutes: 0,
    elapsedSeconds: 0,
    dailyLimitMinutes: 60,
    detoxGroup: 'Соцсети и мессенджеры',
    isRunning: false,
  },
  {
    id: 'vkgames',
    name: 'VK Play / Игры',
    package: 'vkgames',
    category: 'Games',
    icon: 'Trophy',
    url: 'https://games.vk.com',
    type: 'web',
    installed: true,
    favorite: false,
    monthMinutes: 0,
    weekMinutes: 0,
    todayMinutes: 0,
    elapsedSeconds: 0,
    dailyLimitMinutes: 180,
    detoxGroup: 'Игры',
    isRunning: false,
  },
  {
    id: 'youtube',
    name: 'YouTube',
    package: 'youtube',
    category: 'Media',
    icon: 'Play',
    url: 'https://youtube.com',
    type: 'web',
    installed: true,
    favorite: false,
    monthMinutes: 0,
    weekMinutes: 0,
    todayMinutes: 0,
    elapsedSeconds: 0,
    dailyLimitMinutes: 90,
    detoxGroup: 'Медиа',
    isRunning: false,
  },
  {
    id: 'vlc',
    name: 'VLC Media Player',
    package: 'vlc',
    category: 'Media',
    icon: 'Film',
    url: 'vlc://',
    type: 'app',
    installed: true,
    favorite: false,
    monthMinutes: 0,
    weekMinutes: 0,
    todayMinutes: 0,
    elapsedSeconds: 0,
    dailyLimitMinutes: 180,
    detoxGroup: 'Медиа',
    isRunning: false,
  },
  {
    id: 'vkmusic',
    name: 'VK Музыка',
    package: 'vkmusic',
    category: 'Music',
    icon: 'Music',
    url: 'https://vk.com/music',
    type: 'web',
    installed: true,
    favorite: false,
    monthMinutes: 0,
    weekMinutes: 0,
    todayMinutes: 0,
    elapsedSeconds: 0,
    dailyLimitMinutes: 180,
    detoxGroup: 'Медиа',
    isRunning: false,
  },
  {
    id: 'yandexmusic',
    name: 'Яндекс Музыка',
    package: 'yandexmusic',
    category: 'Music',
    icon: 'Headphones',
    url: 'https://music.yandex.ru',
    type: 'web',
    installed: true,
    favorite: false,
    monthMinutes: 0,
    weekMinutes: 0,
    todayMinutes: 0,
    elapsedSeconds: 0,
    dailyLimitMinutes: 180,
    detoxGroup: 'Медиа',
    isRunning: false,
  },
  {
    id: 'firefox',
    name: 'Firefox',
    package: 'firefox',
    category: 'Browser',
    icon: 'Compass',
    url: 'https://mozilla.org',
    type: 'web',
    installed: true,
    favorite: false,
    monthMinutes: 0,
    weekMinutes: 0,
    todayMinutes: 0,
    elapsedSeconds: 0,
    dailyLimitMinutes: 240,
    detoxGroup: 'Браузеры',
    isRunning: false,
  },
  {
    id: 'calc',
    name: 'Калькулятор',
    package: 'calc',
    category: 'System',
    icon: 'Calculator',
    url: 'calc',
    type: 'system',
    installed: true,
    favorite: false,
    monthMinutes: 0,
    weekMinutes: 0,
    todayMinutes: 0,
    elapsedSeconds: 0,
    dailyLimitMinutes: 300,
    detoxGroup: 'Система',
    isRunning: false,
  },
  {
    id: 'explorer',
    name: 'Проводник',
    package: 'explorer',
    category: 'System',
    icon: 'FolderOpen',
    url: 'explorer',
    type: 'system',
    installed: true,
    favorite: false,
    monthMinutes: 0,
    weekMinutes: 0,
    todayMinutes: 0,
    elapsedSeconds: 0,
    dailyLimitMinutes: 300,
    detoxGroup: 'Система',
    isRunning: false,
  },
  {
    id: 'taskmgr',
    name: 'Диспетчер задач',
    package: 'taskmgr',
    category: 'System',
    icon: 'Activity',
    url: 'taskmgr',
    type: 'system',
    installed: true,
    favorite: false,
    monthMinutes: 0,
    weekMinutes: 0,
    todayMinutes: 0,
    elapsedSeconds: 0,
    dailyLimitMinutes: 300,
    detoxGroup: 'Система',
    isRunning: false,
  },
  {
    id: 'cmd',
    name: 'Командная строка',
    package: 'cmd',
    category: 'System',
    icon: 'Terminal',
    url: 'cmd',
    type: 'system',
    installed: true,
    favorite: false,
    monthMinutes: 0,
    weekMinutes: 0,
    todayMinutes: 0,
    elapsedSeconds: 0,
    dailyLimitMinutes: 300,
    detoxGroup: 'Система',
    isRunning: false,
  },
  {
    id: 'winword',
    name: 'Microsoft Word',
    package: 'winword',
    category: 'Office',
    icon: 'FileText',
    url: 'winword',
    type: 'app',
    installed: true,
    favorite: false,
    monthMinutes: 0,
    weekMinutes: 0,
    todayMinutes: 0,
    elapsedSeconds: 0,
    dailyLimitMinutes: 300,
    detoxGroup: 'Работа',
    isRunning: false,
  },
  {
    id: 'yandexdisk',
    name: 'Яндекс Диск',
    package: 'yandexdisk',
    category: 'Cloud',
    icon: 'Cloud',
    url: 'https://disk.yandex.ru',
    type: 'web',
    installed: true,
    favorite: false,
    monthMinutes: 0,
    weekMinutes: 0,
    todayMinutes: 0,
    elapsedSeconds: 0,
    dailyLimitMinutes: 300,
    detoxGroup: 'Работа',
    isRunning: false,
  },
];

export const INITIAL_DETOX_GROUPS: DetoxGroup[] = [
  { name: 'Игры', dailyLimitMinutes: 180, enabled: true },
  { name: 'Соцсети и мессенджеры', dailyLimitMinutes: 90, enabled: true },
  { name: 'Медиа', dailyLimitMinutes: 120, enabled: true },
  { name: 'Браузеры', dailyLimitMinutes: 240, enabled: false },
];

export const INITIAL_PLUGINS: PluginItem[] = [
  {
    id: 'session_tracker_plugin',
    name: 'Game & App Session Tracker',
    version: '2.4.0',
    author: 'LauncherHab Team',
    category: 'Аналитика и Детокс',
    icon: 'BarChart3',
    description:
      'Отслеживает время с 00:00 в реальном времени после запуска каждого приложения или игры, выводит таймер и часы на карточках, строит графики (день/неделя/месяц) и контролирует лимиты детокса.',
    enabled: true,
    file: 'plugins/session_tracker_plugin.py',
    hooks: ['on_load', 'on_app_launched', 'on_tick', 'get_app_card_badge', 'get_ui_component'],
    showInLauncher: true,
    customIntervalSec: 1,
    notificationsEnabled: true,
  },
  {
    id: 'focus_mode_plugin',
    name: 'Focus Mode (Pomodoro)',
    version: '2.4.0',
    author: 'LauncherHab Team',
    category: 'Продуктивность',
    icon: 'Clock',
    description:
      'Режим концентрации с Pomodoro-таймером на 25 минут и автоматическим закрытием отвлекающих мессенджеров.',
    enabled: true,
    file: 'plugins/focus_mode_plugin.py',
    hooks: ['set_context', 'get_ui_component'],
    showInLauncher: true,
    customIntervalSec: 60,
    notificationsEnabled: true,
  },
  {
    id: 'smart_music_controller',
    name: 'Smart Music Controller',
    version: '2.4.0',
    author: 'LauncherHab Team',
    category: 'Медиа',
    icon: 'Music',
    description: 'Встроенный мини-плеер для быстрого переключения треков и управления медиапотоком.',
    enabled: true,
    file: 'plugins/smart_music_controller.py',
    hooks: ['get_ui_component'],
    showInLauncher: true,
    customIntervalSec: 30,
    notificationsEnabled: true,
  },
  {
    id: 'smart_weather_plugin',
    name: 'Smart Weather Plugin',
    version: '2.4.0',
    author: 'LauncherHab Team',
    category: 'Виджеты',
    icon: 'Cloud',
    description: 'Отображение актуальной температуры, влажности и скорости ветра прямо в окне запуска.',
    enabled: true,
    file: 'plugins/smart_weather_plugin.py',
    hooks: ['get_ui_component'],
    showInLauncher: true,
    customIntervalSec: 300,
    notificationsEnabled: true,
  },
  {
    id: 'idea_notebook_plugin',
    name: 'Idea Notebook',
    version: '2.4.0',
    author: 'LauncherHab Team',
    category: 'Утилиты',
    icon: 'FileText',
    description: 'Быстрые заметки и сохранение идей в idea_notes.txt без ошибок show_snack_bar.',
    enabled: true,
    file: 'plugins/idea_notebook_plugin.py',
    hooks: ['get_ui_component'],
    showInLauncher: true,
    customIntervalSec: 60,
    notificationsEnabled: true,
  },
  {
    id: 'smart_file_finder',
    name: 'Smart File Finder',
    version: '2.4.0',
    author: 'LauncherHab Team',
    category: 'Система',
    icon: 'Search',
    description: 'Быстрый мгновенный поиск локальных файлов по рабочей директории.',
    enabled: true,
    file: 'plugins/smart_file_finder.py',
    hooks: ['get_ui_component'],
    showInLauncher: true,
    customIntervalSec: 60,
    notificationsEnabled: true,
  },
];

export const PLUGIN_CATALOG: CatalogPluginItem[] = [
  {
    id: 'system_cleaner_plugin',
    name: 'System Cleaner & RAM Optimizer',
    version: '2.4.0',
    author: 'LauncherHab Store',
    category: 'Система',
    icon: 'Activity',
    description: 'Очистка временного кэша системы и освобождение неиспользуемой оперативной памяти в 1 клик.',
    file: 'plugins/system_cleaner_plugin.py',
    hooks: ['on_load', 'get_ui_component'],
  },
  {
    id: 'game_booster_plugin',
    name: 'Game Booster Pro (FPS & Ping)',
    version: '2.4.0',
    author: 'LauncherHab Store',
    category: 'Игры',
    icon: 'Gamepad2',
    description: 'Повышение приоритета игровых процессов и мониторинг задержки сети перед запуском игр.',
    file: 'plugins/game_booster_plugin.py',
    hooks: ['on_load', 'on_app_launched', 'get_ui_component'],
  },
  {
    id: 'quick_clipboard_plugin',
    name: 'Quick Clipboard History',
    version: '2.4.0',
    author: 'LauncherHab Store',
    category: 'Продуктивность',
    icon: 'Copy',
    description: 'Менеджер буфера обмена с быстрым копированием сохраненных сниппетов и команд.',
    file: 'plugins/quick_clipboard_plugin.py',
    hooks: ['on_load', 'get_ui_component'],
  },
];

export const INITIAL_WORKSPACES: WorkspacePreset[] = [
  {
    id: 'gaming',
    name: 'Игровой режим',
    hotkey: 'ctrl+shift+g',
    closeProcesses: ['chrome', 'browser', 'discordcanary'],
    launchApps: ['steam', 'telegram'],
  },
  {
    id: 'dev',
    name: 'Режим разработчика',
    hotkey: 'ctrl+shift+d',
    closeProcesses: [],
    launchApps: ['cmd', 'chrome'],
  },
  {
    id: 'focus',
    name: 'Фокус и Детокс',
    hotkey: 'ctrl+shift+f',
    closeProcesses: ['steam', 'vk', 'telegram'],
    launchApps: ['winword'],
  },
];

export const PYTHON_PROJECT_FILES: { path: string; title: string; badge: string; summary: string }[] = [
  {
    path: 'modules/encryption_manager.py',
    title: 'modules/encryption_manager.py',
    badge: 'FIXED v2.4',
    summary:
      'Исправлена ошибка Fernet key must be 32 url-safe base64-encoded bytes (SHA-256 -> 32-байтный URL-safe Base64 ключ для надежного сохранения настроек).',
  },
  {
    path: 'modules/glass_morphism.py',
    title: 'modules/glass_morphism.py',
    badge: 'FIXED v2.4',
    summary:
      'Исправлены желтые полоски: формат цветов Flet переведен на #AARRGGBB, стиль темной темы приведен к Midnight Slate как на скриншоте 2.',
  },
  {
    path: 'plugins/session_tracker_plugin.py',
    title: 'plugins/session_tracker_plugin.py',
    badge: 'ZERO-START v2.4',
    summary:
      'Трекер времени начинается с 0 мин и запускает живой посекундный таймер (🟢 00:00:15) при старте приложения или игры.',
  },
  {
    path: 'modules/plugin_manager.py',
    title: 'modules/plugin_manager.py',
    badge: 'STORE & API v2.4',
    summary:
      'Расширенный PluginAPI 2.4: плагины в списке запуска («Плагины»), магазин расширений (скачать/установить/настроить/удалить).',
  },
  {
    path: 'modules/ui_panels.py',
    title: 'modules/ui_panels.py',
    badge: 'ANDROID CLOCK v2.4',
    summary:
      'Вертикальные часы Android 14 (HH / MM), 8 стилей часов и вывод активных плагинов в библиотеке и сетке.',
  },
  {
    path: 'modules/ui_dialogs.py',
    title: 'modules/ui_dialogs.py',
    badge: 'UPDATED v2.4',
    summary:
      '5 вкладок настроек, менеджер резервных копий (восстановление/удаление), 8 стилей часов и устранение show_snack_bar.',
  },
  {
    path: 'modules/ui_manager_core.py',
    title: 'modules/ui_manager_core.py',
    badge: 'UPDATED v2.4',
    summary:
      'Ядро Launcher Hab 2.4: ежесекундный тик таймера запущенных приложений, метод show_toast через page.open(ft.SnackBar).',
  },
  {
    path: 'modules/theme_manager.py',
    title: 'modules/theme_manager.py',
    badge: 'UPDATED v2.4',
    summary:
      'Сохранение всех настроек в launcher_settings.json, 8 стилей часов и темы Midnight Slate / Черный Оникс.',
  },
  {
    path: 'modules/file_manager.py',
    title: 'modules/file_manager.py',
    badge: 'FIXED v2.4',
    summary:
      'Надежное чтение и запись зашифрованных/JSON настроек без повреждения файла при сбое.',
  },
  {
    path: 'modules/audio_controller.py',
    title: 'modules/audio_controller.py',
    badge: 'UPDATED v2.4',
    summary:
      'Неблокирующий фоновый контроллер системной громкости (pycaw CoreAudio COM в фоновом потоке + Mute).',
  },
  {
    path: 'main.py',
    title: 'main.py',
    badge: 'ENTRY',
    summary: 'Точка входа Flet-приложения Launcher Hab 2.4 на языке Python.',
  },
];

export const VERSION_HISTORY: Record<string, string[]> = {
  '2.4': [
    '🚀 LAUNCHER HUB 2.4 – MIDNIGHT SLATE, ANDROID VERTICAL CLOCK, ZERO-START TRACKER & PLUGIN STORE',
    '🛡 ИСПРАВЛЕНО ШИФРОВАНИЕ FERNET И СОХРАНЕНИЕ НАСТРОЕК – корректный 32-байтный URL-safe Base64 ключ через SHA-256',
    '🎨 УБРАНЫ ЖЕЛТЫЕ ПОЛОСКИ И ОБНОВЛЕНА ТЕМНАЯ ТЕМА – исправлен порядок байтов #AARRGGBB в Flet и внедрен дизайн Midnight Slate (как на скриншоте 2)',
    '🔔 ИСПРАВЛЕНА ОШИБКА SHOW_SNACK_BAR – все уведомления переведены на современный метод page.open(ft.SnackBar(...))',
    '⏱ ТРЕКЕР ВРЕМЕНИ С НУЛЯ (0 МИН) + ЖИВОЙ СЕКУНДОМЕР – отсчет начинается с 00:00 строго после запуска приложения',
    '🧩 ПЛАГИНЫ В СПИСКЕ ЗАПУСКА + МАГАЗИН ПЛАГИНОВ – запуск любого плагина из категории «Плагины», скачивание, настройка и удаление',
    '📱 ВЕРТИКАЛЬНЫЕ ЧАСЫ КАК НА ANDROID 14 + 8 СТИЛЕЙ ЧАСОВ – крупные часы HH / MM, Flip-карточки, Стеклянная капсула и Кибер-Моно',
  ],
  '2.3': [
    '🎨 УЛУЧШЕННЫЙ LIQUID GLASS ИНТЕРФЕЙС – переработанный стеклянный дизайн и эффекты прозрачности',
    '🖥 FLOATING HUD – плавающая панель с системной информацией CPU/RAM',
    '🗑 ФИКСИРОВАННАЯ КОРЗИНА – быстрый доступ к корзине в правом нижнем углу',
    '🔌 СИСТЕМА ПЛАГИНОВ – базовая поддержка расширений LauncherHub',
  ],
  '2.2': [
    '⚡ ОПТИМИЗАЦИЯ ПРОИЗВОДИТЕЛЬНОСТИ – кэширование поиска и виртуализация списков',
    '💾 СИСТЕМА РЕЗЕРВНОГО КОПИРОВАНИЯ – автоматическое сохранение и восстановление настроек',
  ],
};

export function formatLiveClock(seconds: number): string {
  const s = Math.max(0, Math.floor(seconds));
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const sec = s % 60;
  if (h > 0) {
    return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}`;
  }
  return `${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}`;
}

export function formatMonthBadge(minutes: number, elapsedSeconds = 0, isRunning = false): string {
  if (isRunning) {
    return `🟢 ${formatLiveClock(elapsedSeconds)}`;
  }
  const totalSec = Math.max(Math.round(minutes * 60), elapsedSeconds);
  if (totalSec <= 0) {
    return '0 мин';
  }
  if (totalSec < 60) {
    return `${totalSec} сек`;
  }
  const totalMinutes = totalSec / 60;
  const hours = totalMinutes / 60;
  if (hours >= 10) return `${Math.round(hours)} ч в мес`;
  if (hours >= 1) return `${hours.toFixed(1)} ч в мес`;
  return `${Math.max(1, Math.round(totalMinutes))} мин в мес`;
}

export function formatDurationRu(minutes: number, elapsedSeconds = 0): string {
  const totalSec = Math.max(Math.round(minutes * 60), elapsedSeconds);
  if (totalSec <= 0) return '0 мин';
  if (totalSec < 60) return `${totalSec} сек`;
  const totalMin = Math.floor(totalSec / 60);
  const h = Math.floor(totalMin / 60);
  const m = totalMin % 60;
  if (h > 0 && m > 0) return `${h} ч ${m} мин`;
  if (h > 0) return `${h} ч`;
  return `${m} мин`;
}
