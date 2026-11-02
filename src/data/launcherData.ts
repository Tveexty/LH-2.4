export type ThemeKey = 'dark' | 'amoled' | 'light' | 'purple' | 'spring' | string;
export type ClockStyleKey =
  | 'android_vertical'
  | 'stacked'
  | 'standard'
  | 'pill_glass'
  | 'split_flip'
  | 'cyber_mono'
  | 'minimal'
  | 'compact_badge'
  | 'nothing_dot'
  | 'ios_standby'
  | 'samsung_oneui'
  | 'neon_synthwave'
  | 'retro_casio'
  | 'macos_sonoma'
  | 'futuristic_hud'
  | 'analog_hybrid'
  | 'vertical_neon_bar'
  | 'material_expressive';
export type GlassIntensity = 'light' | 'medium' | 'strong';
export type AppType = 'app' | 'web' | 'system' | 'plugin';

export interface CustomThemeConfig {
  id: string;
  name: string;
  isDark: boolean;
  bgGradient: string;
  surfaceRgba: string;
  cardHex: string;
  accent: string;
  accentHex: string;
  custom?: boolean;
}

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

export const THEMES: Record<string, CustomThemeConfig> = {
  dark: {
    id: 'dark',
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
    id: 'amoled',
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
    id: 'light',
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
    id: 'purple',
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
    id: 'spring',
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
  isNew25?: boolean;
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
  // +10 НОВЫХ СТИЛЕЙ В ВЕРСИИ 2.5
  {
    id: 'nothing_dot',
    label: 'Nothing OS (Dot-Matrix)',
    sample: '::14 · 32 · 08::',
    description: 'Точечно-матричный индустриальный шрифт в стиле Nothing Phone (2)',
    isNew25: true,
  },
  {
    id: 'ios_standby',
    label: 'iOS 17 StandBy (Ночной док)',
    sample: '14:32 STANDBY',
    description: 'Крупные контрастные часы ночного режима iOS 17 StandBy',
    isNew25: true,
  },
  {
    id: 'samsung_oneui',
    label: 'Samsung OneUI 6 Lock',
    sample: '14 / 32 OneUI',
    description: 'Фирменный двойной блок Samsung One UI 6 с акцентом минут',
    isNew25: true,
  },
  {
    id: 'neon_synthwave',
    label: 'Neon Synthwave 80s',
    sample: '⚡ 14:32:08',
    description: 'Неоновый ретро-футуризм с мягким свечением цифр',
    isNew25: true,
  },
  {
    id: 'retro_casio',
    label: 'Retro LCD (Casio F-91W)',
    sample: "LCD 14:32'08",
    description: 'Кварцевый ЖК-индикатор в стиле классических часов Casio',
    isNew25: true,
  },
  {
    id: 'macos_sonoma',
    label: 'macOS Sonoma Lockscreen',
    sample: '14:32 Sonoma',
    description: 'Элегантная типографика экрана блокировки macOS Sonoma',
    isNew25: true,
  },
  {
    id: 'futuristic_hud',
    label: 'Sci-Fi Tactical HUD',
    sample: 'SYS//14:32.08',
    description: 'Тактический телеметрический дисплей с системным префиксом',
    isNew25: true,
  },
  {
    id: 'analog_hybrid',
    label: 'Гибридный Хронограф',
    sample: '◔ 14:32:08',
    description: 'Сочетание часового индикатора хронографа и цифрового блока',
    isNew25: true,
  },
  {
    id: 'vertical_neon_bar',
    label: 'Неоновая Вертикаль (Бар)',
    sample: '14 ┃ 32',
    description: 'Вертикальная колонка с яркой неоновой полосой акцента',
    isNew25: true,
  },
  {
    id: 'material_expressive',
    label: 'Material You Expressive (Pixel 9)',
    sample: '14 / 32 Pixel',
    description: 'Выразительный адаптивный стиль Google Pixel 9 Material You',
    isNew25: true,
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
    version: '2.5.0',
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
    version: '2.5.0',
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
    version: '2.5.0',
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
    version: '2.5.0',
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
    version: '2.5.0',
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
    version: '2.5.0',
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
    version: '2.5.0',
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
    version: '2.5.0',
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
    version: '2.5.0',
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

export interface IslandPlayerItem {
  id: string;
  name: string;
  color: string;
  track: string;
  artist: string;
}

export interface IslandNotificationItem {
  id: string;
  app: string;
  title: string;
  message: string;
  time: string;
  color: string;
  read: boolean;
}

export const INITIAL_ISLAND_PLAYERS: IslandPlayerItem[] = [
  {
    id: 'windows_smtc',
    name: 'Windows Media (SMTC)',
    color: '#3b82f6',
    track: 'Synthwave Night Drive',
    artist: 'System Audio Session',
  },
  {
    id: 'yandex_music',
    name: 'Яндекс Музыка',
    color: '#f59e0b',
    track: 'Моя Волна • Поток',
    artist: 'Яндекс Музыка HQ',
  },
  {
    id: 'spotify',
    name: 'Spotify Desktop',
    color: '#10b981',
    track: 'Midnight City (Lo-Fi Mix)',
    artist: 'Spotify Connect',
  },
  {
    id: 'vk_music',
    name: 'VK Музыка',
    color: '#60a5fa',
    track: 'Киберпанк Плейлист',
    artist: 'VK Audio',
  },
  {
    id: 'telegram_audio',
    name: 'Telegram Плеер',
    color: '#38bdf8',
    track: 'Голосовой / Аудио подкаст',
    artist: 'Telegram Desktop',
  },
];

export const INITIAL_WINDOWS_NOTIFICATIONS: IslandNotificationItem[] = [
  {
    id: 'win_1',
    app: 'Безопасность Windows 11',
    title: 'Защита в реальном времени активна',
    message: 'Угроз не обнаружено. Криптоконтейнер PBKDF2-HMAC-SHA256 синхронизирован.',
    time: 'Сейчас',
    color: '#10b981',
    read: false,
  },
  {
    id: 'win_2',
    app: 'Центр уведомлений Windows',
    title: 'Dynamic Island 2.6 подключен к системе',
    message: 'Перехват уведомлений Windows, контроль зарядки, таймер и аудио-сессии активны.',
    time: '1 мин назад',
    color: '#3b82f6',
    read: false,
  },
  {
    id: 'win_3',
    app: 'GitHub Auto-Updater 2.6',
    title: 'Проверка обновлений выполнена',
    message: 'Установлена актуальная сборка Launcher Hab 2.6.0 (Python + Flet).',
    time: '2 мин назад',
    color: '#a855f7',
    read: false,
  },
];

export const PYTHON_PROJECT_FILES: { path: string; title: string; badge: string; summary: string }[] = [
  {
    path: 'Luma_Core/luma_core.py',
    title: 'Luma_Core/luma_core.py',
    badge: 'LUMA BETA',
    summary:
      'Независимое фоновое Headless-ядро (JSON-RPC 2.0 сокет 127.0.0.1:45890, WidgetEngine с опросом CPU/RAM раз в 1 сек, ProcessManager, ConfigManager, HotkeyManager).',
  },
  {
    path: 'Luma_Core/ARCHITECTURE.md',
    title: 'Luma_Core/ARCHITECTURE.md',
    badge: 'CONTRACT',
    summary:
      'Архитектурная спецификация Luma Beta: структура директорий Luma_Core/, контракт JSON-RPC 2.0 (system.ping, widgets.get_data, widgets.list) и отказоустойчивость.',
  },
  {
    path: 'Luma_Core/test_ipc_client.py',
    title: 'Luma_Core/test_ipc_client.py',
    badge: 'IPC TEST',
    summary:
      'Асинхронный тестовый клиент JSON-RPC 2.0 для проверки локального сокета Luma Beta и метода {"method": "widgets.get_data"}.',
  },
  {
    path: 'modules/dynamic_island.py',
    title: 'modules/dynamic_island.py',
    badge: 'NEW v2.6',
    summary:
      'Всегда активный Dynamic Island 2.6: уведомления Windows, смена проигрывателя, таймер, секундомер, анимация зарядки и режим «Не беспокоить».',
  },
  {
    path: 'modules/diagnostics_updater.py',
    title: 'modules/diagnostics_updater.py',
    badge: 'NEW v2.6',
    summary:
      'Автообновление с GitHub Releases API, проверка новой версии, переход на GitHub, раздел «О приложении» и полная диагностика 6 подсистем.',
  },
  {
    path: 'modules/ui_dialogs.py',
    title: 'modules/ui_dialogs.py',
    badge: 'ANDROID v2.6',
    summary:
      'Полностью перерисованные настройки в стиле Android 15 (Quick Settings Tiles + боковое меню), адаптивная тема День/Ночь и история версий 1.0–2.6.',
  },
  {
    path: 'modules/theme_manager.py',
    title: 'modules/theme_manager.py',
    badge: 'ADAPTIVE v2.6',
    summary:
      'Адаптивная тема «День / Ночь» по расписанию (выбор времени и тем), настройки Dynamic Island, ПКМ «Назад» и 18 стилей часов.',
  },
  {
    path: 'modules/ui_manager_core.py',
    title: 'modules/ui_manager_core.py',
    badge: 'CORE v2.6',
    summary:
      'Ядро Launcher Hab 2.6: навигация одной рукой (ПКМ = Назад), подавление тостов в режиме «Не беспокоить», тик Острова и авто-смена темы.',
  },
  {
    path: 'modules/ui_panels.py',
    title: 'modules/ui_panels.py',
    badge: 'ISLAND v2.6',
    summary:
      'Встроенная капсула Dynamic Island 2.6 в центре верхней панели, жест ПКМ «Назад» (GestureDetector) и 18 стилей часов.',
  },
  {
    path: 'modules/encryption_manager.py',
    title: 'modules/encryption_manager.py',
    badge: 'CRYPTO v2.5',
    summary:
      'PBKDF2-HMAC-SHA256 (100 000 итераций), контроль целостности HMAC-SHA256, ротация ключей и обратная совместимость с 2.4.',
  },
  {
    path: 'modules/plugin_manager.py',
    title: 'modules/plugin_manager.py',
    badge: 'API v2.6',
    summary:
      'PluginAPI: зашифрованные секреты плагинов, хуки смены темы и часов, магазин расширений и трекер времени.',
  },
  {
    path: 'modules/glass_morphism.py',
    title: 'modules/glass_morphism.py',
    badge: 'GLASS',
    summary:
      'Поддержка кастомного скругления карточек, масштаба иконок (85–120%), подсветки активных приложений и формата #AARRGGBB.',
  },
  {
    path: 'plugins/session_tracker_plugin.py',
    title: 'plugins/session_tracker_plugin.py',
    badge: 'ZERO-START',
    summary:
      'Трекер времени начинается с 0 мин и запускает живой посекундный таймер (🟢 00:00:15) при старте приложения или игры.',
  },
  {
    path: 'modules/file_manager.py',
    title: 'modules/file_manager.py',
    badge: 'STORAGE',
    summary:
      'Надежное чтение и запись зашифрованных/JSON настроек без повреждения файла при сбое.',
  },
  {
    path: 'modules/audio_controller.py',
    title: 'modules/audio_controller.py',
    badge: 'AUDIO',
    summary:
      'Неблокирующий фоновый контроллер системной громкости (pycaw CoreAudio COM в фоновом потоке + Mute).',
  },
  {
    path: 'main.py',
    title: 'main.py',
    badge: 'ENTRY',
    summary: 'Точка входа Flet-приложения Launcher Hab 2.6 на языке Python.',
  },
];

// Полная история версий с 1.0 до 2.6
export const VERSION_HISTORY: Record<string, string[]> = {
  '2.6': [
    '🚀 LAUNCHER HAB 2.6 — DYNAMIC ISLAND, НАСТРОЙКИ В СТИЛЕ ANDROID, АДАПТИВНАЯ ТЕМА ДЕНЬ/НОЧЬ, АВТООБНОВЛЕНИЕ С GITHUB И ПКМ «НАЗАД»',
    '🏝️ ВСЕГДА АКТИВНЫЙ DYNAMIC ISLAND — интерактивный остров в верхней панели с постоянным отображением статуса, времени, даты и процентов заряда устройства',
    '🔔 ПРОСМОТР УВЕДОМЛЕНИЙ ОТ WINDOWS В ОСТРОВЕ — перехват и журнал системных и прикладных уведомлений Windows с очисткой и фильтрацией',
    '🎵 СМЕНА ПРОИГРЫВАТЕЛЯ В DYNAMIC ISLAND — переключение между Windows Media (SMTC), Яндекс Музыкой, Spotify, VK Музыкой и Telegram Audio + управление треками',
    '⏱️ ВСТРОЕННЫЙ ТАЙМЕР И СЕКУНДОМЕР В ОСТРОВЕ — обратный отсчет с пресетами (1/5/15/25 мин) и секундомер с записью кругов (Laps) и выводом прямо на капсулу',
    '⚡ АНИМАЦИЯ ЗАРЯДКИ УСТРОЙСТВА — неоновая изумрудная волна и пульсация молнии в Dynamic Island при подключении питания и отображение процентов батареи',
    '🌙 ПОЛНОСТЬЮ РАБОЧИМ РЕЖИМ «НЕ БЕСПОКОИТЬ» (DND) — блокирует всплывающие баннеры и звуки, тихо сохраняя все уведомления внутри Dynamic Island',
    '📱 ПОЛНОСТЬЮ ПЕРЕРИСОВАННЫЕ НАСТРОЙКИ В СТИЛЕ ANDROID 15 — боковое меню с цветными иконками, плитки быстрых настроек (Quick Settings Tiles) и скругленные карточки',
    '🌗 АДАПТИВНАЯ ТЕМА «ДЕНЬ / НОЧЬ» ПО РАСПИСАНИЮ — автоматическая смена темы (днем — светлая/белая, ночью — темная) с выбором точного времени смены и конкретных тем',
    '🔄 АВТООБНОВЛЕНИЕ И ПРОВЕРКА НОВОЙ ВЕРСИИ С GITHUB — проверка релизов через GitHub API, переход на репозиторий GitHub в 1 клик и автопроверка при запуске',
    '🩺 ДИАГНОСТИКА ПРИЛОЖЕНИЯ И РАЗДЕЛ «О ПРИЛОЖЕНИИ» — комплексная проверка файловой системы, шифрования PBKDF2, плагинов, ресурсов ОС и экспорт отчета',
    '🖱️ ФУНКЦИЯ «НАЗАД» НА ПКМ (ПРАВУЮ КНОПКУ МЫШИ) — удобная навигация одной рукой: клик ПКМ возвращает на предыдущий экран, сбрасывает фильтр или закрывает поиск',
  ],
  '2.5': [
    '🚀 LAUNCHER HAB 2.5 — МЕГА-ПЕРСОНАЛИЗАЦИЯ, 18 СТИЛЕЙ ЧАСОВ, КАСТОМНЫЕ ТЕМЫ PRO, API 2.5 И PBKDF2 ШИФРОВАНИЕ',
    '💡 МГНОВЕННАЯ ПОДСВЕТКА АКТИВНЫХ НАСТРОЕК («ЗАЖИГАНИЕ» СТАТУСА) — при выборе любого стиля, переключателя или пресета элемент мгновенно загорается неоновой рамкой и меняет статус с «⚪ НЕАКТИВНО» на «🟢 АКТИВНО»',
    '🕒 +10 НОВЫХ СТИЛЕЙ ЧАСОВ (ВСЕГО 18 СТИЛЕЙ) — добавлены Nothing OS (Dot-Matrix), iOS 17 StandBy, Samsung OneUI 6, Neon Synthwave 80s, Retro LCD Casio F-91W, macOS Sonoma, Sci-Fi Tactical HUD, Гибридный Хронограф, Неоновая Вертикаль и Material You Expressive',
    '✨ РАСШИРЕННЫЙ ДИЗАЙН ЧАСОВ — настройка неонового свечения (Glow), скругления рамки часов, прозрачности подложки, акцентного цвета минут, жирности шрифта и мигающего разделителя',
    '🎨 СТУДИЯ СОЗДАНИЯ КАСТОМНЫХ ТЕМ 2.5 — живое интерактивное превью темы, выбор режима (Dark / AMOLED / Light), настройка цветовых каналов, радиуса скругления карточек, масштаба иконок и свечения при наведении',
    '🔐 ОБНОВЛЕННОЕ ШИФРОВАНИЕ ДАННЫХ 2.5 — деривация ключей PBKDF2-HMAC-SHA256 (100 000 итераций), контроль целостности HMAC-SHA256, ротация ключей и обратная совместимость с v2.4',
    '🔌 УЛУЧШЕННЫЙ APPLICATION & PLUGIN API 2.5 — шифрованное хранилище секретов для плагинов, хуки смены темы/часов (on_theme_changed, on_clock_style_changed) и диагностика безопасности',
    '📜 ПОЛНАЯ ИСТОРИЯ ОБНОВЛЕНИЙ — добавлен полный архив изменений всех версий программы с 1.0 по 2.5',
  ],
  '2.4': [
    '🚀 LAUNCHER HAB 2.4 — DARK SLATE PRO, LIVE SESSION TRACKER (С 0) И ANDROID 14 ЧАСЫ',
    '🎨 ИСПРАВЛЕНЫ ЦВЕТА И РАМКИ (#AARRGGBB) — убраны желтые полосы, внедрен графитовый стиль Midnight Slate',
    '🔐 ИСПРАВЛЕНО СОХРАНЕНИЕ И ШИФРОВАНИЕ НАСТРОЕК — валидный 32-байтовый ключ Fernet без потери данных',
    '⏱️ GAME & APP SESSION TRACKER С 0 — честный отсчет времени с 00:00 при запуске приложения и живой таймер на карточках',
    '🧩 ПЛАГИНЫ В СПИСКЕ ЗАПУСКА И МАГАЗИН РАСШИРЕНИЙ — скачивание, настройка, включение и удаление плагинов в 1 клик',
    '🕒 ВЕРТИКАЛЬНЫЕ ЧАСЫ ANDROID 14 — крупный вертикальный виджет часов (HH / MM) и 8 современных стилей',
    '🔊 ФОНОВЫЙ КОНТРОЛЛЕР СИСТЕМНОЙ ГРОМКОСТИ — плавная регулировка громкости в фоновом потоке',
  ],
  '2.3': [
    '🎨 УЛУЧШЕННЫЙ LIQUID GLASS ИНТЕРФЕЙС – переработанный стеклянный дизайн, плавные эффекты прозрачности и более современный внешний вид',
    '🖥 FLOATING HUD – новая плавающая панель с системной информацией и быстрым доступом к функциям',
    '🗑 ФИКСИРОВАННАЯ КОРЗИНА – корзина закреплена в правом нижнем углу интерфейса',
    '🔎 ИСТОРИЯ ПОИСКА – система поиска теперь сохраняет предыдущие запросы для более быстрого доступа',
    '💾 УЛУЧШЕННАЯ СИСТЕМА РЕЗЕРВНОГО КОПИРОВАНИЯ – стабильное сохранение и восстановление настроек и данных пользователя',
    '🕒 НОВЫЕ СТИЛИ ЧАСОВ – добавлены дополнительные варианты отображения времени и даты с кастомизацией цвета',
    '🎨 УЛУЧШЕННАЯ ПАНЕЛЬ НАСТРОЕК – более гармоничный дизайн и удобная навигация',
    '🔌 СИСТЕМА ПЛАГИНОВ – поддержка расширений LauncherHub для добавления новых возможностей',
    '🎯 FOCUS MODE PLUGIN – режим концентрации с Pomodoro таймером и минималистичным интерфейсом',
    '🌦 SMART WEATHER PLUGIN – отображение температуры, влажности и скорости ветра',
    '🎵 SMART MUSIC CONTROLLER – управление музыкой через встроенный мини-плеер',
    '📂 SMART FILE FINDER И IDEA NOTEBOOK – быстрый поиск файлов и встроенный блокнот для идей',
  ],
  '2.2': [
    '🚀 LAUNCHER HAB 2.2 - ОПТИМИЗАЦИЯ И КАСТОМИЗАЦИЯ',
    '⚡ ОПТИМИЗАЦИЯ ПРОИЗВОДИТЕЛЬНОСТИ - снижение потребления памяти на 25% и ускорение загрузки',
    '🎨 КАСТОМИЗАЦИЯ ВРЕМЕНИ И ДАТЫ - выбор шрифтов, размеров, цветов и форматов отображения',
    '💾 СИСТЕМА РЕЗЕРВНОГО КОПИРОВАНИЯ - автоматическое и ручное создание бэкапов настроек',
    '🔍 КЭШИРОВАНИЕ ПОИСКА - мгновенный поиск по приложениям с интеллектуальным кэшированием',
    '🎯 ВИРТУАЛИЗАЦИЯ СПИСКОВ - плавная работа с большими библиотеками приложений (1000+)',
    '🛠️ УЛУЧШЕННОЕ УПРАВЛЕНИЕ ПАМЯТЬЮ - автоматическая очистка неиспользуемых ресурсов',
    '📊 МОНИТОРИНГ ПРОИЗВОДИТЕЛЬНОСТИ - отслеживание использования CPU, памяти и кэша',
    '🔧 ГИБКИЕ НАСТРОЙКИ ПРОИЗВОДИТЕЛЬНОСТИ - индивидуальная настройка кэширования и виртуализации',
  ],
  '2.1': [
    '🚀 LAUNCHER HAB 2.1 - НОВЫЕ ВОЗМОЖНОСТИ И РАСШИРЕНИЯ',
    '🔌 СИСТЕМА ПЛАГИНОВ - поддержка сторонних расширений и модулей',
    '🔊 УПРАВЛЕНИЕ АУДИО - встроенный контроллер громкости с поддержкой всех ОС',
    '🎨 СОЗДАНИЕ ТЕМ - визуальный редактор пользовательских цветовых схем',
    '💫 РАСШИРЕННОЕ СТЕКЛО - тонкая настройка прозрачности стеклянного эффекта',
    '🏷️ СИСТЕМА ТЕГОВ - организация приложений с помощью пользовательских меток',
    '🔍 ПОИСК ПО ТЕГАМ - быстрая фильтрация приложений по категориям и тегам',
    '📊 ПРОДВИНУТЫЕ НАСТРОЙКИ - новые вкладки для управления всеми функциями',
    '🛠️ УЛУЧШЕННАЯ АРХИТЕКТУРА - модульная структура для легкого расширения',
    '🔒 БЕЗОПАСНОСТЬ ПЛАГИНОВ - изолированная среда выполнения стороннего кода',
    '🎯 АВТОМАТИЧЕСКОЕ ОБНАРУЖЕНИЕ - сканирование папки plugins при запуске',
  ],
  '2.0': [
    '🎉 КРУПНОЕ ОБНОВЛЕНИЕ LAUNCHER HAB 2.0!',
    '✨ Полностью переработанный дизайн с эффектом жидкого стекла (Glass Morphism)',
    '🎬 Плавные анимации в стиле Android с поддержкой кривых Безье',
    '🔐 Шифрование пользовательских данных с использованием алгоритма Fernet',
    '📡 Расширенный мониторинг системы: отслеживание Bluetooth, Wi-Fi и геолокации',
    '🎨 7 предустановленных цветовых тем (Темная, Светлая, Синяя, Зеленая, Фиолетовая, Оранжевая, Розовая)',
    '⚡ Настройка интенсивности стеклянного эффекта (Слабая, Средняя, Сильная)',
    '🔄 Улучшенная система фильтрации с диалоговым меню',
    '📱 Адаптивная сетка карточек приложений с эффектами наведения',
    '🔔 Интеллектуальная система уведомлений о действиях пользователя',
    '🛡️ Повышенная стабильность работы и обработка ошибок',
    '💾 Автоматическое сохранение всех настроек в зашифрованном виде',
  ],
  '1.9': [
    'Добавлен мониторинг системных ресурсов (CPU, память, батарея, сеть)',
    'Реализована система автоматического определения установленных приложений',
    'Улучшена производительность при работе с большими списками приложений',
    'Добавлена поддержка пользовательских путей к приложениям',
    'Исправлены ошибки при запуске веб-приложений',
  ],
  '1.8': [
    'Внедрена система избранных приложений (до 10 элементов)',
    'Добавлена панель быстрого доступа к часто используемым программам',
    'Реализовано контекстное меню для управления приложениями',
    'Улучшен поиск с поддержкой фильтрации по категориям',
    'Обновлен интерфейс боковой панели',
  ],
  '1.7': [
    'Добавлена возможность добавления собственных приложений и сайтов',
    'Реализован выбор иконок для пользовательских элементов',
    'Внедрена система категорий (Браузеры, Медиа, Музыка, Соцсети, Игры, Система, Офис)',
    'Улучшена навигация по категориям приложений',
    'Добавлены подсказки при наведении на элементы интерфейса',
  ],
  '1.6': [
    'Разработана базовая система тем оформления (Темная и Светлая)',
    'Добавлены часы и дата в заголовок приложения',
    'Реализовано автообновление времени каждую секунду',
    'Улучшена адаптивность интерфейса при изменении размера окна',
    'Исправлены проблемы с отображением кириллицы',
  ],
  '1.5': [
    'Добавлена функция поиска по приложениям в реальном времени',
    'Реализована фильтрация приложений по типам (Все, Приложения, Сайты, Система)',
    'Улучшена визуальная обратная связь при взаимодействии с элементами',
    'Оптимизирована загрузка иконок приложений',
    'Добавлена поддержка горячих клавиш',
  ],
  '1.4': [
    'Расширена база предустановленных приложений (более 30 программ)',
    'Добавлена проверка наличия приложений в системе',
    'Реализовано перенаправление на официальные сайты для неустановленных программ',
    'Улучшена обработка ошибок при запуске приложений',
    'Обновлен дизайн карточек приложений',
  ],
  '1.3': [
    'Добавлена поддержка запуска системных утилит Windows и Linux',
    'Реализована кроссплатформенная совместимость (Windows, Linux, macOS)',
    'Улучшена система определения путей к исполняемым файлам',
    'Добавлен индикатор загрузки при запуске тяжелых приложений',
    'Исправлены ошибки при работе в различных окружениях',
  ],
  '1.2': [
    'Внедрено сохранение настроек между сеансами работы',
    'Добавлено диалоговое окно настроек приложения',
    'Реализована возможность сброса избранного и пользовательских путей',
    'Улучшена структура хранения конфигурационных файлов',
    'Повышена общая стабильность приложения',
  ],
  '1.1': [
    'Добавлена боковая панель со списком всех приложений',
    'Реализовано разделение интерфейса на функциональные зоны',
    'Улучшено отображение статуса статуса установки приложений',
    'Добавлены базовые анимации при наведении курсора',
    'Исправлены мелкие визуальные недочеты',
  ],
  '1.0': [
    '🚀 Первый официальный релиз Launcher Hab!',
    'Базовый функционал запуска приложений и веб-сайтов',
    'Простой и понятный пользовательский интерфейс на базе Flet',
    'Поддержка основных браузеров и медиа-плееров',
    'Фундамент для будущих обновлений и расширений',
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
