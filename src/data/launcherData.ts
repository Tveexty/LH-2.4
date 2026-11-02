export type ThemeKey = 'dark' | 'light' | 'purple' | 'spring';
export type ClockStyleKey = 'standard' | 'stacked' | 'minimal' | 'pill_glass' | 'cyber_mono' | 'compact_badge';
export type GlassIntensity = 'light' | 'medium' | 'strong';
export type AppType = 'app' | 'web' | 'system';

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
  dailyLimitMinutes: number;
  detoxGroup: string;
  isRunning?: boolean;
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
  description: string;
  enabled: boolean;
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

export const THEMES: Record<ThemeKey, {
  name: string;
  isDark: boolean;
  bgGradient: string;
  surfaceRgba: string;
  accent: string;
  accentHex: string;
}> = {
  dark: {
    name: 'Темная',
    isDark: true,
    bgGradient: 'radial-gradient(circle at 18% 15%, rgba(59, 130, 246, 0.16), transparent 42%), radial-gradient(circle at 82% 80%, rgba(99, 102, 241, 0.12), transparent 45%), linear-gradient(145deg, #11141c 0%, #171b26 55%, #12151e 100%)',
    surfaceRgba: 'rgba(30, 35, 48, 0.58)',
    accent: 'blue',
    accentHex: '#4285f4',
  },
  light: {
    name: 'Светлая',
    isDark: false,
    bgGradient: 'radial-gradient(circle at 20% 15%, rgba(59, 130, 246, 0.12), transparent 45%), radial-gradient(circle at 80% 85%, rgba(14, 165, 233, 0.10), transparent 45%), linear-gradient(145deg, #eef2f7 0%, #f8fafc 60%, #e2e8f0 100%)',
    surfaceRgba: 'rgba(255, 255, 255, 0.68)',
    accent: 'blue',
    accentHex: '#2563eb',
  },
  purple: {
    name: 'Фиолетовая',
    isDark: true,
    bgGradient: 'radial-gradient(circle at 22% 18%, rgba(168, 85, 247, 0.22), transparent 45%), radial-gradient(circle at 80% 78%, rgba(217, 70, 239, 0.14), transparent 45%), linear-gradient(145deg, #131124 0%, #1d1936 55%, #141229 100%)',
    surfaceRgba: 'rgba(39, 34, 68, 0.58)',
    accent: 'purple',
    accentHex: '#a855f7',
  },
  spring: {
    name: 'Весна',
    isDark: false,
    bgGradient: 'radial-gradient(circle at 22% 18%, rgba(236, 72, 153, 0.15), transparent 45%), radial-gradient(circle at 80% 78%, rgba(244, 114, 182, 0.14), transparent 45%), linear-gradient(145deg, #fff5f8 0%, #fce7f3 60%, #fbcfe8 100%)',
    surfaceRgba: 'rgba(255, 245, 250, 0.72)',
    accent: 'pink',
    accentHex: '#e91e63',
  },
};

export const CLOCK_STYLE_OPTIONS: { id: ClockStyleKey; label: string; sample: string }[] = [
  { id: 'standard', label: 'Классический', sample: '14:32:08' },
  { id: 'stacked', label: 'Stacked (Вертикальный)', sample: '14 / 32' },
  { id: 'minimal', label: 'Минималистичный', sample: '14:32' },
  { id: 'pill_glass', label: 'Стеклянная капсула', sample: '14:32 • Пн, 02.11' },
  { id: 'cyber_mono', label: 'Цифровой Моно', sample: '[ 14 : 32 : 08 ]' },
  { id: 'compact_badge', label: 'Компактный с днем недели', sample: 'Пн • 14:32' },
];

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
    monthMinutes: 2520, // 42 ч в месяц
    weekMinutes: 840,
    todayMinutes: 95,
    dailyLimitMinutes: 180,
    detoxGroup: 'Игры',
    isRunning: true,
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
    monthMinutes: 1980, // 33 ч в месяц
    weekMinutes: 520,
    todayMinutes: 75,
    dailyLimitMinutes: 240,
    detoxGroup: 'Браузеры',
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
    monthMinutes: 1140, // 19 ч в месяц
    weekMinutes: 310,
    todayMinutes: 52,
    dailyLimitMinutes: 60,
    detoxGroup: 'Соцсети и мессенджеры',
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
    monthMinutes: 660, // 11 ч в месяц
    weekMinutes: 175,
    todayMinutes: 35,
    dailyLimitMinutes: 60,
    detoxGroup: 'Соцсети и мессенджеры',
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
    monthMinutes: 1560, // 26 ч в месяц
    weekMinutes: 410,
    todayMinutes: 65,
    dailyLimitMinutes: 90,
    detoxGroup: 'Медиа',
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
    monthMinutes: 480, // 8 ч в месяц
    weekMinutes: 120,
    todayMinutes: 20,
    dailyLimitMinutes: 180,
    detoxGroup: 'Медиа',
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
    monthMinutes: 720, // 12 ч в месяц
    weekMinutes: 190,
    todayMinutes: 30,
    dailyLimitMinutes: 180,
    detoxGroup: 'Медиа',
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
    monthMinutes: 900, // 15 ч в месяц
    weekMinutes: 240,
    todayMinutes: 40,
    dailyLimitMinutes: 180,
    detoxGroup: 'Медиа',
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
    monthMinutes: 420, // 7 ч в месяц
    weekMinutes: 95,
    todayMinutes: 15,
    dailyLimitMinutes: 240,
    detoxGroup: 'Браузеры',
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
    monthMinutes: 840, // 14 ч в месяц
    weekMinutes: 210,
    todayMinutes: 45,
    dailyLimitMinutes: 180,
    detoxGroup: 'Игры',
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
    monthMinutes: 65,
    weekMinutes: 20,
    todayMinutes: 5,
    dailyLimitMinutes: 300,
    detoxGroup: 'Система',
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
    monthMinutes: 360, // 6 ч в месяц
    weekMinutes: 90,
    todayMinutes: 15,
    dailyLimitMinutes: 300,
    detoxGroup: 'Система',
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
    monthMinutes: 180, // 3 ч в месяц
    weekMinutes: 45,
    todayMinutes: 8,
    dailyLimitMinutes: 300,
    detoxGroup: 'Система',
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
    monthMinutes: 540, // 9 ч в месяц
    weekMinutes: 130,
    todayMinutes: 25,
    dailyLimitMinutes: 300,
    detoxGroup: 'Система',
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
    monthMinutes: 600, // 10 ч в месяц
    weekMinutes: 160,
    todayMinutes: 30,
    dailyLimitMinutes: 300,
    detoxGroup: 'Работа',
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
    monthMinutes: 240, // 4 ч в месяц
    weekMinutes: 60,
    todayMinutes: 10,
    dailyLimitMinutes: 300,
    detoxGroup: 'Работа',
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
    description: 'Отслеживает время в каждом запущенном приложении или игре (аналог статистики Steam / Экранного времени), выводит часы на карточках («42 ч в мес»), строит графики (день/неделя/месяц) и контролирует лимиты детокса.',
    enabled: true,
    file: 'plugins/session_tracker_plugin.py',
    hooks: ['on_load', 'on_app_launched', 'on_tick', 'get_app_card_badge', 'get_ui_component'],
  },
  {
    id: 'focus_mode_plugin',
    name: 'Focus Mode (Pomodoro)',
    version: '2.3.0',
    description: 'Режим концентрации с Pomodoro-таймером на 25 минут и автоматическим закрытием отвлекающих мессенджеров.',
    enabled: true,
    file: 'plugins/focus_mode_plugin.py',
    hooks: ['set_context', 'get_ui_component'],
  },
  {
    id: 'smart_music_controller',
    name: 'Smart Music Controller',
    version: '2.3.0',
    description: 'Встроенный мини-плеер для быстрого переключения треков и управления медиапотоком.',
    enabled: true,
    file: 'plugins/smart_music_controller.py',
    hooks: ['get_ui_component'],
  },
  {
    id: 'smart_weather_plugin',
    name: 'Smart Weather Plugin',
    version: '2.3.0',
    description: 'Отображение актуальной температуры, влажности и скорости ветра прямо в панели расширений.',
    enabled: true,
    file: 'plugins/smart_weather_plugin.py',
    hooks: ['get_ui_component'],
  },
  {
    id: 'smart_file_finder',
    name: 'Smart File Finder',
    version: '2.3.0',
    description: 'Быстрый мгновенный поиск локальных файлов по рабочей директории.',
    enabled: false,
    file: 'plugins/smart_file_finder.py',
    hooks: ['get_ui_component'],
  },
  {
    id: 'idea_notebook_plugin',
    name: 'Idea Notebook',
    version: '2.3.0',
    description: 'Быстрые заметки и сохранение идей в idea_notes.txt по горячей клавише Ctrl + Alt + N.',
    enabled: true,
    file: 'plugins/idea_notebook_plugin.py',
    hooks: ['get_ui_component'],
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
    path: 'plugins/session_tracker_plugin.py',
    title: 'plugins/session_tracker_plugin.py',
    badge: 'NEW v2.4',
    summary: 'Плагин Game & App Session Tracker: учет времени, бейджи «42 ч в мес», графики День/Неделя/Месяц и группы детокса.',
  },
  {
    path: 'modules/glass_morphism.py',
    title: 'modules/glass_morphism.py',
    badge: 'UPDATED v2.4',
    summary: 'Настоящее прозрачное стекло с аппаратным размытием ft.Blur, плавной анимацией и поддержкой бейджей времени на карточках.',
  },
  {
    path: 'modules/audio_controller.py',
    title: 'modules/audio_controller.py',
    badge: 'UPDATED v2.4',
    summary: 'Неблокирующий фоновый контроллер системной громкости (pycaw CoreAudio COM в фоновом потоке + Linux/macOS + Mute).',
  },
  {
    path: 'modules/plugin_manager.py',
    title: 'modules/plugin_manager.py',
    badge: 'UPDATED v2.4',
    summary: 'Расширенный PluginAPI 2.4 с хуками on_app_launched, on_tick, get_app_card_badge и встроенным SDK-генератором шаблонов.',
  },
  {
    path: 'modules/ui_dialogs_add_app.py',
    title: 'modules/ui_dialogs_add_app.py',
    badge: 'UPDATED v2.4',
    summary: 'Улучшенное единое окно добавления приложения: живое превью карточки, поиск по 70+ иконкам, CLI-аргументы и лимит детокса.',
  },
  {
    path: 'modules/ui_panels.py',
    title: 'modules/ui_panels.py',
    badge: 'UPDATED v2.4',
    summary: 'Плавные переходы между разделами через ft.AnimatedSwitcher, переключатель Трекер/Приложения и 6 стилей часов.',
  },
  {
    path: 'modules/ui_manager_core.py',
    title: 'modules/ui_manager_core.py',
    badge: 'UPDATED v2.4',
    summary: 'Ядро Launcher Hab 2.4: фоновый тик плагинов, интеграция трекера при запуске приложений и обновление стилей часов.',
  },
  {
    path: 'modules/ui_dialogs.py',
    title: 'modules/ui_dialogs.py',
    badge: 'UPDATED v2.4',
    summary: 'Настройки 6 стилей часов, быстрые цветовые пресеты, управление плагинами и история обновлений версии 2.4.',
  },
  {
    path: 'modules/theme_manager.py',
    title: 'modules/theme_manager.py',
    badge: 'UPDATED v2.4',
    summary: 'Хранение настроек прозрачного стекла, 6 стилей часов (standard, stacked, minimal, pill_glass, cyber_mono, compact_badge).',
  },
  {
    path: 'версии .txt',
    title: 'версии .txt',
    badge: 'CHANGELOG 2.4',
    summary: 'Полный список изменений новой версии Launcher Hab 2.4.',
  },
  {
    path: 'main.py',
    title: 'main.py',
    badge: 'ENTRY',
    summary: 'Точка входа Flet-приложения Launcher Hab 2.4.',
  },
];

export const VERSION_HISTORY: Record<string, string[]> = {
  '2.4': [
    '🚀 LAUNCHER HUB 2.4 – ПРОЗРАЧНОЕ СТЕКЛО, SESSION TRACKER И PLUGIN API 2.4',
    '🔮 НАСТОЯЩИЙ ЭФФЕКТ ПРОЗРАЧНОГО СТЕКЛА (GLASSMORPHISM 2.4) – аппаратное размытие заднего фона (ft.Blur), стеклянные блики границ и настраиваемая прозрачность',
    '✨ ПЛАВНАЯ АНИМАЦИЯ ПЕРЕХОДОВ МЕЖДУ РАЗДЕЛАМИ – мягкие переходы между библиотекой, фильтрами, поиском и трекером времени через AnimatedSwitcher',
    '➕ УЛУЧШЕННОЕ ОКНО «ДОБАВИТЬ ПРИЛОЖЕНИЕ» – живое превью карточки, поиск по 70+ иконкам, автоопределение типа (EXE / URL), CLI-аргументы и лимит времени',
    '🧩 ПЛАТФОРМА РАСШИРЕНИЙ И PLUGIN API 2.4 – новый SDK с хуками жизненного цикла (on_app_launched, on_tick), бейджами карточек и генератором шаблонов',
    '🔊 ФОНОВЫЙ КОНТРОЛЛЕР СИСТЕМНОЙ ГРОМКОСТИ – мгновенное изменение громкости в фоновом потоке через CoreAudio (pycaw / COM Interop) без зависаний и кнопка Mute',
    '🎮 ПЛАГИН «GAME & APP SESSION TRACKER» – отслеживание игрового и экранного времени: бейджи на карточках («Steam — 42 ч в мес») и графики за день/неделю/месяц',
    '🛑 ГРУППЫ ЦИФРОВОГО ДЕТОКСА – настраиваемые дневные лимиты для игр, соцсетей и медиа с автоматическими уведомлениями при превышении',
    '🕒 РАСШИРЕННАЯ КАСТОМИЗАЦИЯ СТИЛЕЙ ЧАСОВ – 6 стилей часов (Классический, Stacked, Минималистичный, Стеклянная капсула, Цифровой Моно, Компактный), управление секундами, днем недели и пресетами цвета',
  ],
  '2.3': [
    '🎨 УЛУЧШЕННЫЙ LIQUID GLASS ИНТЕРФЕЙС – переработанный стеклянный дизайн и эффекты прозрачности',
    '🖥 FLOATING HUD – плавающая панель с системной информацией CPU/RAM',
    '🗑 ФИКСИРОВАННАЯ КОРЗИНА – быстрый доступ к корзине в правом нижнем углу',
    '🔎 ИСТОРИЯ ПОИСКА – сохранение предыдущих поисковых запросов',
    '🔌 СИСТЕМА ПЛАГИНОВ – базовая поддержка расширений LauncherHub',
    '🎯 FOCUS MODE, SMART WEATHER, SMART MUSIC, FILE FINDER, IDEA NOTEBOOK',
  ],
  '2.2': [
    '⚡ ОПТИМИЗАЦИЯ ПРОИЗВОДИТЕЛЬНОСТИ – кэширование поиска и виртуализация списков',
    '💾 СИСТЕМА РЕЗЕРВНОГО КОПИРОВАНИЯ – автоматическое сохранение и восстановление настроек',
    '⌨️ РАСШИРЕННЫЕ ГОРЯЧИЕ КЛАВИШИ – кастомные комбинации клавиш',
  ],
};

export function formatMonthBadge(minutes: number): string {
  const hours = minutes / 60;
  if (hours >= 10) return `${Math.round(hours)} ч в мес`;
  if (hours >= 1) return `${hours.toFixed(1)} ч в мес`;
  if (minutes > 0) return `${minutes} мин в мес`;
  return '0 ч в мес';
}

export function formatDurationRu(minutes: number): string {
  const h = Math.floor(minutes / 60);
  const m = Math.round(minutes % 60);
  if (h > 0 && m > 0) return `${h} ч ${m} мин`;
  if (h > 0) return `${h} ч`;
  return `${m} мин`;
}
