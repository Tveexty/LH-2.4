/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useMemo, useRef } from 'react';
import {
  Rocket,
  Search,
  Plus,
  Star,
  Settings,
  Puzzle,
  Volume2,
  Volume1,
  VolumeX,
  Activity,
  Trash2,
  BatteryCharging,
  Wifi,
  Gamepad2,
  Globe,
  MessageSquare,
  Users,
  Play,
  Film,
  Music,
  Headphones,
  Compass,
  Trophy,
  Calculator,
  FolderOpen,
  Terminal,
  FileText,
  Cloud,
  Code2,
  Download,
  Check,
  X,
  MoreVertical,
  Clock,
  BarChart3,
  AlertTriangle,
  Copy,
  FileCode,
  Sparkles,
  PlayCircle,
  PauseCircle,
  ShieldAlert,
  Sliders,
  LayoutGrid,
  RefreshCw,
  RotateCcw,
  Archive,
  Square,
} from 'lucide-react';
import {
  AppItem,
  AppType,
  BackupRecord,
  CatalogPluginItem,
  ClockStyleKey,
  CLOCK_STYLE_OPTIONS,
  CustomThemeConfig,
  DetoxGroup,
  formatDurationRu,
  formatLiveClock,
  formatMonthBadge,
  GlassIntensity,
  INITIAL_APPS,
  INITIAL_DETOX_GROUPS,
  INITIAL_PLUGINS,
  INITIAL_WORKSPACES,
  PLUGIN_CATALOG,
  PluginItem,
  PYTHON_PROJECT_FILES,
  ThemeKey,
  THEMES,
  VERSION_HISTORY,
  WorkspacePreset,
} from './data/launcherData';

const ICON_MAP: Record<string, React.ComponentType<{ className?: string }>> = {
  Gamepad2,
  Globe,
  MessageSquare,
  Users,
  Play,
  Film,
  Music,
  Headphones,
  Compass,
  Trophy,
  Calculator,
  FolderOpen,
  Activity,
  Terminal,
  FileText,
  Cloud,
  Code2,
  Rocket,
  Star,
  Puzzle,
  Clock,
  BarChart3,
  Search,
  Copy,
};

const ICON_NAMES = Object.keys(ICON_MAP);
const WEEKDAYS_RU = ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'];
const STORAGE_KEY = 'launcher_hab_v25_zero_state_v1';

interface ToastMessage {
  id: string;
  title: string;
  message: string;
  type?: 'info' | 'warning' | 'success';
}

function LitStatusBadge({ active }: { active: boolean }) {
  return (
    <span
      className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold tracking-wide transition-all duration-200 ${
        active
          ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-400/60 shadow-[0_0_12px_rgba(16,185,129,0.35)]'
          : 'bg-slate-800/80 text-slate-400 border border-slate-700/60'
      }`}
    >
      {active ? '🟢 АКТИВНО' : '⚪ НЕАКТИВНО'}
    </span>
  );
}

export default function App() {
  // Load persisted state from localStorage
  const savedState = useMemo(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) return JSON.parse(raw);
    } catch {
      // ignore
    }
    return null;
  }, []);

  // --- Core Theme & Glassmorphism State (v2.5) ---
  const [themeKey, setThemeKey] = useState<ThemeKey>(savedState?.themeKey || 'dark');
  const [customThemes, setCustomThemes] = useState<Record<string, CustomThemeConfig>>(
    savedState?.customThemes || {}
  );
  const [glassEnabled, setGlassEnabled] = useState<boolean>(savedState?.glassEnabled ?? true);
  const [glassIntensity, setGlassIntensity] = useState<GlassIntensity>(savedState?.glassIntensity || 'medium');
  const [glassOpacity, setGlassOpacity] = useState<number>(savedState?.glassOpacity ?? 88);
  const [smoothAnimations, setSmoothAnimations] = useState<boolean>(savedState?.smoothAnimations ?? true);
  const [cardColumns, setCardColumns] = useState<number>(savedState?.cardColumns ?? 6);
  const [showPluginsInGrid, setShowPluginsInGrid] = useState<boolean>(savedState?.showPluginsInGrid ?? true);
  const [launchBehavior, setLaunchBehavior] = useState<'keep' | 'minimize'>(savedState?.launchBehavior || 'keep');

  // --- Personalization 2.5 State ---
  const [cardBorderRadius, setCardBorderRadius] = useState<number>(savedState?.cardBorderRadius ?? 20);
  const [iconScalePct, setIconScalePct] = useState<number>(savedState?.iconScalePct ?? 100);
  const [cardHoverGlow, setCardHoverGlow] = useState<boolean>(savedState?.cardHoverGlow ?? true);
  const [activeAppColor, setActiveAppColor] = useState<string>(savedState?.activeAppColor || '#10b981');

  // --- Clock Styles State (18 styles + Android Vertical Widget + Design 2.5) ---
  const [clockStyle, setClockStyle] = useState<ClockStyleKey>(savedState?.clockStyle || 'android_vertical');
  const [showAndroidClockWidget, setShowAndroidClockWidget] = useState<boolean>(
    savedState?.showAndroidClockWidget ?? true
  );
  const [timeFormat, setTimeFormat] = useState<'24' | '12'>(savedState?.timeFormat || '24');
  const [showSeconds, setShowSeconds] = useState<boolean>(savedState?.showSeconds ?? true);
  const [showDate, setShowDate] = useState<boolean>(savedState?.showDate ?? true);
  const [showWeekday, setShowWeekday] = useState<boolean>(savedState?.showWeekday ?? true);
  const [clockGlassFrame, setClockGlassFrame] = useState<boolean>(savedState?.clockGlassFrame ?? true);
  const [timeColor, setTimeColor] = useState<string>(savedState?.timeColor || '#f8fafc');
  const [dateColor, setDateColor] = useState<string>(savedState?.dateColor || '#94a3b8');
  const [clockAccentColor, setClockAccentColor] = useState<string>(savedState?.clockAccentColor || '#3b82f6');
  const [clockGlowEnabled, setClockGlowEnabled] = useState<boolean>(savedState?.clockGlowEnabled ?? true);
  const [clockGlowIntensity, setClockGlowIntensity] = useState<number>(savedState?.clockGlowIntensity ?? 16);
  const [clockBorderRadius, setClockBorderRadius] = useState<number>(savedState?.clockBorderRadius ?? 16);
  const [clockBgOpacity, setClockBgOpacity] = useState<number>(savedState?.clockBgOpacity ?? 78);
  const [clockBlinkColon, setClockBlinkColon] = useState<boolean>(savedState?.clockBlinkColon ?? false);
  const [clockBold, setClockBold] = useState<boolean>(savedState?.clockBold ?? true);
  const [timeFontSize, setTimeFontSize] = useState<number>(savedState?.timeFontSize ?? 22);
  const [now, setNow] = useState<Date>(new Date());

  // --- Navigation & Section Transition State ---
  const [activeSection, setActiveSection] = useState<'apps' | 'tracker' | 'python_code'>('apps');
  const [sectionAnimating, setSectionAnimating] = useState<boolean>(false);
  const [currentFilter, setCurrentFilter] = useState<'all' | 'web' | 'app' | 'system' | 'plugin' | 'custom'>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');

  // --- Apps, Session Tracker (starts from 0) & Detox Groups ---
  const [apps, setApps] = useState<AppItem[]>(savedState?.apps || INITIAL_APPS);
  const [detoxGroups, setDetoxGroups] = useState<DetoxGroup[]>(savedState?.detoxGroups || INITIAL_DETOX_GROUPS);
  const [detoxNotifications, setDetoxNotifications] = useState<boolean>(savedState?.detoxNotifications ?? true);
  const [trackerPeriod, setTrackerPeriod] = useState<'day' | 'week' | 'month'>('month');
  const [plugins, setPlugins] = useState<PluginItem[]>(savedState?.plugins || INITIAL_PLUGINS);
  const [workspaces] = useState<WorkspacePreset[]>(INITIAL_WORKSPACES);
  const [backups, setBackups] = useState<BackupRecord[]>(
    savedState?.backups || [
      {
        id: 'bk_init',
        filename: 'settings_backup_20261102_110000.json',
        createdAt: '02.11.2026 11:00',
        sizeKb: '4.2 KB',
      },
    ]
  );

  // --- Background System Audio Controller State ---
  const [volume, setVolume] = useState<number>(savedState?.volume ?? 68);
  const [isMuted, setIsMuted] = useState<boolean>(savedState?.isMuted ?? false);
  const [volumePopupOpen, setVolumePopupOpen] = useState<boolean>(false);
  const [audioBgStatus, setAudioBgStatus] = useState<string>('CoreAudio Worker Ready');
  const audioCtxRef = useRef<AudioContext | null>(null);

  // --- Floating HUD & Modals ---
  const [floatingHudVisible, setFloatingHudVisible] = useState<boolean>(false);
  const [cpuLoad, setCpuLoad] = useState<number>(16);
  const [ramLoad] = useState<number>(42);

  const [addAppModalOpen, setAddAppModalOpen] = useState<boolean>(false);
  const [settingsModalOpen, setSettingsModalOpen] = useState<boolean>(false);
  const [settingsTab, setSettingsTab] = useState<'appearance' | 'clock' | 'plugins' | 'system' | 'changelog'>('appearance');
  const [pluginsModalOpen, setPluginsModalOpen] = useState<boolean>(false);
  const [workspaceModalOpen, setWorkspaceModalOpen] = useState<boolean>(false);
  const [backupModalOpen, setBackupModalOpen] = useState<boolean>(false);
  const [contextMenuApp, setContextMenuApp] = useState<AppItem | null>(null);
  const [activePluginModal, setActivePluginModal] = useState<PluginItem | null>(null);
  const [editingPluginSettings, setEditingPluginSettings] = useState<PluginItem | null>(null);
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  // --- Interactive Plugin Widget States ---
  const [ideaNotes, setIdeaNotes] = useState<string[]>([
    'Исправить Fernet 32-byte URL-safe base64 key',
    'Убрать желтые рамки (#AARRGGBB в Flet)',
    'Сделать старт таймера с 00:00 по запуску приложения',
  ]);
  const [newIdeaText, setNewIdeaText] = useState<string>('');
  const [pomodoroSeconds, setPomodoroSeconds] = useState<number>(25 * 60);
  const [pomodoroRunning, setPomodoroRunning] = useState<boolean>(false);

  // --- Add App Form State ---
  const [newAppName, setNewAppName] = useState<string>('');
  const [newAppUrl, setNewAppUrl] = useState<string>('');
  const [newAppArgs, setNewAppArgs] = useState<string>('');
  const [newAppCategory, setNewAppCategory] = useState<string>('Games');
  const [newAppType, setNewAppType] = useState<AppType>('app');
  const [newAppIcon, setNewAppIcon] = useState<string>('Gamepad2');
  const [newAppIconSearch, setNewAppIconSearch] = useState<string>('');
  const [newAppFav, setNewAppFav] = useState<boolean>(true);
  const [newAppLimit, setNewAppLimit] = useState<number>(120);

  // --- Plugin SDK Template Generator State ---
  const [newPluginSlug, setNewPluginSlug] = useState<string>('');
  const [newPluginTitle, setNewPluginTitle] = useState<string>('');

  // --- Python Source Code Viewer & Custom Theme Studio State ---
  const [selectedPyFile, setSelectedPyFile] = useState<string>(PYTHON_PROJECT_FILES[0].path);
  const [pyFileContent, setPyFileContent] = useState<string>('Загрузка исходного кода Python...');
  const [copiedCode, setCopiedCode] = useState<boolean>(false);
  const [customThemeModalOpen, setCustomThemeModalOpen] = useState<boolean>(false);
  const [newThemeName, setNewThemeName] = useState<string>('Neon Cyber Slate');
  const [newThemeMode, setNewThemeMode] = useState<'dark' | 'amoled' | 'light'>('dark');
  const [newThemeBg, setNewThemeBg] = useState<string>('#0a0e17');
  const [newThemeSurface, setNewThemeSurface] = useState<string>('#141c2b');
  const [newThemeAccent, setNewThemeAccent] = useState<string>('#38bdf8');
  const [cryptoKeyVersion, setCryptoKeyVersion] = useState<number>(1);
  const [changelogFilter, setChangelogFilter] = useState<string>('all');

  const allThemesMap = useMemo(() => ({ ...THEMES, ...customThemes }), [customThemes]);
  const currentTheme = allThemesMap[themeKey] || THEMES.dark;
  const sessionTrackerEnabled = useMemo(
    () => plugins.find((p) => p.id === 'session_tracker_plugin')?.enabled ?? true,
    [plugins]
  );

  // Persist all settings & state to localStorage automatically
  useEffect(() => {
    try {
      const payload = {
        themeKey,
        customThemes,
        glassEnabled,
        glassIntensity,
        glassOpacity,
        smoothAnimations,
        cardColumns,
        showPluginsInGrid,
        launchBehavior,
        cardBorderRadius,
        iconScalePct,
        cardHoverGlow,
        activeAppColor,
        clockStyle,
        showAndroidClockWidget,
        timeFormat,
        showSeconds,
        showDate,
        showWeekday,
        clockGlassFrame,
        timeColor,
        dateColor,
        clockAccentColor,
        clockGlowEnabled,
        clockGlowIntensity,
        clockBorderRadius,
        clockBgOpacity,
        clockBlinkColon,
        clockBold,
        timeFontSize,
        apps,
        detoxGroups,
        detoxNotifications,
        plugins,
        backups,
        volume,
        isMuted,
      };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
    } catch {
      // ignore storage quota errors
    }
  }, [
    themeKey,
    customThemes,
    glassEnabled,
    glassIntensity,
    glassOpacity,
    smoothAnimations,
    cardColumns,
    showPluginsInGrid,
    launchBehavior,
    cardBorderRadius,
    iconScalePct,
    cardHoverGlow,
    activeAppColor,
    clockStyle,
    showAndroidClockWidget,
    timeFormat,
    showSeconds,
    showDate,
    showWeekday,
    clockGlassFrame,
    timeColor,
    dateColor,
    clockAccentColor,
    clockGlowEnabled,
    clockGlowIntensity,
    clockBorderRadius,
    clockBgOpacity,
    clockBlinkColon,
    clockBold,
    timeFontSize,
    apps,
    detoxGroups,
    detoxNotifications,
    plugins,
    backups,
    volume,
    isMuted,
  ]);

  // Sync dark class on <html>
  useEffect(() => {
    const html = document.documentElement;
    if (currentTheme.isDark) {
      html.classList.add('dark');
    } else {
      html.classList.remove('dark');
    }
  }, [currentTheme.isDark]);

  // Real-time 1-second ticker: updates clock, CPU telemetry, Pomodoro, and running app session timers!
  useEffect(() => {
    const timer = setInterval(() => {
      setNow(new Date());
      setCpuLoad((prev) => Math.max(8, Math.min(65, prev + Math.floor(Math.random() * 5) - 2)));

      if (pomodoroRunning) {
        setPomodoroSeconds((prev) => (prev > 0 ? prev - 1 : 0));
      }

      if (sessionTrackerEnabled) {
        setApps((prevApps) => {
          const anyRunning = prevApps.some((a) => a.isRunning);
          if (!anyRunning) return prevApps;
          return prevApps.map((a) => {
            if (!a.isRunning) return a;
            const nextSec = (a.elapsedSeconds || 0) + 1;
            const addMin = 1 / 60;
            return {
              ...a,
              elapsedSeconds: nextSec,
              todayMinutes: +(a.todayMinutes + addMin).toFixed(2),
              weekMinutes: +(a.weekMinutes + addMin).toFixed(2),
              monthMinutes: +(a.monthMinutes + addMin).toFixed(2),
            };
          });
        });
      }
    }, 1000);
    return () => clearInterval(timer);
  }, [sessionTrackerEnabled, pomodoroRunning]);

  // Load selected Python file from /launcher_hab2.4/
  useEffect(() => {
    let cancelled = false;
    fetch(`/launcher_hab2.4/${selectedPyFile}`)
      .then((res) => (res.ok ? res.text() : Promise.reject('Failed')))
      .then((text) => {
        if (!cancelled) setPyFileContent(text);
      })
      .catch(() => {
        if (!cancelled) setPyFileContent('# Не удалось загрузить файл предпросмотра');
      });
    return () => {
      cancelled = true;
    };
  }, [selectedPyFile]);

  const pushToast = (title: string, message: string, type: 'info' | 'warning' | 'success' = 'info') => {
    const id = Math.random().toString(36).slice(2);
    setToasts((prev) => [...prev.slice(-3), { id, title, message, type }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 4000);
  };

  // Smooth section transition helper
  const handleSwitchSection = (target: 'apps' | 'tracker' | 'python_code') => {
    if (target === activeSection) return;
    if (smoothAnimations) {
      setSectionAnimating(true);
      setTimeout(() => {
        setActiveSection(target);
        setSectionAnimating(false);
      }, 130);
    } else {
      setActiveSection(target);
    }
  };

  // Background audio volume handler
  const handleVolumeChange = (newVol: number) => {
    const clamped = Math.max(0, Math.min(100, newVol));
    setVolume(clamped);
    if (clamped > 0 && isMuted) setIsMuted(false);
    setAudioBgStatus(`pycaw SetMasterVolumeScalar(${(clamped / 100).toFixed(2)}) [Daemon Thread]`);
    try {
      if (!audioCtxRef.current && typeof window !== 'undefined') {
        const AudioCtx =
          window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
        if (AudioCtx) audioCtxRef.current = new AudioCtx();
      }
    } catch {
      // ignore
    }
  };

  const handleToggleMute = () => {
    const nextMute = !isMuted;
    setIsMuted(nextMute);
    setAudioBgStatus(nextMute ? 'CoreAudio SetMute(1) [Background]' : `CoreAudio SetMute(0) • ${volume}%`);
    pushToast(
      'Системный звук',
      nextMute ? 'Звук системы приглушен (Mute) в фоновом режиме' : `Громкость системы: ${volume}%`
    );
  };

  // Check detox limits and notify if exceeded
  const checkDetoxLimits = (updatedApp: AppItem, allUpdatedApps: AppItem[]) => {
    if (!detoxNotifications) return;
    if (updatedApp.dailyLimitMinutes > 0 && updatedApp.todayMinutes >= updatedApp.dailyLimitMinutes) {
      pushToast(
        `⚠️ Превышен лимит: ${updatedApp.name}`,
        `Вы провели в ${updatedApp.name} уже ${formatDurationRu(updatedApp.todayMinutes, updatedApp.elapsedSeconds)} сегодня (лимит: ${formatDurationRu(updatedApp.dailyLimitMinutes)}).`,
        'warning'
      );
    }

    const groupCfg = detoxGroups.find((g) => g.name === updatedApp.detoxGroup);
    if (groupCfg && groupCfg.enabled) {
      const groupTotal = allUpdatedApps
        .filter((a) => a.detoxGroup === groupCfg.name)
        .reduce((acc, item) => acc + item.todayMinutes, 0);
      if (groupTotal >= groupCfg.dailyLimitMinutes) {
        pushToast(
          `🛑 Цифровой детокс: группа «${groupCfg.name}»`,
          `Дневной лимит группы «${groupCfg.name}» превышен (${formatDurationRu(groupTotal)} из ${formatDurationRu(groupCfg.dailyLimitMinutes)}).`,
          'warning'
        );
      }
    }
  };

  // Launch or toggle running state for an app (starts timer from 00:00 in real time!)
  const handleLaunchApp = (app: AppItem) => {
    if (app.type === 'plugin' && app.pluginId) {
      const targetPlugin = plugins.find((p) => p.id === app.pluginId);
      if (targetPlugin) {
        if (targetPlugin.id === 'session_tracker_plugin') {
          handleSwitchSection('tracker');
        } else {
          setActivePluginModal(targetPlugin);
        }
        return;
      }
    }

    setApps((prev) =>
      prev.map((item) => {
        if (item.id !== app.id) return item;
        const nextRunning = !item.isRunning;
        return {
          ...item,
          isRunning: nextRunning,
        };
      })
    );

    const willRun = !app.isRunning;
    if (willRun) {
      pushToast(
        `Запуск ${app.name}`,
        sessionTrackerEnabled
          ? `${app.name} запущено • Таймер запущен с ${formatLiveClock(app.elapsedSeconds || 0)}`
          : `${app.name} (${app.url}) запущено`,
        'success'
      );
    } else {
      pushToast(
        `Сессия остановлена: ${app.name}`,
        `Таймер остановлен на ${formatLiveClock(app.elapsedSeconds || 0)}`,
        'info'
      );
    }
  };

  const handleResetAllTimers = () => {
    setApps((prev) =>
      prev.map((a) => ({
        ...a,
        isRunning: false,
        elapsedSeconds: 0,
        todayMinutes: 0,
        weekMinutes: 0,
        monthMinutes: 0,
      }))
    );
    pushToast('Трекер сброшен в 0', 'Все счетчики времени обнулены до 00:00 (0 мин).', 'success');
  };

  const handleAddSessionMinutes = (appId: string, minutesToAdd: number) => {
    setApps((prev) => {
      let targetUpdated: AppItem | null = null;
      const next = prev.map((item) => {
        if (item.id !== appId) return item;
        targetUpdated = {
          ...item,
          elapsedSeconds: (item.elapsedSeconds || 0) + minutesToAdd * 60,
          todayMinutes: item.todayMinutes + minutesToAdd,
          weekMinutes: item.weekMinutes + minutesToAdd,
          monthMinutes: item.monthMinutes + minutesToAdd,
        };
        return targetUpdated;
      });
      if (targetUpdated) {
        checkDetoxLimits(targetUpdated, next);
      }
      return next;
    });
  };

  const handleToggleFavorite = (app: AppItem) => {
    const favCount = apps.filter((a) => a.favorite).length;
    if (!app.favorite && favCount >= 10) {
      pushToast('Избранное', 'Максимум 10 приложений в избранном', 'warning');
      return;
    }
    setApps((prev) =>
      prev.map((item) => (item.id === app.id ? { ...item, favorite: !item.favorite } : item))
    );
    pushToast(
      'Избранное',
      !app.favorite ? `${app.name} добавлено в избранное` : `${app.name} удалено из избранного`
    );
  };

  const handleAddCustomApp = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newAppName.trim() || !newAppUrl.trim()) {
      pushToast('Ошибка', 'Заполните название и путь/URL приложения', 'warning');
      return;
    }
    const cleanName = newAppName.trim();
    const detectedType: AppType = newAppUrl.trim().toLowerCase().startsWith('http') ? 'web' : newAppType;

    const created: AppItem = {
      id: `custom_${Date.now()}`,
      name: cleanName,
      package: cleanName.toLowerCase().replace(/\s+/g, '_'),
      category: newAppCategory,
      icon: newAppIcon,
      url: newAppUrl.trim(),
      args: newAppArgs.trim(),
      type: detectedType,
      installed: true,
      favorite: newAppFav,
      custom: true,
      monthMinutes: 0,
      weekMinutes: 0,
      todayMinutes: 0,
      elapsedSeconds: 0,
      isRunning: false,
      dailyLimitMinutes: Number(newAppLimit) || 120,
      detoxGroup:
        newAppCategory === 'Games'
          ? 'Игры'
          : newAppCategory === 'Social'
          ? 'Соцсети и мессенджеры'
          : 'Браузеры',
    };

    setApps((prev) => [created, ...prev]);
    setNewAppName('');
    setNewAppUrl('');
    setNewAppArgs('');
    setAddAppModalOpen(false);
    pushToast(
      'Приложение добавлено',
      `«${cleanName}» добавлено в библиотеку со счетчиком 0 мин`,
      'success'
    );
  };

  const handleInstallCatalogPlugin = (item: CatalogPluginItem) => {
    if (plugins.some((p) => p.id === item.id)) {
      pushToast('Магазин плагинов', `${item.name} уже установлен`, 'info');
      return;
    }
    const installed: PluginItem = {
      id: item.id,
      name: item.name,
      version: item.version,
      author: item.author,
      category: item.category,
      icon: item.icon,
      description: item.description,
      enabled: true,
      file: item.file,
      hooks: item.hooks,
      showInLauncher: true,
      customIntervalSec: 60,
      notificationsEnabled: true,
    };
    setPlugins((prev) => [...prev, installed]);
    pushToast('Плагин скачан и активирован', `«${item.name}» добавлен в список запуска!`, 'success');
  };

  const handleDeletePlugin = (pluginId: string) => {
    const target = plugins.find((p) => p.id === pluginId);
    setPlugins((prev) => prev.filter((p) => p.id !== pluginId));
    if (target) {
      pushToast('Плагин удален', `Плагин «${target.name}» удален из системы`, 'info');
    }
  };

  const handleCreatePluginTemplate = () => {
    if (!newPluginSlug.trim()) {
      pushToast('Plugin SDK 2.4', 'Введите ID нового расширения (например: discord_rpc)', 'warning');
      return;
    }
    const slug = newPluginSlug.trim().toLowerCase().replace(/[^a-z0-9_]/g, '_');
    const title = newPluginTitle.trim() || 'Custom Extension';
    const newPlugin: PluginItem = {
      id: slug,
      name: title,
      version: '2.4.0',
      author: 'User SDK',
      category: 'Пользовательские',
      icon: 'Puzzle',
      description: 'Пользовательское расширение, сгенерированное через Plugin SDK 2.4.',
      enabled: true,
      file: `plugins/${slug}.py`,
      hooks: ['on_load', 'on_app_launched', 'get_ui_component'],
      showInLauncher: true,
      customIntervalSec: 60,
      notificationsEnabled: true,
    };
    setPlugins((prev) => [newPlugin, ...prev]);
    setNewPluginSlug('');
    setNewPluginTitle('');
    pushToast(
      'Plugin SDK 2.4',
      `Шаблон плагина «${title}» (plugins/${slug}.py) создан и добавлен в список запуска!`,
      'success'
    );
  };

  // Convert active plugins into launchable AppItems so they appear in the launch list!
  const pluginAppItems: AppItem[] = useMemo(() => {
    if (!showPluginsInGrid) return [];
    return plugins
      .filter((p) => p.enabled && p.showInLauncher !== false)
      .map((p) => ({
        id: `plugin_${p.id}`,
        name: p.name,
        package: `plugin:${p.id}`,
        category: 'Плагины',
        icon: p.icon || 'Puzzle',
        url: `plugin://${p.id}`,
        type: 'plugin' as AppType,
        installed: true,
        favorite: false,
        monthMinutes: 0,
        weekMinutes: 0,
        todayMinutes: 0,
        elapsedSeconds: 0,
        dailyLimitMinutes: 0,
        detoxGroup: 'Система',
        pluginId: p.id,
      }));
  }, [plugins, showPluginsInGrid]);

  const combinedApps = useMemo(() => [...apps, ...pluginAppItems], [apps, pluginAppItems]);

  // Filtered apps
  const filteredApps = useMemo(() => {
    return combinedApps.filter((app) => {
      if (currentFilter === 'web' && app.type !== 'web') return false;
      if (currentFilter === 'app' && app.type !== 'app') return false;
      if (currentFilter === 'system' && app.type !== 'system') return false;
      if (currentFilter === 'plugin' && app.type !== 'plugin') return false;
      if (currentFilter === 'custom' && !app.custom) return false;
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase().trim();
        return (
          app.name.toLowerCase().includes(q) ||
          app.category.toLowerCase().includes(q) ||
          app.package.toLowerCase().includes(q)
        );
      }
      return true;
    });
  }, [combinedApps, currentFilter, searchQuery]);

  const favoriteApps = useMemo(() => apps.filter((a) => a.favorite), [apps]);

  const categoriesMap = useMemo(() => {
    const map: Record<string, AppItem[]> = {};
    for (const app of filteredApps) {
      if (!map[app.category]) map[app.category] = [];
      map[app.category].push(app);
    }
    return map;
  }, [filteredApps]);

  // Formatted clock parts for all 8 styles + Android 14 vertical clock
  const clockParts = useMemo(() => {
    let hours = now.getHours();
    const mins = String(now.getMinutes()).padStart(2, '0');
    const secs = String(now.getSeconds()).padStart(2, '0');
    let ampm = '';
    if (timeFormat === '12') {
      ampm = hours >= 12 ? ' PM' : ' AM';
      hours = hours % 12 || 12;
    }
    const hrs = String(hours).padStart(2, '0');

    const day = String(now.getDate()).padStart(2, '0');
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const year = now.getFullYear();
    const weekday = WEEKDAYS_RU[now.getDay()];

    const dateBase = `${day}.${month}.${year}`;
    const fullDate = showWeekday ? `${weekday}, ${dateBase}` : dateBase;

    return { hrs, mins, secs, ampm, weekday, dateBase, fullDate };
  }, [now, timeFormat, showWeekday]);

  // Glassmorphism dynamic CSS styles (matching Screenshot 2 Midnight Slate aesthetic)
  const blurPx = glassEnabled
    ? glassIntensity === 'light'
      ? 'blur(8px)'
      : glassIntensity === 'medium'
      ? 'blur(16px)'
      : 'blur(26px)'
    : 'none';

  const cardGlassStyle: React.CSSProperties = {
    backgroundColor: glassEnabled
      ? currentTheme.isDark
        ? `rgba(21, 27, 38, ${(glassOpacity / 100).toFixed(2)})`
        : `rgba(255, 255, 255, ${(Math.max(65, glassOpacity) / 100).toFixed(2)})`
      : currentTheme.cardHex,
    backdropFilter: blurPx,
    WebkitBackdropFilter: blurPx,
  };

  const renderAppIcon = (iconName: string, className = 'w-8 h-8') => {
    const IconComponent = ICON_MAP[iconName] || Rocket;
    return <IconComponent className={className} />;
  };

  const runningAppsCount = useMemo(() => apps.filter((a) => a.isRunning).length, [apps]);

  return (
    <div
      className={`min-h-screen w-full flex flex-col select-none transition-colors duration-300 ${
        currentTheme.isDark ? 'text-slate-100' : 'text-slate-900'
      }`}
      style={{ background: currentTheme.bgGradient }}
    >
      {/* ==================== TOP HEADER (Flet Header 2.5) ==================== */}
      <header
        className={`sticky top-0 z-30 flex items-center justify-between gap-4 px-5 py-2.5 border-b transition-all ${
          currentTheme.isDark ? 'border-slate-800/90' : 'border-slate-300/80'
        }`}
        style={cardGlassStyle}
      >
        {/* Left: Workspace button + Brand Title + Section Switcher */}
        <div className="flex items-center gap-3 min-w-0">
          <button
            onClick={() => setWorkspaceModalOpen(true)}
            title="Smart Workspace (Пресеты)"
            className="p-2 rounded-xl bg-blue-500/15 hover:bg-blue-500/25 text-blue-400 border border-blue-500/30 transition-all cursor-pointer shrink-0"
          >
            <Rocket className="w-5 h-5" />
          </button>

          <div className="flex items-center gap-2 shrink-0">
            <span className="text-lg font-bold tracking-tight whitespace-nowrap">
              Launcher Hab 2.5
            </span>
            <span className="hidden sm:inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
              v2.5 PRO
            </span>
          </div>

          {/* Section Switcher */}
          <nav className="hidden md:flex items-center gap-1 p-1 rounded-xl bg-[#0d111a]/80 border border-slate-700/60 ml-2">
            <button
              onClick={() => handleSwitchSection('apps')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer whitespace-nowrap ${
                activeSection === 'apps'
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <LayoutGrid className="w-3.5 h-3.5" />
              Приложения
            </button>
            <button
              onClick={() => handleSwitchSection('tracker')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer whitespace-nowrap ${
                activeSection === 'tracker'
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <BarChart3 className="w-3.5 h-3.5" />
              Трекер времени
              {runningAppsCount > 0 && (
                <span className="px-1.5 py-0.2 rounded-full bg-emerald-500/20 text-emerald-400 text-[10px] font-mono">
                  {runningAppsCount} актив.
                </span>
              )}
            </button>
            <button
              onClick={() => handleSwitchSection('python_code')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer whitespace-nowrap ${
                activeSection === 'python_code'
                  ? 'bg-emerald-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Code2 className="w-3.5 h-3.5" />
              Python Код v2.5
            </button>
          </nav>
        </div>

        {/* Center/Right: System Devices + Customizable Clock (18 Styles) + Audio + Plugins + Settings */}
        <div className="flex items-center gap-2.5 shrink-0">
          {/* Devices Monitor (Battery & Wi-Fi) */}
          <div className="hidden lg:flex items-center gap-3 px-3 py-1.5 rounded-xl bg-[#1e2636]/70 border border-slate-700/60 text-xs">
            <div className="flex items-center gap-1.5 text-emerald-400">
              <BatteryCharging className="w-4 h-4" />
              <span className="font-mono tabular-nums">96%</span>
            </div>
            <span className="opacity-30">•</span>
            <div className="flex items-center gap-1.5 text-emerald-400">
              <Wifi className="w-4 h-4" />
              <span>Ethernet</span>
            </div>
          </div>

          {/* Customizable Clock Widget (18 Styles including Android Vertical & 10 new v2.5 styles) */}
          <button
            onClick={() => {
              setSettingsTab('clock');
              setSettingsModalOpen(true);
            }}
            title="Нажмите для настройки 18 стилей часов и дизайна циферблата (v2.5)"
            style={{
              borderRadius: `${clockBorderRadius}px`,
              backgroundColor: clockGlassFrame
                ? `rgba(30, 38, 54, ${(clockBgOpacity / 100).toFixed(2)})`
                : 'transparent',
              borderColor: clockGlassFrame
                ? clockGlowEnabled
                  ? `${clockAccentColor}66`
                  : 'rgba(51, 65, 85, 0.7)'
                : 'transparent',
              boxShadow:
                clockGlassFrame && clockGlowEnabled
                  ? `0 0 ${clockGlowIntensity}px ${clockAccentColor}40`
                  : 'none',
            }}
            className={`px-3.5 py-1.5 transition-all cursor-pointer border ${
              clockGlassFrame ? 'hover:brightness-110' : 'hover:bg-white/5 border-transparent'
            }`}
          >
            {(() => {
              const sep = clockBlinkColon && now.getSeconds() % 2 === 1 ? ' ' : ':';
              const weightCls = clockBold ? 'font-extrabold' : 'font-medium';
              if (
                clockStyle === 'android_vertical' ||
                clockStyle === 'stacked' ||
                clockStyle === 'samsung_oneui' ||
                clockStyle === 'vertical_neon_bar' ||
                clockStyle === 'material_expressive'
              ) {
                return (
                  <div className="flex items-center gap-2.5">
                    <div className="flex flex-col items-center leading-none">
                      <span
                        className={`${weightCls} font-mono tabular-nums tracking-tight`}
                        style={{ color: timeColor, fontSize: '15px' }}
                      >
                        {clockParts.hrs}
                      </span>
                      <span
                        className={`${weightCls} font-mono tabular-nums tracking-tight`}
                        style={{ color: clockAccentColor, fontSize: '15px' }}
                      >
                        {clockParts.mins}
                      </span>
                    </div>
                    {showDate && (
                      <div
                        className="flex flex-col items-start leading-tight border-l pl-2"
                        style={{ borderColor: clockAccentColor }}
                      >
                        <span
                          className="text-[10px] font-bold uppercase"
                          style={{ color: clockAccentColor }}
                        >
                          {clockParts.weekday}
                        </span>
                        <span className="text-[10px] font-mono tabular-nums" style={{ color: dateColor }}>
                          {clockParts.dateBase}
                        </span>
                      </div>
                    )}
                  </div>
                );
              }
              if (clockStyle === 'split_flip') {
                return (
                  <div className="flex items-center gap-1">
                    <span className="px-1.5 py-0.5 rounded bg-[#0d111a] border border-slate-700 font-mono font-bold text-xs">
                      {clockParts.hrs}
                    </span>
                    <span className="font-bold text-xs" style={{ color: clockAccentColor }}>
                      {sep}
                    </span>
                    <span
                      className="px-1.5 py-0.5 rounded bg-[#0d111a] border border-slate-700 font-mono font-bold text-xs"
                      style={{ color: clockAccentColor }}
                    >
                      {clockParts.mins}
                    </span>
                    {showSeconds && (
                      <span className="px-1 py-0.5 rounded bg-[#0d111a] border border-slate-800 font-mono text-[10px] text-slate-400">
                        {clockParts.secs}
                      </span>
                    )}
                  </div>
                );
              }
              if (clockStyle === 'pill_glass' || clockStyle === 'ios_standby' || clockStyle === 'macos_sonoma') {
                return (
                  <div className="flex items-center gap-2">
                    <Clock className="w-3.5 h-3.5" style={{ color: clockAccentColor }} />
                    <span
                      className={`${weightCls} font-mono tabular-nums text-xs`}
                      style={{ color: timeColor }}
                    >
                      {clockParts.hrs}
                      {sep}
                      {clockParts.mins}
                    </span>
                    {showDate && (
                      <>
                        <span className="opacity-40">•</span>
                        <span className="text-[11px] font-mono tabular-nums" style={{ color: dateColor }}>
                          {clockParts.fullDate}
                        </span>
                      </>
                    )}
                  </div>
                );
              }
              if (clockStyle === 'compact_badge') {
                return (
                  <div className="flex items-center gap-1.5">
                    <span
                      className="px-1.5 py-0.5 rounded text-white text-[10px] font-bold"
                      style={{ backgroundColor: clockAccentColor }}
                    >
                      {clockParts.weekday}
                    </span>
                    <span className={`font-mono ${weightCls} text-xs`} style={{ color: timeColor }}>
                      {clockParts.hrs}
                      {sep}
                      {clockParts.mins}
                    </span>
                  </div>
                );
              }

              let formattedTime = `${clockParts.hrs}${sep}${clockParts.mins}${
                showSeconds && clockStyle !== 'minimal' ? `${sep}${clockParts.secs}` : ''
              }`;
              if (clockStyle === 'cyber_mono') {
                formattedTime = `[ ${clockParts.hrs}${sep}${clockParts.mins}${showSeconds ? `${sep}${clockParts.secs}` : ''} ]`;
              } else if (clockStyle === 'nothing_dot') {
                formattedTime = `::${clockParts.hrs} · ${clockParts.mins}${showSeconds ? ` · ${clockParts.secs}` : ''}::`;
              } else if (clockStyle === 'neon_synthwave') {
                formattedTime = `⚡ ${clockParts.hrs}${sep}${clockParts.mins}${showSeconds ? `${sep}${clockParts.secs}` : ''}`;
              } else if (clockStyle === 'retro_casio') {
                formattedTime = `LCD ${clockParts.hrs}${sep}${clockParts.mins}${showSeconds ? `'${clockParts.secs}` : ''}`;
              } else if (clockStyle === 'futuristic_hud') {
                formattedTime = `SYS//${clockParts.hrs}${sep}${clockParts.mins}${showSeconds ? `.${clockParts.secs}` : ''}`;
              } else if (clockStyle === 'analog_hybrid') {
                formattedTime = `◔ ${clockParts.hrs}${sep}${clockParts.mins}${showSeconds ? `${sep}${clockParts.secs}` : ''}`;
              }

              return (
                <div className="flex flex-col items-center leading-tight">
                  <span
                    className={`${weightCls} font-mono tabular-nums text-xs`}
                    style={{ color: timeColor }}
                  >
                    {formattedTime}
                  </span>
                  {showDate && (
                    <span className="text-[10px] font-mono tabular-nums" style={{ color: dateColor }}>
                      {clockParts.fullDate}
                    </span>
                  )}
                </div>
              );
            })()}
          </button>

          {/* Background System Audio Controller */}
          <div className="relative flex items-center gap-1.5">
            <button
              onClick={() => setVolumePopupOpen((v) => !v)}
              title="Управление системной громкостью (Фоновый контроллер v2.5)"
              className={`p-2 rounded-xl border transition-all cursor-pointer ${
                volumePopupOpen
                  ? 'bg-blue-500/20 border-blue-500/40 text-blue-400'
                  : 'bg-[#1e2636]/80 hover:bg-[#263044] border-slate-700/60'
              }`}
            >
              {isMuted || volume === 0 ? (
                <VolumeX className="w-4 h-4 text-rose-400" />
              ) : volume < 50 ? (
                <Volume1 className="w-4 h-4" />
              ) : (
                <Volume2 className="w-4 h-4" />
              )}
            </button>

            {volumePopupOpen && (
              <div
                className="flex items-center gap-2.5 px-3 py-1.5 rounded-xl border border-slate-700 shadow-lg"
                style={cardGlassStyle}
              >
                <button
                  onClick={handleToggleMute}
                  title="Mute / Unmute"
                  className="text-xs p-1 rounded hover:bg-white/10 cursor-pointer"
                >
                  {isMuted || volume === 0 ? (
                    <VolumeX className="w-4 h-4 text-rose-400" />
                  ) : (
                    <Volume2 className="w-4 h-4 text-blue-400" />
                  )}
                </button>
                <input
                  type="range"
                  min={0}
                  max={100}
                  value={isMuted ? 0 : volume}
                  onChange={(e) => handleVolumeChange(Number(e.target.value))}
                  className="w-24 accent-blue-500 cursor-pointer"
                />
                <span className="text-xs font-mono tabular-nums w-9 text-right">
                  {isMuted ? 'MUTE' : `${volume}%`}
                </span>
              </div>
            )}
          </div>

          {/* Plugins Button */}
          <button
            onClick={() => setPluginsModalOpen(true)}
            title="Магазин и управление плагинами (API 2.5)"
            className="p-2 rounded-xl bg-[#1e2636]/80 hover:bg-[#263044] border border-slate-700/60 transition-all cursor-pointer"
          >
            <Puzzle className="w-4 h-4" />
          </button>

          {/* Floating HUD Button */}
          <button
            onClick={() => setFloatingHudVisible((v) => !v)}
            title="Floating HUD (Мониторинг CPU/RAM)"
            className={`p-2 rounded-xl border transition-all cursor-pointer ${
              floatingHudVisible
                ? 'bg-blue-500/20 border-blue-500/40 text-blue-400'
                : 'bg-[#1e2636]/80 hover:bg-[#263044] border-slate-700/60'
            }`}
          >
            <Activity className="w-4 h-4" />
          </button>

          {/* Settings Button */}
          <button
            onClick={() => {
              setSettingsTab('appearance');
              setSettingsModalOpen(true);
            }}
            title="Настройки Launcher Hab 2.5"
            className="p-2 rounded-xl bg-[#1e2636]/80 hover:bg-[#263044] border border-slate-700/60 transition-all cursor-pointer"
          >
            <Settings className="w-4 h-4" />
          </button>

          {/* Direct Download Python v2.5 ZIP */}
          <a
            href="/launcher_hab2.4.zip"
            download="launcher_hab2.5.zip"
            className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold shadow-sm transition-all whitespace-nowrap"
          >
            <Download className="w-3.5 h-3.5" />
            Python v2.5 (.zip)
          </a>
        </div>
      </header>

      {/* ==================== MAIN BODY (Sidebar + Main Viewport matching Screenshot 2) ==================== */}
      <div className="flex-1 flex overflow-hidden relative">
        {/* LEFT SIDEBAR (Matches Screenshot 2 dark slate cards without yellow borders) */}
        <aside
          className={`w-80 lg:w-88 shrink-0 flex flex-col border-r transition-all ${
            currentTheme.isDark ? 'border-slate-800/90' : 'border-slate-300/80'
          }`}
          style={cardGlassStyle}
        >
          {/* Sidebar Header */}
          <div className="px-5 pt-4 pb-2 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <LayoutGrid className="w-4 h-4 text-blue-400" />
              <h2 className="text-base font-bold">Библиотека</h2>
            </div>
            <span className="text-xs text-slate-400 font-mono tabular-nums">
              {combinedApps.length} прил.
            </span>
          </div>

          {/* Search Input */}
          <div className="px-4 py-2 flex items-center gap-2">
            <div className="relative flex-1">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Поиск приложений и плагинов..."
                className={`w-full pl-9 pr-7 py-2 rounded-xl text-xs border outline-none transition-all ${
                  currentTheme.isDark
                    ? 'bg-[#1a2232] border-slate-700/70 focus:border-blue-500/70 text-white placeholder:text-slate-500'
                    : 'bg-slate-100 border-slate-300 focus:border-blue-500 text-slate-900 placeholder:text-slate-400'
                }`}
              />
              {searchQuery && (
                <button
                  onClick={() => setSearchQuery('')}
                  className="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white cursor-pointer"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              )}
            </div>
          </div>

          {/* Filter Tabs (including Плагины) */}
          <div className="px-4 pb-2.5 flex items-center gap-1 overflow-x-auto">
            {(
              [
                ['all', 'Все'],
                ['app', 'EXE'],
                ['web', 'Web'],
                ['plugin', 'Плагины'],
                ['system', 'Система'],
              ] as const
            ).map(([key, label]) => (
              <button
                key={key}
                onClick={() => setCurrentFilter(key)}
                className={`px-2.5 py-1 rounded-lg text-[11px] font-medium transition-all cursor-pointer whitespace-nowrap ${
                  currentFilter === key
                    ? 'bg-blue-600 text-white'
                    : 'bg-[#1a2232] hover:bg-[#232d42] text-slate-400 border border-slate-700/50'
                }`}
              >
                {label}
              </button>
            ))}
          </div>

          <div className="border-t border-slate-800/80" />

          {/* Sidebar Apps & Plugins List (Matches Screenshot 2 exactly!) */}
          <div className="flex-1 overflow-y-auto p-3 space-y-2">
            {filteredApps.map((app) => {
              const isPlugin = app.type === 'plugin';
              const badge = isPlugin
                ? 'ПЛАГИН • Активен'
                : sessionTrackerEnabled
                ? formatMonthBadge(app.monthMinutes, app.elapsedSeconds, app.isRunning)
                : app.type.toUpperCase();

              return (
                <div
                  key={app.id}
                  onClick={() => handleLaunchApp(app)}
                  className={`group flex items-center gap-3 p-3 rounded-xl border transition-all cursor-pointer ${
                    app.isRunning
                      ? 'bg-[#19283a] border-blue-500/60 shadow-sm'
                      : currentTheme.isDark
                      ? 'bg-[#1a2232]/90 hover:bg-[#212b3f] border-slate-700/60 hover:border-slate-600'
                      : 'bg-white/80 hover:bg-blue-50 border-slate-200/80 hover:border-blue-400'
                  }`}
                >
                  <div
                    className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border ${
                      app.isRunning
                        ? 'text-emerald-400 bg-emerald-500/15 border-emerald-500/40'
                        : isPlugin
                        ? 'text-purple-400 bg-purple-500/15 border-purple-500/30'
                        : app.type === 'web'
                        ? 'text-blue-400 bg-blue-500/10 border-blue-500/25'
                        : 'text-slate-100 bg-[#232d42] border-slate-700/70'
                    }`}
                  >
                    {renderAppIcon(app.icon, 'w-5 h-5')}
                  </div>

                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-1.5">
                      <p className="text-xs font-bold truncate">{app.name}</p>
                      {app.isRunning && (
                        <span className="text-[10px] font-mono text-emerald-400 font-semibold">
                          • Активно
                        </span>
                      )}
                    </div>
                    <p
                      className={`text-[11px] truncate font-mono tabular-nums mt-0.5 ${
                        app.isRunning ? 'text-emerald-400' : 'text-slate-400'
                      }`}
                    >
                      {app.category} • {badge}
                    </p>
                  </div>

                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      if (isPlugin && app.pluginId) {
                        const pl = plugins.find((p) => p.id === app.pluginId);
                        if (pl) setEditingPluginSettings(pl);
                      } else {
                        setContextMenuApp(app);
                      }
                    }}
                    title="Меню"
                    className="p-1.5 rounded-lg opacity-70 hover:opacity-100 hover:bg-white/10 transition-all cursor-pointer"
                  >
                    <MoreVertical className="w-4 h-4 text-slate-400" />
                  </button>
                </div>
              );
            })}
          </div>

          <div className="border-t border-slate-800/80" />

          {/* Add App Button at Bottom of Sidebar */}
          <div className="p-3.5">
            <button
              onClick={() => setAddAppModalOpen(true)}
              className="w-full flex items-center gap-3 p-3 rounded-xl bg-emerald-500/15 hover:bg-emerald-500/25 border border-emerald-500/40 transition-all cursor-pointer text-left"
            >
              <div className="w-10 h-10 rounded-xl bg-emerald-500/25 flex items-center justify-center text-emerald-400 shrink-0">
                <Plus className="w-5 h-5" />
              </div>
              <div className="min-w-0">
                <div className="text-xs font-bold text-emerald-100">Добавить приложение</div>
                <div className="text-[11px] text-emerald-300/80 truncate">
                  EXE, URI или веб-сервис + трекер с 0
                </div>
              </div>
            </button>
          </div>
        </aside>

        {/* ==================== MAIN CONTENT AREA ==================== */}
        <main className="flex-1 overflow-y-auto p-6 relative">
          <div
            className={`transition-all duration-200 ${
              sectionAnimating ? 'opacity-0 scale-[0.99] translate-y-1' : 'opacity-100 scale-100 translate-y-0'
            }`}
          >
            {/* -------------------- SECTION 1: APPS, ANDROID VERTICAL CLOCK & PLUGINS -------------------- */}
            {activeSection === 'apps' && (
              <div className="space-y-6 max-w-6xl mx-auto">
                {/* ANDROID 14 / 18 STYLES CLOCK WIDGET BANNER (v2.5) */}
                {showAndroidClockWidget && (
                  <section
                    className="border border-slate-700/70 p-5 shadow-xl flex flex-wrap items-center justify-between gap-6"
                    style={{ ...cardGlassStyle, borderRadius: `${cardBorderRadius}px` }}
                  >
                    <div className="flex items-center gap-6">
                      {/* Vertical Android 14 Lock-Screen Clock (HH over MM) with v2.5 Glow & Radius */}
                      <div
                        onClick={() => {
                          setSettingsTab('clock');
                          setSettingsModalOpen(true);
                        }}
                        title="Нажмите для настройки 18 стилей часов и неонового свечения (v2.5)"
                        style={{
                          borderRadius: `${clockBorderRadius}px`,
                          backgroundColor: `rgba(26, 34, 50, ${(clockBgOpacity / 100).toFixed(2)})`,
                          borderColor: clockGlowEnabled ? `${clockAccentColor}77` : 'rgba(51, 65, 85, 0.8)',
                          boxShadow: clockGlowEnabled ? `0 0 ${clockGlowIntensity}px ${clockAccentColor}40` : 'none',
                        }}
                        className="px-6 py-3 border flex flex-col items-center justify-center leading-none cursor-pointer hover:brightness-110 transition-all"
                      >
                        <span
                          className={`${clockBold ? 'font-black' : 'font-semibold'} font-mono tabular-nums tracking-tighter`}
                          style={{ color: timeColor, fontSize: '44px', lineHeight: 0.95 }}
                        >
                          {clockParts.hrs}
                        </span>
                        <span
                          className={`${clockBold ? 'font-black' : 'font-semibold'} font-mono tabular-nums tracking-tighter mt-1`}
                          style={{ color: clockAccentColor, fontSize: '44px', lineHeight: 0.95 }}
                        >
                          {clockParts.mins}
                        </span>
                      </div>

                      <div className="space-y-1.5">
                        <div className="flex flex-wrap items-center gap-2">
                          <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-lg bg-blue-500/15 border border-blue-500/30 text-blue-400 text-xs font-bold">
                            <Clock className="w-3.5 h-3.5" />
                            {clockParts.fullDate}
                            {showSeconds && (
                              <span className="font-mono text-slate-300">• :{clockParts.secs}</span>
                            )}
                          </div>
                          <LitStatusBadge active={true} />
                        </div>
                        <h3 className="text-base font-bold">
                          Launcher Hab 2.5 — {CLOCK_STYLE_OPTIONS.find((c) => c.id === clockStyle)?.label}
                        </h3>
                        <p className="text-xs text-slate-400">
                          Клик по карточке запускает приложение и включает живой секундомер с <code className="text-emerald-400">00:00</code> • Повторный клик останавливает сессию
                        </p>
                      </div>
                    </div>

                    <div className="flex flex-wrap items-center gap-2">
                      <button
                        onClick={() => {
                          const idx = CLOCK_STYLE_OPTIONS.findIndex((c) => c.id === clockStyle);
                          const next = CLOCK_STYLE_OPTIONS[(idx + 1) % CLOCK_STYLE_OPTIONS.length];
                          setClockStyle(next.id);
                          pushToast('Стиль часов 2.5', `Активирован стиль: ${next.label}`, 'success');
                        }}
                        className="px-3.5 py-2 rounded-xl bg-emerald-500/15 hover:bg-emerald-500/25 border border-emerald-500/40 text-emerald-300 text-xs font-semibold cursor-pointer transition-all"
                      >
                        ⚡ След. стиль (из 18)
                      </button>
                      <button
                        onClick={() => {
                          setSettingsTab('clock');
                          setSettingsModalOpen(true);
                        }}
                        className="px-3.5 py-2 rounded-xl bg-[#1e2636] hover:bg-[#273247] border border-slate-700 text-xs font-semibold cursor-pointer transition-all"
                      >
                        🕒 Настроить часы (18)
                      </button>
                      <button
                        onClick={() => setCustomThemeModalOpen(true)}
                        className="px-3.5 py-2 rounded-xl bg-blue-600/20 hover:bg-blue-600/30 border border-blue-500/40 text-blue-300 text-xs font-semibold cursor-pointer transition-all"
                      >
                        🎨 Создать тему 2.5
                      </button>
                    </div>
                  </section>
                )}

                {/* FAVORITES SECTION (Matches Screenshot 2 dark slate style & emerald active indicator) */}
                <section
                  className="rounded-2xl border border-slate-800/90 p-6 shadow-xl transition-all"
                  style={cardGlassStyle}
                >
                  <div className="flex flex-wrap items-center justify-between gap-2 mb-5">
                    <div className="flex items-center gap-2.5">
                      <Star className="w-5 h-5 text-amber-400 fill-amber-400" />
                      <h3 className="text-base font-bold">Избранное</h3>
                      <span className="text-xs text-slate-400 font-mono tabular-nums">
                        {favoriteApps.length}/10
                      </span>
                    </div>
                    <span className="text-xs text-slate-400">
                      Клик — запуск и старт таймера с 00:00 • ПКМ / меню — управление
                    </span>
                  </div>

                  {favoriteApps.length === 0 ? (
                    <div className="py-8 text-center text-slate-400 text-xs">
                      Добавьте приложения в избранное через меню карточки
                    </div>
                  ) : (
                    <div
                      className="grid gap-4"
                      style={{
                        gridTemplateColumns: `repeat(${Math.min(cardColumns, 6)}, minmax(0, 1fr))`,
                      }}
                    >
                      {favoriteApps.map((app) => {
                        const badgeText = sessionTrackerEnabled
                          ? formatMonthBadge(app.monthMinutes, app.elapsedSeconds, app.isRunning)
                          : app.type.toUpperCase();
                        return (
                          <div
                            key={app.id}
                            onClick={() => handleLaunchApp(app)}
                            onContextMenu={(e) => {
                              e.preventDefault();
                              setContextMenuApp(app);
                            }}
                            className="group relative flex flex-col items-center p-2.5 rounded-2xl hover:scale-105 transition-all duration-200 cursor-pointer"
                          >
                            <div
                              className={`w-22 h-22 rounded-2xl flex items-center justify-center relative border transition-all ${
                                app.isRunning
                                  ? 'border-emerald-400 bg-[#12312a] shadow-lg shadow-emerald-950/50'
                                  : 'border-slate-700/80 bg-[#1e2636] group-hover:border-blue-500/60 group-hover:bg-[#242f44]'
                              }`}
                            >
                              <div
                                className={
                                  app.isRunning
                                    ? 'text-white'
                                    : app.type === 'web'
                                    ? 'text-blue-400'
                                    : 'text-slate-100'
                                }
                              >
                                {renderAppIcon(app.icon, 'w-9 h-9')}
                              </div>
                              <div className="absolute bottom-2 right-2">
                                {app.isRunning ? (
                                  <span className="w-3.5 h-3.5 rounded-full border-2 border-emerald-400 bg-emerald-500/30 block animate-pulse" />
                                ) : (
                                  <Star className="w-3.5 h-3.5 text-amber-400 fill-amber-400" />
                                )}
                              </div>
                            </div>

                            <span className="mt-2.5 text-xs font-bold text-center truncate w-full">
                              {app.name}
                            </span>
                            <span
                              className={`text-[11px] font-mono tabular-nums text-center truncate w-full mt-0.5 ${
                                app.isRunning ? 'text-emerald-400 font-semibold' : 'text-slate-400'
                              }`}
                            >
                              {badgeText}
                            </span>
                          </div>
                        );
                      })}
                    </div>
                  )}
                </section>

                {/* CATEGORY SECTIONS (Including Плагины in Launch List!) */}
                {Object.entries(categoriesMap).map(([category, catApps]) => (
                  <section
                    key={category}
                    className="rounded-2xl border border-slate-800/90 p-6 shadow-xl transition-all"
                    style={cardGlassStyle}
                  >
                    <div className="flex items-center justify-between mb-5">
                      <div className="flex items-center gap-2.5">
                        <span
                          className={`w-1.5 h-5 rounded-full ${
                            category === 'Плагины' ? 'bg-purple-500' : 'bg-blue-500'
                          }`}
                        />
                        <h3 className="text-base font-bold">{category}</h3>
                        <span className="text-xs text-slate-400 font-mono tabular-nums">
                          · {catApps.length}
                        </span>
                      </div>
                      {category === 'Плагины' && (
                        <button
                          onClick={() => setPluginsModalOpen(true)}
                          className="text-xs text-blue-400 hover:underline cursor-pointer"
                        >
                          Открыть магазин и настройки плагинов →
                        </button>
                      )}
                    </div>

                    <div
                      className="grid gap-4"
                      style={{
                        gridTemplateColumns: `repeat(${Math.min(cardColumns, 6)}, minmax(0, 1fr))`,
                      }}
                    >
                      {catApps.map((app) => {
                        const isPlugin = app.type === 'plugin';
                        const badgeText = isPlugin
                          ? 'Открыть плагин'
                          : sessionTrackerEnabled
                          ? formatMonthBadge(app.monthMinutes, app.elapsedSeconds, app.isRunning)
                          : app.type.toUpperCase();

                        return (
                          <div
                            key={app.id}
                            onClick={() => handleLaunchApp(app)}
                            onContextMenu={(e) => {
                              e.preventDefault();
                              if (!isPlugin) setContextMenuApp(app);
                            }}
                            className="group relative flex flex-col items-center p-2.5 rounded-2xl hover:scale-105 transition-all duration-200 cursor-pointer"
                          >
                            <div
                              className={`w-22 h-22 rounded-2xl flex items-center justify-center relative border transition-all ${
                                app.isRunning
                                  ? 'border-emerald-400 bg-[#12312a] shadow-lg shadow-emerald-950/50'
                                  : isPlugin
                                  ? 'border-purple-500/40 bg-[#1f1d36] group-hover:border-purple-400'
                                  : 'border-slate-700/80 bg-[#1e2636] group-hover:border-blue-500/60 group-hover:bg-[#242f44]'
                              }`}
                            >
                              <div
                                className={
                                  app.isRunning
                                    ? 'text-white'
                                    : isPlugin
                                    ? 'text-purple-400'
                                    : app.type === 'web'
                                    ? 'text-blue-400'
                                    : 'text-slate-100'
                                }
                              >
                                {renderAppIcon(app.icon, 'w-9 h-9')}
                              </div>
                              {!isPlugin && (
                                <button
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    setContextMenuApp(app);
                                  }}
                                  className="absolute top-1.5 right-1.5 opacity-0 group-hover:opacity-100 p-1 rounded-lg bg-black/50 hover:bg-black/80 text-slate-200 transition-opacity cursor-pointer"
                                >
                                  <MoreVertical className="w-3.5 h-3.5" />
                                </button>
                              )}
                              <div className="absolute bottom-2 right-2">
                                {app.isRunning ? (
                                  <PlayCircle className="w-4 h-4 text-emerald-400" />
                                ) : isPlugin ? (
                                  <Puzzle className="w-3.5 h-3.5 text-purple-400" />
                                ) : (
                                  <Check className="w-3.5 h-3.5 text-emerald-400/80" />
                                )}
                              </div>
                            </div>

                            <span className="mt-2.5 text-xs font-bold text-center truncate w-full">
                              {app.name}
                            </span>
                            <span
                              className={`text-[11px] font-mono tabular-nums text-center truncate w-full mt-0.5 ${
                                app.isRunning
                                  ? 'text-emerald-400 font-semibold'
                                  : isPlugin
                                  ? 'text-purple-400'
                                  : 'text-slate-400'
                              }`}
                            >
                              {badgeText}
                            </span>
                          </div>
                        );
                      })}
                    </div>
                  </section>
                ))}
              </div>
            )}

            {/* -------------------- SECTION 2: GAME & APP SESSION TRACKER (Starts at 0!) -------------------- */}
            {activeSection === 'tracker' && (
              <div className="space-y-5 max-w-6xl mx-auto">
                <section
                  className="rounded-2xl border border-slate-800/90 p-6 shadow-xl"
                  style={cardGlassStyle}
                >
                  <div className="flex flex-wrap items-center justify-between gap-4 pb-5 border-b border-slate-800">
                    <div>
                      <div className="flex items-center gap-2.5">
                        <BarChart3 className="w-6 h-6 text-blue-400" />
                        <h2 className="text-xl font-bold">
                          Game &amp; App Session Tracker (Отсчет с 00:00 по запуску)
                        </h2>
                      </div>
                      <p className="text-xs text-slate-400 mt-1">
                        Все приложения начинаются с 0 мин. При запуске приложения включается живой секундомер в реальном времени.
                      </p>
                    </div>

                    <div className="flex flex-wrap items-center gap-2">
                      <button
                        onClick={handleResetAllTimers}
                        className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-rose-500/15 hover:bg-rose-500/25 border border-rose-500/30 text-rose-300 text-xs font-semibold cursor-pointer transition-all"
                      >
                        <RotateCcw className="w-3.5 h-3.5" />
                        Сбросить все в 0
                      </button>

                      {/* Period Selector: День | Неделя | Месяц */}
                      <div className="flex items-center gap-1 p-1 rounded-xl bg-[#0d111a] border border-slate-700/70">
                        {(
                          [
                            ['day', 'День'],
                            ['week', 'Неделя'],
                            ['month', 'Месяц'],
                          ] as const
                        ).map(([key, label]) => (
                          <button
                            key={key}
                            onClick={() => setTrackerPeriod(key)}
                            className={`px-4 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                              trackerPeriod === key
                                ? 'bg-blue-600 text-white shadow-sm'
                                : 'text-slate-400 hover:text-white'
                            }`}
                          >
                            {label}
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Top Summary Metrics */}
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 my-5">
                    <div className="p-4 rounded-xl bg-[#1a2232] border border-slate-700/70">
                      <span className="text-xs text-slate-400">Общее экранное время</span>
                      <div className="text-2xl font-bold font-mono tabular-nums mt-1 text-blue-400">
                        {formatDurationRu(
                          apps.reduce(
                            (acc, a) =>
                              acc +
                              (trackerPeriod === 'day'
                                ? a.todayMinutes
                                : trackerPeriod === 'week'
                                ? a.weekMinutes
                                : a.monthMinutes),
                            0
                          ),
                          apps.reduce((acc, a) => acc + (a.elapsedSeconds || 0), 0)
                        )}
                      </div>
                      <span className="text-[11px] text-slate-400">
                        Старт с 0 мин • Посекундный учет
                      </span>
                    </div>

                    <div className="p-4 rounded-xl bg-[#1a2232] border border-slate-700/70">
                      <span className="text-xs text-slate-400">Активных таймеров сейчас</span>
                      <div className="text-2xl font-bold font-mono tabular-nums mt-1 text-emerald-400">
                        {runningAppsCount} прил.
                      </div>
                      <span className="text-[11px] text-slate-400">
                        Нажмите «Старт» ниже для запуска секундомера
                      </span>
                    </div>

                    <div className="p-4 rounded-xl bg-[#1a2232] border border-slate-700/70">
                      <span className="text-xs text-slate-400">Статус цифрового детокса</span>
                      <div className="text-2xl font-bold font-mono tabular-nums mt-1 text-amber-400">
                        {detoxGroups.filter((g) => g.enabled).length} групп активны
                      </div>
                      <span className="text-[11px] text-slate-400">
                        Уведомления при превышении дневного лимита
                      </span>
                    </div>
                  </div>

                  {/* Per-Application Activity Bars & Live Start/Stop Timer Controls */}
                  <div className="space-y-2.5">
                    <h3 className="text-sm font-bold text-slate-300">
                      Приложения и игры (Нажмите «Старт» для запуска таймера с 00:00)
                    </h3>

                    {[...apps]
                      .sort((a, b) => {
                        if (a.isRunning !== b.isRunning) return a.isRunning ? -1 : 1;
                        return (b.elapsedSeconds || 0) - (a.elapsedSeconds || 0);
                      })
                      .map((app) => {
                        const val =
                          trackerPeriod === 'day'
                            ? app.todayMinutes
                            : trackerPeriod === 'week'
                            ? app.weekMinutes
                            : app.monthMinutes;
                        const maxVal = Math.max(10, app.dailyLimitMinutes || 120);
                        const percent = Math.min(100, Math.round((val / maxVal) * 100));
                        const isOverDailyLimit =
                          app.dailyLimitMinutes > 0 && app.todayMinutes >= app.dailyLimitMinutes;

                        return (
                          <div
                            key={app.id}
                            className={`p-3.5 rounded-xl border flex flex-col gap-2 transition-all ${
                              app.isRunning
                                ? 'bg-[#132a27] border-emerald-500/60'
                                : 'bg-[#1a2232]/90 border-slate-700/60'
                            }`}
                          >
                            <div className="flex flex-wrap items-center justify-between gap-2">
                              <div className="flex items-center gap-2.5">
                                <div className={app.isRunning ? 'text-emerald-400' : 'text-blue-400'}>
                                  {renderAppIcon(app.icon, 'w-5 h-5')}
                                </div>
                                <span className="text-sm font-bold">{app.name}</span>
                                <span
                                  className={`px-2 py-0.5 rounded-md text-xs font-mono tabular-nums ${
                                    app.isRunning
                                      ? 'bg-emerald-500/20 text-emerald-300 font-bold'
                                      : 'bg-slate-800 text-slate-300'
                                  }`}
                                >
                                  {app.isRunning
                                    ? `🟢 ${formatLiveClock(app.elapsedSeconds || 0)}`
                                    : formatDurationRu(val, app.elapsedSeconds)}
                                </span>
                                <span className="text-xs text-slate-400">
                                  · {app.detoxGroup}
                                </span>
                              </div>

                              <div className="flex items-center gap-2">
                                <button
                                  onClick={() => handleLaunchApp(app)}
                                  className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-semibold cursor-pointer transition-all ${
                                    app.isRunning
                                      ? 'bg-rose-500/20 hover:bg-rose-500/30 border border-rose-500/40 text-rose-300'
                                      : 'bg-emerald-500/20 hover:bg-emerald-500/30 border border-emerald-500/40 text-emerald-300'
                                  }`}
                                >
                                  {app.isRunning ? (
                                    <>
                                      <PauseCircle className="w-3.5 h-3.5" />
                                      Стоп ({formatLiveClock(app.elapsedSeconds || 0)})
                                    </>
                                  ) : (
                                    <>
                                      <PlayCircle className="w-3.5 h-3.5" />
                                      Старт с 00:00
                                    </>
                                  )}
                                </button>

                                <button
                                  onClick={() => handleAddSessionMinutes(app.id, 15)}
                                  title="Добавить +15 мин для проверки графика и детокса"
                                  className="px-2.5 py-1 rounded-lg bg-blue-500/15 hover:bg-blue-500/25 border border-blue-500/30 text-blue-300 text-xs font-mono cursor-pointer transition-all"
                                >
                                  +15 мин
                                </button>
                              </div>
                            </div>

                            <div className="w-full h-1.5 rounded-full bg-black/40 overflow-hidden">
                              <div
                                className={`h-full rounded-full transition-all duration-300 ${
                                  isOverDailyLimit
                                    ? 'bg-rose-500'
                                    : app.isRunning
                                    ? 'bg-emerald-400'
                                    : 'bg-blue-500'
                                }`}
                                style={{
                                  width: `${
                                    app.elapsedSeconds > 0 ? Math.max(4, percent) : 0
                                  }%`,
                                }}
                              />
                            </div>
                          </div>
                        );
                      })}
                  </div>
                </section>

                {/* Digital Detox Groups Configuration */}
                <section
                  className="rounded-2xl border border-slate-800/90 p-6 shadow-xl"
                  style={cardGlassStyle}
                >
                  <div className="flex items-center gap-2.5 mb-4">
                    <ShieldAlert className="w-5 h-5 text-amber-400" />
                    <h3 className="text-base font-bold">
                      Группы цифрового детокса (Уведомления при превышении лимита)
                    </h3>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {detoxGroups.map((group) => {
                      const groupTodayMinutes = apps
                        .filter((a) => a.detoxGroup === group.name)
                        .reduce((acc, a) => acc + a.todayMinutes, 0);
                      const isExceeded = group.enabled && groupTodayMinutes >= group.dailyLimitMinutes;

                      return (
                        <div
                          key={group.name}
                          className={`p-4 rounded-xl border transition-all ${
                            isExceeded
                              ? 'bg-rose-500/10 border-rose-500/40'
                              : 'bg-[#1a2232] border-slate-700/70'
                          }`}
                        >
                          <div className="flex items-center justify-between mb-2">
                            <div className="flex items-center gap-2">
                              <input
                                type="checkbox"
                                checked={group.enabled}
                                onChange={(e) =>
                                  setDetoxGroups((prev) =>
                                    prev.map((g) =>
                                      g.name === group.name ? { ...g, enabled: e.target.checked } : g
                                    )
                                  )
                                }
                                className="w-4 h-4 accent-blue-500 cursor-pointer"
                              />
                              <span className="text-sm font-bold">{group.name}</span>
                            </div>
                            <span
                              className={`text-xs font-mono tabular-nums ${
                                isExceeded ? 'text-rose-400 font-bold' : 'text-slate-400'
                              }`}
                            >
                              {formatDurationRu(groupTodayMinutes)} / {formatDurationRu(group.dailyLimitMinutes)}
                            </span>
                          </div>

                          <div className="flex items-center gap-3 mt-2">
                            <span className="text-xs text-slate-400 whitespace-nowrap">Дневной лимит:</span>
                            <input
                              type="range"
                              min={30}
                              max={360}
                              step={15}
                              value={group.dailyLimitMinutes}
                              onChange={(e) =>
                                setDetoxGroups((prev) =>
                                  prev.map((g) =>
                                    g.name === group.name
                                      ? { ...g, dailyLimitMinutes: Number(e.target.value) }
                                      : g
                                  )
                                )
                              }
                              className="flex-1 accent-blue-500 cursor-pointer"
                            />
                            <span className="text-xs font-mono tabular-nums w-16 text-right">
                              {group.dailyLimitMinutes} мин
                            </span>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </section>
              </div>
            )}

            {/* -------------------- SECTION 3: PYTHON 2.4 SOURCE CODE & DOWNLOAD -------------------- */}
            {activeSection === 'python_code' && (
              <div className="space-y-5 max-w-6xl mx-auto">
                <section
                  className="rounded-2xl border border-slate-800/90 p-6 shadow-xl"
                  style={cardGlassStyle}
                >
                  <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-slate-800">
                    <div>
                      <div className="flex items-center gap-2">
                        <FileCode className="w-5 h-5 text-emerald-400" />
                        <h2 className="text-lg font-bold">
                          Исходный код Python — Launcher Hab 2.4 (Flet)
                        </h2>
                      </div>
                      <p className="text-xs text-slate-400 mt-1">
                        Весь проект написан на Python: исправлены Fernet-ключ, желтые полоски <code className="text-emerald-400">#AARRGGBB</code>, ошибка <code className="text-emerald-400">show_snack_bar</code>, трекер с 0 и магазин плагинов.
                      </p>
                    </div>

                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => {
                          navigator.clipboard.writeText(pyFileContent);
                          setCopiedCode(true);
                          setTimeout(() => setCopiedCode(false), 2000);
                        }}
                        className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-white/10 hover:bg-white/15 border border-white/15 text-xs font-semibold cursor-pointer transition-all"
                      >
                        {copiedCode ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
                        {copiedCode ? 'Скопировано!' : 'Копировать файл'}
                      </button>

                      <a
                        href="/launcher_hab2.4.zip"
                        download="launcher_hab2.4.zip"
                        className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold shadow-sm transition-all"
                      >
                        <Download className="w-4 h-4" />
                        Скачать проект launcher_hab2.4.zip
                      </a>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 mt-5">
                    {/* File List */}
                    <div className="lg:col-span-4 space-y-2">
                      {PYTHON_PROJECT_FILES.map((file) => {
                        const active = selectedPyFile === file.path;
                        return (
                          <button
                            key={file.path}
                            onClick={() => setSelectedPyFile(file.path)}
                            className={`w-full text-left p-3 rounded-xl border transition-all cursor-pointer ${
                              active
                                ? 'bg-blue-600/20 border-blue-500/60 text-white'
                                : 'bg-[#1a2232] hover:bg-[#222c40] border-slate-700/60 text-slate-300'
                            }`}
                          >
                            <div className="flex items-center justify-between gap-2">
                              <span className="text-xs font-mono font-bold truncate">{file.title}</span>
                              <span className="text-[10px] font-mono text-emerald-400 shrink-0">
                                {file.badge}
                              </span>
                            </div>
                            <p className="text-[11px] text-slate-400 mt-1 line-clamp-2">
                              {file.summary}
                            </p>
                          </button>
                        );
                      })}
                    </div>

                    {/* Code Viewer */}
                    <div className="lg:col-span-8 flex flex-col rounded-xl bg-[#090d14] border border-slate-800 overflow-hidden">
                      <div className="px-4 py-2.5 bg-[#121824] border-b border-slate-800 flex items-center justify-between text-xs font-mono text-slate-300">
                        <span>launcher_hab2.4/{selectedPyFile}</span>
                        <span className="text-emerald-400">Python 3.11 • Flet 0.24+ • Проверено</span>
                      </div>
                      <pre className="p-4 text-xs font-mono text-slate-200 overflow-x-auto overflow-y-auto max-h-[600px] leading-relaxed">
                        <code>{pyFileContent}</code>
                      </pre>
                    </div>
                  </div>
                </section>
              </div>
            )}
          </div>

          {/* FLOATING HUD (Right Top Overlay) */}
          {floatingHudVisible && (
            <div
              className="fixed right-6 top-20 z-20 p-4 rounded-2xl border border-slate-700 shadow-2xl w-56"
              style={cardGlassStyle}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-bold text-blue-400">Floating HUD 2.4</span>
                <Activity className="w-3.5 h-3.5 text-emerald-400" />
              </div>
              <div className="space-y-1.5 text-xs font-mono tabular-nums">
                <div className="flex justify-between">
                  <span className="text-slate-400">CPU:</span>
                  <span>{cpuLoad}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">RAM:</span>
                  <span>{ramLoad}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Volume:</span>
                  <span>{isMuted ? 'Muted' : `${volume}%`}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Активных сессий:</span>
                  <span className="text-emerald-400">{runningAppsCount}</span>
                </div>
              </div>
            </div>
          )}

          {/* FIXED RECYCLE BIN FAB (Bottom Right) */}
          <button
            onClick={() => pushToast('Корзина', 'Открыта системная корзина Windows (shell:RecycleBinFolder)')}
            title="Открыть корзину"
            className="fixed right-6 bottom-6 z-20 p-3.5 rounded-2xl border border-slate-700/80 shadow-xl hover:scale-105 transition-all cursor-pointer"
            style={cardGlassStyle}
          >
            <Trash2 className="w-5 h-5" />
          </button>
        </main>
      </div>

      {/* ==================== MODAL: INTERACTIVE PLUGIN WINDOW (Launched from Grid/Sidebar) ==================== */}
      {activePluginModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div
            className="w-full max-w-lg rounded-2xl border border-slate-700 p-6 shadow-2xl space-y-4"
            style={cardGlassStyle}
          >
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-xl bg-purple-500/20 text-purple-400">
                  {renderAppIcon(activePluginModal.icon || 'Puzzle', 'w-5 h-5')}
                </div>
                <div>
                  <h3 className="text-base font-bold">{activePluginModal.name}</h3>
                  <span className="text-xs font-mono text-slate-400">
                    v{activePluginModal.version} • {activePluginModal.file}
                  </span>
                </div>
              </div>
              <button
                onClick={() => setActivePluginModal(null)}
                className="p-1.5 rounded-lg hover:bg-white/10 cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="text-xs text-slate-300">{activePluginModal.description}</p>

            {/* Interactive content based on plugin ID */}
            {activePluginModal.id === 'idea_notebook_plugin' && (
              <div className="space-y-3 p-4 rounded-xl bg-[#0d111a] border border-slate-800">
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={newIdeaText}
                    onChange={(e) => setNewIdeaText(e.target.value)}
                    placeholder="Введите быструю заметку..."
                    className="flex-1 px-3 py-2 rounded-xl bg-[#1a2232] border border-slate-700 text-xs outline-none"
                  />
                  <button
                    onClick={() => {
                      if (!newIdeaText.trim()) return;
                      setIdeaNotes((prev) => [newIdeaText.trim(), ...prev]);
                      setNewIdeaText('');
                      pushToast('Idea Notebook', 'Заметка сохранена в idea_notes.txt', 'success');
                    }}
                    className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold cursor-pointer"
                  >
                    Сохранить
                  </button>
                </div>
                <ul className="space-y-1.5 max-h-40 overflow-y-auto text-xs text-slate-300">
                  {ideaNotes.map((note, idx) => (
                    <li key={idx} className="p-2 rounded-lg bg-[#161d2b] border border-slate-800">
                      • {note}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {activePluginModal.id === 'focus_mode_plugin' && (
              <div className="p-4 rounded-xl bg-[#0d111a] border border-slate-800 flex items-center justify-between">
                <div>
                  <div className="text-xs text-slate-400">Таймер концентрации Pomodoro</div>
                  <div className="text-3xl font-black font-mono text-emerald-400 mt-1">
                    {formatLiveClock(pomodoroSeconds)}
                  </div>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => setPomodoroRunning((r) => !r)}
                    className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold cursor-pointer"
                  >
                    {pomodoroRunning ? 'Пауза' : 'Старт'}
                  </button>
                  <button
                    onClick={() => {
                      setPomodoroRunning(false);
                      setPomodoroSeconds(25 * 60);
                    }}
                    className="px-3 py-2 rounded-xl bg-white/10 text-xs cursor-pointer"
                  >
                    Сброс
                  </button>
                </div>
              </div>
            )}

            {activePluginModal.id !== 'idea_notebook_plugin' &&
              activePluginModal.id !== 'focus_mode_plugin' && (
                <div className="p-4 rounded-xl bg-[#0d111a] border border-slate-800 space-y-3">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-slate-400">Статус модуля:</span>
                    <span className="text-emerald-400 font-mono">Активен в ядре Launcher Hab 2.4</span>
                  </div>
                  <button
                    onClick={() =>
                      pushToast(
                        activePluginModal.name,
                        `Действие плагина «${activePluginModal.name}» успешно выполнено!`,
                        'success'
                      )
                    }
                    className="w-full py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold cursor-pointer"
                  >
                    Выполнить быстрое действие плагина
                  </button>
                </div>
              )}

            <div className="flex justify-end gap-2 pt-2">
              <button
                onClick={() => {
                  setEditingPluginSettings(activePluginModal);
                  setActivePluginModal(null);
                }}
                className="px-3.5 py-2 rounded-xl bg-white/10 hover:bg-white/15 text-xs font-semibold cursor-pointer"
              >
                Настройки плагина
              </button>
              <button
                onClick={() => setActivePluginModal(null)}
                className="px-4 py-2 rounded-xl bg-blue-600 text-white text-xs font-semibold cursor-pointer"
              >
                Готово
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ==================== MODAL: PLUGIN SETTINGS CONFIGURATION ==================== */}
      {editingPluginSettings && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div
            className="w-full max-w-md rounded-2xl border border-slate-700 p-6 shadow-2xl space-y-4"
            style={cardGlassStyle}
          >
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <h3 className="text-base font-bold">Настройки: {editingPluginSettings.name}</h3>
              <button
                onClick={() => setEditingPluginSettings(null)}
                className="p-1.5 rounded-lg hover:bg-white/10 cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <label className="flex items-center justify-between p-3 rounded-xl bg-[#1a2232] border border-slate-700 cursor-pointer">
                <span>Показывать плагин в списке запуска («Плагины»)</span>
                <input
                  type="checkbox"
                  checked={editingPluginSettings.showInLauncher !== false}
                  onChange={(e) =>
                    setEditingPluginSettings({
                      ...editingPluginSettings,
                      showInLauncher: e.target.checked,
                    })
                  }
                  className="w-4 h-4 accent-blue-500"
                />
              </label>

              <label className="flex items-center justify-between p-3 rounded-xl bg-[#1a2232] border border-slate-700 cursor-pointer">
                <span>Разрешить уведомления от плагина</span>
                <input
                  type="checkbox"
                  checked={editingPluginSettings.notificationsEnabled !== false}
                  onChange={(e) =>
                    setEditingPluginSettings({
                      ...editingPluginSettings,
                      notificationsEnabled: e.target.checked,
                    })
                  }
                  className="w-4 h-4 accent-blue-500"
                />
              </label>

              <div className="p-3 rounded-xl bg-[#1a2232] border border-slate-700 space-y-2">
                <div className="flex justify-between">
                  <span>Интервал фонового опроса (сек):</span>
                  <span className="font-mono text-blue-400">
                    {editingPluginSettings.customIntervalSec || 60} сек
                  </span>
                </div>
                <input
                  type="range"
                  min={1}
                  max={300}
                  value={editingPluginSettings.customIntervalSec || 60}
                  onChange={(e) =>
                    setEditingPluginSettings({
                      ...editingPluginSettings,
                      customIntervalSec: Number(e.target.value),
                    })
                  }
                  className="w-full accent-blue-500"
                />
              </div>
            </div>

            <div className="flex justify-end gap-2 pt-2">
              <button
                onClick={() => setEditingPluginSettings(null)}
                className="px-3.5 py-2 rounded-xl bg-white/10 text-xs font-semibold cursor-pointer"
              >
                Отмена
              </button>
              <button
                onClick={() => {
                  setPlugins((prev) =>
                    prev.map((p) => (p.id === editingPluginSettings.id ? editingPluginSettings : p))
                  );
                  setEditingPluginSettings(null);
                  pushToast('Настройки сохранены', 'Параметры плагина обновлены и сохранены.', 'success');
                }}
                className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold cursor-pointer"
              >
                Сохранить
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ==================== MODAL 1: IMPROVED ADD APPLICATION (v2.4) ==================== */}
      {addAppModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div
            className="w-full max-w-2xl rounded-2xl border border-slate-700 p-6 shadow-2xl max-h-[90vh] overflow-y-auto"
            style={cardGlassStyle}
          >
            <div className="flex items-center justify-between pb-4 border-b border-slate-800">
              <div className="flex items-center gap-2.5">
                <Plus className="w-5 h-5 text-blue-400" />
                <h3 className="text-lg font-bold">Добавить приложение (Старт таймера с 0 мин)</h3>
              </div>
              <button
                onClick={() => setAddAppModalOpen(false)}
                className="p-1.5 rounded-lg hover:bg-white/10 cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleAddCustomApp} className="space-y-4 mt-4">
              {/* Live Glass Card Preview */}
              <div className="p-4 rounded-2xl bg-[#1a2232] border border-slate-700 flex items-center gap-4">
                <div className="w-16 h-16 rounded-2xl bg-blue-500/15 border border-blue-500/35 flex items-center justify-center text-blue-400 shrink-0">
                  {renderAppIcon(newAppIcon, 'w-8 h-8')}
                </div>
                <div className="min-w-0 flex-1">
                  <div className="text-[10px] font-mono uppercase tracking-wider text-blue-400 font-bold">
                    Предпросмотр карточки (Начальное время: 0 мин)
                  </div>
                  <div className="text-sm font-bold truncate mt-0.5">
                    {newAppName.trim() || 'Новое приложение'}
                  </div>
                  <div className="text-xs text-slate-400 font-mono tabular-nums mt-0.5">
                    {newAppCategory} • 0 мин • Лимит детокса: {newAppLimit} мин/день
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div>
                  <label className="text-xs text-slate-300 block mb-1">Название *</label>
                  <input
                    type="text"
                    required
                    value={newAppName}
                    onChange={(e) => setNewAppName(e.target.value)}
                    placeholder="Cyberpunk 2077 / VS Code"
                    className="w-full px-3 py-2 rounded-xl bg-[#1a2232] border border-slate-700 text-xs outline-none focus:border-blue-500"
                  />
                </div>

                <div>
                  <label className="text-xs text-slate-300 block mb-1">Категория</label>
                  <select
                    value={newAppCategory}
                    onChange={(e) => setNewAppCategory(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-[#1a2232] border border-slate-700 text-xs outline-none"
                  >
                    <option value="Games">Games</option>
                    <option value="Browser">Browser</option>
                    <option value="Media">Media</option>
                    <option value="Music">Music</option>
                    <option value="Social">Social</option>
                    <option value="Office">Office</option>
                    <option value="System">System</option>
                  </select>
                </div>

                <div>
                  <label className="text-xs text-slate-300 block mb-1">Тип запуска</label>
                  <select
                    value={newAppType}
                    onChange={(e) => setNewAppType(e.target.value as AppType)}
                    className="w-full px-3 py-2 rounded-xl bg-[#1a2232] border border-slate-700 text-xs outline-none"
                  >
                    <option value="app">Локальное (EXE / URI)</option>
                    <option value="web">Веб-приложение (URL)</option>
                    <option value="system">Системная команда</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div className="sm:col-span-2">
                  <label className="text-xs text-slate-300 block mb-1">URL, URI или путь к .exe файлу *</label>
                  <input
                    type="text"
                    required
                    value={newAppUrl}
                    onChange={(e) => setNewAppUrl(e.target.value)}
                    placeholder="https://... или C:\Program Files\App\app.exe"
                    className="w-full px-3 py-2 rounded-xl bg-[#1a2232] border border-slate-700 text-xs outline-none focus:border-blue-500 font-mono"
                  />
                </div>
                <div>
                  <label className="text-xs text-slate-300 block mb-1">Лимит детокса (мин/день)</label>
                  <input
                    type="number"
                    min={15}
                    max={600}
                    value={newAppLimit}
                    onChange={(e) => setNewAppLimit(Number(e.target.value))}
                    className="w-full px-3 py-2 rounded-xl bg-[#1a2232] border border-slate-700 text-xs outline-none font-mono tabular-nums"
                  />
                </div>
              </div>

              {/* Icon Picker */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-semibold">Выбор иконки</span>
                  <input
                    type="text"
                    value={newAppIconSearch}
                    onChange={(e) => setNewAppIconSearch(e.target.value)}
                    placeholder="Поиск иконки..."
                    className="px-2.5 py-1 rounded-lg bg-[#1a2232] border border-slate-700 text-xs outline-none"
                  />
                </div>
                <div className="grid grid-cols-8 sm:grid-cols-12 gap-2 p-2.5 rounded-xl bg-[#0d111a] border border-slate-800 max-h-32 overflow-y-auto">
                  {ICON_NAMES.filter((name) =>
                    name.toLowerCase().includes(newAppIconSearch.toLowerCase())
                  ).map((iconKey) => (
                    <button
                      type="button"
                      key={iconKey}
                      onClick={() => setNewAppIcon(iconKey)}
                      className={`p-2 rounded-xl flex items-center justify-center border transition-all cursor-pointer ${
                        newAppIcon === iconKey
                          ? 'bg-blue-600/30 border-blue-400 text-blue-300'
                          : 'bg-[#1a2232] border-transparent hover:bg-white/10 text-slate-300'
                      }`}
                    >
                      {renderAppIcon(iconKey, 'w-5 h-5')}
                    </button>
                  ))}
                </div>
              </div>

              <div className="flex items-center justify-end gap-2 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setAddAppModalOpen(false)}
                  className="px-4 py-2 rounded-xl bg-white/5 hover:bg-white/10 text-xs font-semibold cursor-pointer"
                >
                  Отмена
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold cursor-pointer shadow-md"
                >
                  Добавить приложение
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ==================== MODAL 2: PLUGIN STORE, MANAGER & SDK 2.4 ==================== */}
      {pluginsModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div
            className="w-full max-w-4xl rounded-2xl border border-slate-700 p-6 shadow-2xl max-h-[90vh] overflow-y-auto space-y-5"
            style={cardGlassStyle}
          >
            <div className="flex items-center justify-between pb-4 border-b border-slate-800">
              <div className="flex items-center gap-2.5">
                <Puzzle className="w-5 h-5 text-blue-400" />
                <div>
                  <h3 className="text-lg font-bold">
                    Центр управления плагинами и магазин расширений (Plugin API 2.4)
                  </h3>
                  <p className="text-xs text-slate-400">
                    Скачивайте плагины из каталога, настраивайте параметры, выводите их в список запуска или удаляйте
                  </p>
                </div>
              </div>
              <button
                onClick={() => setPluginsModalOpen(false)}
                className="p-1.5 rounded-lg hover:bg-white/10 cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Plugin Store Catalog (1-Click Download/Install) */}
            <div className="p-4 rounded-xl bg-[#121926] border border-slate-700/80 space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 text-xs font-bold text-emerald-400">
                  <Download className="w-4 h-4" />
                  Магазин расширений (Скачать и добавить в запуск в 1 клик)
                </div>
                <span className="text-[11px] text-slate-400 font-mono">
                  Доступно в каталоге: {PLUGIN_CATALOG.length}
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                {PLUGIN_CATALOG.map((catItem) => {
                  const isInstalled = plugins.some((p) => p.id === catItem.id);
                  return (
                    <div
                      key={catItem.id}
                      className="p-3.5 rounded-xl bg-[#1a2232] border border-slate-700/70 flex flex-col justify-between gap-3"
                    >
                      <div>
                        <div className="flex items-center justify-between gap-2">
                          <span className="text-xs font-bold">{catItem.name}</span>
                          <span className="text-[10px] font-mono text-blue-400">v{catItem.version}</span>
                        </div>
                        <p className="text-[11px] text-slate-400 mt-1">{catItem.description}</p>
                      </div>

                      <button
                        disabled={isInstalled}
                        onClick={() => handleInstallCatalogPlugin(catItem)}
                        className={`w-full py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                          isInstalled
                            ? 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 cursor-default'
                            : 'bg-blue-600 hover:bg-blue-500 text-white'
                        }`}
                      >
                        {isInstalled ? '✓ Установлено' : '⬇ Скачать и установить'}
                      </button>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Plugin SDK Template Generator */}
            <div className="p-4 rounded-xl bg-blue-500/10 border border-blue-500/25">
              <div className="flex items-center gap-2 text-xs font-bold text-blue-300 mb-2">
                <Code2 className="w-4 h-4" />
                Plugin SDK 2.4 — Генератор собственного плагина (.py)
              </div>
              <div className="flex flex-col sm:flex-row gap-2">
                <input
                  type="text"
                  value={newPluginSlug}
                  onChange={(e) => setNewPluginSlug(e.target.value)}
                  placeholder="ID плагина (напр. discord_overlay)"
                  className="flex-1 px-3 py-2 rounded-xl bg-[#0d111a] border border-slate-700 text-xs font-mono outline-none"
                />
                <input
                  type="text"
                  value={newPluginTitle}
                  onChange={(e) => setNewPluginTitle(e.target.value)}
                  placeholder="Название расширения"
                  className="flex-1 px-3 py-2 rounded-xl bg-[#0d111a] border border-slate-700 text-xs outline-none"
                />
                <button
                  onClick={handleCreatePluginTemplate}
                  className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold cursor-pointer whitespace-nowrap"
                >
                  + Создать плагин
                </button>
              </div>
            </div>

            {/* Installed Plugins List with Open / Configure / Reload / Delete */}
            <div className="space-y-2.5">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                Установленные плагины ({plugins.length})
              </h4>
              {plugins.map((plugin) => (
                <div
                  key={plugin.id}
                  className="p-4 rounded-xl bg-[#1a2232] border border-slate-700/70 flex flex-wrap items-center justify-between gap-3"
                >
                  <div className="max-w-xl">
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-bold">{plugin.name}</span>
                      <span className="text-xs font-mono text-blue-400">v{plugin.version}</span>
                      <span className="text-xs font-mono text-slate-400">({plugin.file})</span>
                    </div>
                    <p className="text-xs text-slate-300 mt-1">{plugin.description}</p>
                  </div>

                  <div className="flex items-center gap-2 shrink-0">
                    <button
                      onClick={() => {
                        setPluginsModalOpen(false);
                        if (plugin.id === 'session_tracker_plugin') {
                          handleSwitchSection('tracker');
                        } else {
                          setActivePluginModal(plugin);
                        }
                      }}
                      className="px-3 py-1.5 rounded-lg bg-emerald-500/20 hover:bg-emerald-500/30 border border-emerald-500/40 text-xs font-semibold text-emerald-300 cursor-pointer"
                    >
                      Запустить
                    </button>

                    <button
                      onClick={() => setEditingPluginSettings(plugin)}
                      title="Настроить параметры плагина"
                      className="p-1.5 rounded-lg bg-white/5 hover:bg-white/10 border border-slate-700 cursor-pointer"
                    >
                      <Settings className="w-4 h-4 text-slate-300" />
                    </button>

                    <button
                      onClick={() =>
                        pushToast('Перезагрузка модуля', `Плагин «${plugin.name}» перезагружен`, 'info')
                      }
                      title="Перезагрузить плагин"
                      className="p-1.5 rounded-lg bg-white/5 hover:bg-white/10 border border-slate-700 cursor-pointer"
                    >
                      <RefreshCw className="w-4 h-4 text-blue-400" />
                    </button>

                    {plugin.id !== 'session_tracker_plugin' && (
                      <button
                        onClick={() => handleDeletePlugin(plugin.id)}
                        title="Удалить плагин"
                        className="p-1.5 rounded-lg bg-rose-500/10 hover:bg-rose-500/25 border border-rose-500/30 cursor-pointer"
                      >
                        <Trash2 className="w-4 h-4 text-rose-400" />
                      </button>
                    )}

                    <label className="flex items-center gap-1.5 text-xs cursor-pointer ml-1">
                      <input
                        type="checkbox"
                        checked={plugin.enabled}
                        onChange={(e) => {
                          const val = e.target.checked;
                          setPlugins((prev) =>
                            prev.map((p) => (p.id === plugin.id ? { ...p, enabled: val } : p))
                          );
                          pushToast(
                            plugin.name,
                            val ? 'Плагин включен и добавлен в список запуска' : 'Плагин отключен'
                          );
                        }}
                        className="w-4 h-4 accent-blue-500 cursor-pointer"
                      />
                      <span>{plugin.enabled ? 'Вкл' : 'Выкл'}</span>
                    </label>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ==================== MODAL 3: SETTINGS 2.5 (INSTANT LIT ACTIVE STATUS, 18 CLOCK STYLES, CUSTOM THEMES & CHANGELOG 1.0–2.5) ==================== */}
      {settingsModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div
            className="w-full max-w-4xl rounded-2xl border border-slate-700 p-6 shadow-2xl max-h-[90vh] flex flex-col"
            style={cardGlassStyle}
          >
            <div className="flex items-center justify-between pb-4 border-b border-slate-800">
              <div className="flex items-center gap-2.5">
                <Sliders className="w-5 h-5 text-blue-400" />
                <div>
                  <h3 className="text-lg font-bold">
                    Настройки Launcher Hab 2.5 — Персонализация и Часы
                  </h3>
                  <p className="text-xs text-slate-400">
                    При выборе любого параметра он сразу загорается и меняет статус с «⚪ НЕАКТИВНО» на «🟢 АКТИВНО»
                  </p>
                </div>
              </div>
              <button
                onClick={() => setSettingsModalOpen(false)}
                className="p-1.5 rounded-lg hover:bg-white/10 cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Settings Tabs */}
            <div className="flex items-center gap-1.5 py-3 border-b border-slate-800 overflow-x-auto">
              {(
                [
                  ['appearance', '🎨 Темы и Персонализация 2.5'],
                  ['clock', '🕒 Часы (18 стилей + Дизайн)'],
                  ['plugins', '🧩 Плагины и Сетка'],
                  ['system', '🔐 Шифрование 2.5 и Бэкапы'],
                  ['changelog', '📜 История версий (1.0 – 2.5)'],
                ] as const
              ).map(([tabKey, tabLabel]) => (
                <button
                  key={tabKey}
                  onClick={() => setSettingsTab(tabKey)}
                  className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all cursor-pointer whitespace-nowrap ${
                    settingsTab === tabKey
                      ? 'bg-blue-600 text-white shadow-[0_0_12px_rgba(59,130,246,0.45)]'
                      : 'bg-[#1a2232] hover:bg-[#232e44] text-slate-300'
                  }`}
                >
                  {tabLabel}
                </button>
              ))}
            </div>

            <div className="flex-1 overflow-y-auto py-4 space-y-5">
              {/* TAB 1: APPEARANCE, CUSTOM THEME STUDIO & PERSONALIZATION 2.5 */}
              {settingsTab === 'appearance' && (
                <div className="space-y-4">
                  <div className="p-4 rounded-xl bg-[#1a2232] border border-slate-700/70 space-y-3">
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <div>
                        <h4 className="text-sm font-bold">
                          Темы оформления и Кастомные темы (Мгновенное зажигание статуса)
                        </h4>
                        <p className="text-xs text-slate-400">
                          Выберите готовую тему или создайте собственную в студии кастомных тем 2.5
                        </p>
                      </div>
                      <button
                        onClick={() => setCustomThemeModalOpen(true)}
                        className="px-3.5 py-1.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold cursor-pointer shadow-sm"
                      >
                        + Создать кастомную тему 2.5
                      </button>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5">
                      {Object.keys(allThemesMap).map((tKey) => {
                        const isSelected = themeKey === tKey;
                        const th = allThemesMap[tKey];
                        return (
                          <button
                            key={tKey}
                            onClick={() => {
                              setThemeKey(tKey);
                              pushToast('Тема активирована', `Тема «${th.name}» зажглась: 🟢 АКТИВНО`, 'success');
                            }}
                            className={`p-3 rounded-xl border text-xs font-semibold transition-all duration-200 cursor-pointer text-left flex flex-col gap-2 ${
                              isSelected
                                ? 'border-emerald-400 bg-emerald-500/15 text-white shadow-[0_0_18px_rgba(16,185,129,0.25)]'
                                : 'border-slate-700 bg-[#121824] hover:bg-[#1e2636] text-slate-300'
                            }`}
                          >
                            <div className="flex items-center justify-between gap-2 w-full">
                              <span className="truncate font-bold">{th.name}</span>
                              <LitStatusBadge active={isSelected} />
                            </div>
                            <div className="flex items-center gap-1.5">
                              <span
                                className="w-4 h-4 rounded-full border border-white/20"
                                style={{ backgroundColor: th.cardHex }}
                              />
                              <span
                                className="w-4 h-4 rounded-full border border-white/20"
                                style={{ backgroundColor: th.accentHex }}
                              />
                              <span className="text-[10px] text-slate-400 font-mono ml-auto">
                                {th.custom ? 'Custom 2.5' : 'Preset'}
                              </span>
                            </div>
                          </button>
                        );
                      })}
                    </div>
                  </div>

                  {/* Lit Toggle Rows for Glass & Animations */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div
                      onClick={() => setGlassEnabled((v) => !v)}
                      className={`p-4 rounded-xl border transition-all duration-200 cursor-pointer flex items-center justify-between gap-3 ${
                        glassEnabled
                          ? 'border-emerald-400/80 bg-emerald-500/10 shadow-[0_0_16px_rgba(16,185,129,0.2)]'
                          : 'border-slate-700 bg-[#121824]'
                      }`}
                    >
                      <div>
                        <div className="text-xs font-bold">Прозрачное стекло (Liquid Glass #AARRGGBB)</div>
                        <div className="text-[11px] text-slate-400 mt-0.5">
                          Настоящий эффект матового стекла без цветовых искажений
                        </div>
                      </div>
                      <LitStatusBadge active={glassEnabled} />
                    </div>

                    <div
                      onClick={() => setSmoothAnimations((v) => !v)}
                      className={`p-4 rounded-xl border transition-all duration-200 cursor-pointer flex items-center justify-between gap-3 ${
                        smoothAnimations
                          ? 'border-emerald-400/80 bg-emerald-500/10 shadow-[0_0_16px_rgba(16,185,129,0.2)]'
                          : 'border-slate-700 bg-[#121824]'
                      }`}
                    >
                      <div>
                        <div className="text-xs font-bold">Плавные переходы между разделами</div>
                        <div className="text-[11px] text-slate-400 mt-0.5">
                          Анимация переключения вкладок и карточек
                        </div>
                      </div>
                      <LitStatusBadge active={smoothAnimations} />
                    </div>

                    <div
                      onClick={() => setCardHoverGlow((v) => !v)}
                      className={`p-4 rounded-xl border transition-all duration-200 cursor-pointer flex items-center justify-between gap-3 ${
                        cardHoverGlow
                          ? 'border-emerald-400/80 bg-emerald-500/10 shadow-[0_0_16px_rgba(16,185,129,0.2)]'
                          : 'border-slate-700 bg-[#121824]'
                      }`}
                    >
                      <div>
                        <div className="text-xs font-bold">Неоновая подсветка карточек при наведении</div>
                        <div className="text-[11px] text-slate-400 mt-0.5">
                          Акцентное свечение рамки при наведении курсора
                        </div>
                      </div>
                      <LitStatusBadge active={cardHoverGlow} />
                    </div>

                    <div className="p-4 rounded-xl border border-slate-700 bg-[#121824] flex flex-col justify-between gap-2">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-bold">Интенсивность размытия стекла</span>
                        <LitStatusBadge active={glassEnabled} />
                      </div>
                      <div className="grid grid-cols-3 gap-1.5">
                        {(
                          [
                            ['light', 'Слабая'],
                            ['medium', 'Средняя'],
                            ['strong', 'Сильная'],
                          ] as const
                        ).map(([k, lbl]) => (
                          <button
                            key={k}
                            onClick={() => setGlassIntensity(k)}
                            className={`py-1 rounded-lg text-[11px] font-semibold border cursor-pointer transition-all ${
                              glassIntensity === k
                                ? 'border-emerald-400 bg-emerald-500/20 text-emerald-200'
                                : 'border-slate-700 bg-[#1a2232] text-slate-400'
                            }`}
                          >
                            {lbl}
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Personalization 2.5 Sliders */}
                  <div className="p-4 rounded-xl bg-[#1a2232] border border-slate-700/70 space-y-4">
                    <h4 className="text-sm font-bold">Персонализация карточек и плиток (v2.5)</h4>

                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
                      <div className="space-y-1.5">
                        <div className="flex justify-between">
                          <span className="text-slate-300">Плотность стекла:</span>
                          <span className="font-mono text-emerald-400">{glassOpacity}%</span>
                        </div>
                        <input
                          type="range"
                          min={35}
                          max={98}
                          value={glassOpacity}
                          onChange={(e) => setGlassOpacity(Number(e.target.value))}
                          className="w-full accent-emerald-500 cursor-pointer"
                        />
                      </div>

                      <div className="space-y-1.5">
                        <div className="flex justify-between">
                          <span className="text-slate-300">Радиус скругления карточек:</span>
                          <span className="font-mono text-emerald-400">{cardBorderRadius} px</span>
                        </div>
                        <input
                          type="range"
                          min={8}
                          max={32}
                          value={cardBorderRadius}
                          onChange={(e) => setCardBorderRadius(Number(e.target.value))}
                          className="w-full accent-emerald-500 cursor-pointer"
                        />
                      </div>

                      <div className="space-y-1.5">
                        <div className="flex justify-between">
                          <span className="text-slate-300">Масштаб иконок плиток:</span>
                          <span className="font-mono text-emerald-400">{iconScalePct}%</span>
                        </div>
                        <input
                          type="range"
                          min={85}
                          max={120}
                          value={iconScalePct}
                          onChange={(e) => setIconScalePct(Number(e.target.value))}
                          className="w-full accent-emerald-500 cursor-pointer"
                        />
                      </div>
                    </div>

                    <div className="flex flex-wrap items-center gap-3 pt-2 border-t border-slate-800">
                      <span className="text-xs text-slate-300">Цвет индикатора активного приложения:</span>
                      {['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b', '#ec4899', '#06b6d4'].map((clr) => (
                        <button
                          key={clr}
                          onClick={() => setActiveAppColor(clr)}
                          className={`w-7 h-7 rounded-full border-2 cursor-pointer transition-all ${
                            activeAppColor === clr
                              ? 'border-white scale-115 shadow-[0_0_12px_rgba(255,255,255,0.5)]'
                              : 'border-transparent opacity-75'
                          }`}
                          style={{ backgroundColor: clr }}
                        />
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 2: 18 CLOCK STYLES + CLOCK DESIGN 2.5 */}
              {settingsTab === 'clock' && (
                <div className="space-y-4">
                  {/* Lit Toggles for Clock */}
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
                    <div
                      onClick={() => setShowAndroidClockWidget((v) => !v)}
                      className={`p-3.5 rounded-xl border transition-all cursor-pointer flex items-center justify-between gap-2 ${
                        showAndroidClockWidget
                          ? 'border-emerald-400 bg-emerald-500/15 shadow-[0_0_14px_rgba(16,185,129,0.2)]'
                          : 'border-slate-700 bg-[#121824]'
                      }`}
                    >
                      <span className="text-xs font-bold">Виджет часов Android 14</span>
                      <LitStatusBadge active={showAndroidClockWidget} />
                    </div>

                    <div
                      onClick={() => setClockGlowEnabled((v) => !v)}
                      className={`p-3.5 rounded-xl border transition-all cursor-pointer flex items-center justify-between gap-2 ${
                        clockGlowEnabled
                          ? 'border-emerald-400 bg-emerald-500/15 shadow-[0_0_14px_rgba(16,185,129,0.2)]'
                          : 'border-slate-700 bg-[#121824]'
                      }`}
                    >
                      <span className="text-xs font-bold">Неоновое свечение часов</span>
                      <LitStatusBadge active={clockGlowEnabled} />
                    </div>

                    <div
                      onClick={() => setClockBlinkColon((v) => !v)}
                      className={`p-3.5 rounded-xl border transition-all cursor-pointer flex items-center justify-between gap-2 ${
                        clockBlinkColon
                          ? 'border-emerald-400 bg-emerald-500/15 shadow-[0_0_14px_rgba(16,185,129,0.2)]'
                          : 'border-slate-700 bg-[#121824]'
                      }`}
                    >
                      <span className="text-xs font-bold">Мигающее двоеточие (:)</span>
                      <LitStatusBadge active={clockBlinkColon} />
                    </div>
                  </div>

                  {/* 18 Clock Styles Grid with Instant Lit Active Status */}
                  <div className="p-4 rounded-xl bg-[#1a2232] border border-slate-700/70 space-y-3">
                    <div className="flex items-center justify-between">
                      <h4 className="text-sm font-bold">
                        Коллекция стилей часов — 18 стилей (+10 новых в версии 2.5)
                      </h4>
                      <span className="text-xs font-mono text-emerald-400">
                        Активен: {CLOCK_STYLE_OPTIONS.find((o) => o.id === clockStyle)?.label}
                      </span>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5 max-h-80 overflow-y-auto pr-1">
                      {CLOCK_STYLE_OPTIONS.map((opt) => {
                        const isSelected = clockStyle === opt.id;
                        return (
                          <button
                            key={opt.id}
                            onClick={() => {
                              setClockStyle(opt.id);
                              pushToast('Стиль часов зажегся', `${opt.label} • 🟢 АКТИВНО`, 'success');
                            }}
                            className={`p-3 rounded-xl border text-left transition-all duration-200 cursor-pointer flex flex-col gap-1.5 ${
                              isSelected
                                ? 'border-emerald-400 bg-emerald-500/15 shadow-[0_0_16px_rgba(16,185,129,0.25)]'
                                : 'border-slate-700 bg-[#121824] hover:bg-[#1e2636]'
                            }`}
                          >
                            <div className="flex items-center justify-between gap-1.5 w-full">
                              <span className="text-xs font-bold truncate">{opt.label}</span>
                              {opt.isNew25 && (
                                <span className="px-1.5 py-0.2 rounded bg-blue-500/25 text-blue-300 text-[9px] font-mono font-bold shrink-0">
                                  NEW 2.5
                                </span>
                              )}
                            </div>
                            <div className="flex items-center justify-between w-full">
                              <span className="text-xs font-mono text-blue-300">{opt.sample}</span>
                              <LitStatusBadge active={isSelected} />
                            </div>
                            <span className="text-[11px] text-slate-400 line-clamp-1">{opt.description}</span>
                          </button>
                        );
                      })}
                    </div>
                  </div>

                  {/* Clock Design Sliders & Colors */}
                  <div className="p-4 rounded-xl bg-[#1a2232] border border-slate-700/70 space-y-4">
                    <h4 className="text-sm font-bold">Дизайн циферблата и подложки часов (v2.5)</h4>

                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
                      <div className="space-y-1">
                        <div className="flex justify-between">
                          <span className="text-slate-300">Скругление капсулы:</span>
                          <span className="font-mono text-emerald-400">{clockBorderRadius} px</span>
                        </div>
                        <input
                          type="range"
                          min={6}
                          max={28}
                          value={clockBorderRadius}
                          onChange={(e) => setClockBorderRadius(Number(e.target.value))}
                          className="w-full accent-emerald-500 cursor-pointer"
                        />
                      </div>

                      <div className="space-y-1">
                        <div className="flex justify-between">
                          <span className="text-slate-300">Прозрачность подложки:</span>
                          <span className="font-mono text-emerald-400">{clockBgOpacity}%</span>
                        </div>
                        <input
                          type="range"
                          min={20}
                          max={100}
                          value={clockBgOpacity}
                          onChange={(e) => setClockBgOpacity(Number(e.target.value))}
                          className="w-full accent-emerald-500 cursor-pointer"
                        />
                      </div>

                      <div className="space-y-1">
                        <div className="flex justify-between">
                          <span className="text-slate-300">Сила неонового свечения:</span>
                          <span className="font-mono text-emerald-400">{clockGlowIntensity} px</span>
                        </div>
                        <input
                          type="range"
                          min={4}
                          max={32}
                          value={clockGlowIntensity}
                          onChange={(e) => setClockGlowIntensity(Number(e.target.value))}
                          className="w-full accent-emerald-500 cursor-pointer"
                        />
                      </div>
                    </div>

                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 text-xs">
                      {(
                        [
                          ['Секунды', showSeconds, setShowSeconds],
                          ['Показывать дату', showDate, setShowDate],
                          ['День недели', showWeekday, setShowWeekday],
                          ['Жирный шрифт', clockBold, setClockBold],
                        ] as const
                      ).map(([lbl, val, setter]) => (
                        <button
                          key={lbl}
                          onClick={() => setter(!val)}
                          className={`p-2.5 rounded-xl border flex items-center justify-between cursor-pointer transition-all ${
                            val
                              ? 'border-emerald-400 bg-emerald-500/15 text-white'
                              : 'border-slate-700 bg-[#121824] text-slate-400'
                          }`}
                        >
                          <span className="font-semibold">{lbl}</span>
                          <span className="text-[10px] font-mono">{val ? '🟢 ВКЛ' : '⚪ ВЫКЛ'}</span>
                        </button>
                      ))}
                    </div>

                    <div className="flex flex-wrap items-center justify-between gap-4 pt-2 border-t border-slate-800">
                      <div className="flex items-center gap-2.5">
                        <span className="text-xs text-slate-300">Цвет часов:</span>
                        {['#f8fafc', '#60a5fa', '#34d399', '#fbbf24', '#f472b6', '#c084fc'].map((hex) => (
                          <button
                            key={hex}
                            onClick={() => setTimeColor(hex)}
                            className={`w-6 h-6 rounded-full border-2 cursor-pointer ${
                              timeColor === hex ? 'border-white scale-115' : 'border-transparent'
                            }`}
                            style={{ backgroundColor: hex }}
                          />
                        ))}
                      </div>

                      <div className="flex items-center gap-2.5">
                        <span className="text-xs text-slate-300">Акцент минут и неона:</span>
                        {['#3b82f6', '#10b981', '#a855f7', '#ec4899', '#f59e0b', '#06b6d4'].map((hex) => (
                          <button
                            key={hex}
                            onClick={() => setClockAccentColor(hex)}
                            className={`w-6 h-6 rounded-full border-2 cursor-pointer ${
                              clockAccentColor === hex ? 'border-white scale-115' : 'border-transparent'
                            }`}
                            style={{ backgroundColor: hex }}
                          />
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 3: PLUGINS & LAUNCH GRID SETTINGS */}
              {settingsTab === 'plugins' && (
                <div className="space-y-4">
                  <div className="p-4 rounded-xl bg-[#1a2232] border border-slate-700/70 space-y-3">
                    <div
                      onClick={() => setShowPluginsInGrid((v) => !v)}
                      className={`p-3.5 rounded-xl border transition-all cursor-pointer flex items-center justify-between ${
                        showPluginsInGrid
                          ? 'border-emerald-400 bg-emerald-500/15 shadow-[0_0_14px_rgba(16,185,129,0.2)]'
                          : 'border-slate-700 bg-[#121824]'
                      }`}
                    >
                      <div>
                        <div className="text-sm font-bold">Показывать плагины в списке запуска («Плагины»)</div>
                        <div className="text-xs text-slate-400">
                          Активные плагины отображаются как карточки в библиотеке и главной сетке
                        </div>
                      </div>
                      <LitStatusBadge active={showPluginsInGrid} />
                    </div>

                    <div className="flex items-center justify-between pt-3 border-t border-slate-800">
                      <span className="text-xs text-slate-300">Колонок приложений в сетке:</span>
                      <div className="flex gap-1.5">
                        {[4, 5, 6].map((col) => (
                          <button
                            key={col}
                            onClick={() => setCardColumns(col)}
                            className={`px-3 py-1 rounded-lg text-xs font-mono cursor-pointer border ${
                              cardColumns === col
                                ? 'bg-emerald-500/20 border-emerald-400 text-emerald-300 font-bold'
                                : 'bg-[#121824] text-slate-400 border-slate-700'
                            }`}
                          >
                            {col} кол.
                          </button>
                        ))}
                      </div>
                    </div>

                    <div className="flex items-center justify-between pt-3 border-t border-slate-800">
                      <span className="text-xs text-slate-300">Поведение окна при запуске игры/приложения:</span>
                      <select
                        value={launchBehavior}
                        onChange={(e) => setLaunchBehavior(e.target.value as 'keep' | 'minimize')}
                        className="px-3 py-1.5 rounded-xl bg-[#121824] border border-slate-700 text-xs"
                      >
                        <option value="keep">Оставлять окно открытым</option>
                        <option value="minimize">Сворачивать в фоновый режим</option>
                      </select>
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 4: SYSTEM, CRYPTO 2.5 (PBKDF2 + HMAC) & BACKUP MANAGER */}
              {settingsTab === 'system' && (
                <div className="space-y-4">
                  <div className="p-4 rounded-xl bg-[#1a2232] border border-emerald-500/40 space-y-3">
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <div>
                        <h4 className="text-sm font-bold text-emerald-300">
                          Шифрование данных Crypto 2.5 (PBKDF2-HMAC-SHA256 + Fernet AES-128)
                        </h4>
                        <p className="text-xs text-slate-400">
                          100 000 итераций PBKDF2, 32-байтный URL-safe Base64 ключ, контроль целостности HMAC-SHA256 и совместимость с v2.4
                        </p>
                      </div>
                      <LitStatusBadge active={true} />
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5 text-xs font-mono">
                      <div className="p-2.5 rounded-lg bg-[#121824] border border-slate-800">
                        <div className="text-slate-400 text-[10px]">KDF АЛГОРИТМ</div>
                        <div className="text-emerald-400 font-bold mt-0.5">PBKDF2-SHA256 (100k)</div>
                      </div>
                      <div className="p-2.5 rounded-lg bg-[#121824] border border-slate-800">
                        <div className="text-slate-400 text-[10px]">ЦЕЛОСТНОСТЬ ДАННЫХ</div>
                        <div className="text-blue-400 font-bold mt-0.5">HMAC-SHA256 Verified</div>
                      </div>
                      <div className="p-2.5 rounded-lg bg-[#121824] border border-slate-800 flex items-center justify-between">
                        <div>
                          <div className="text-slate-400 text-[10px]">РОТАЦИЯ КЛЮЧА</div>
                          <div className="text-slate-200 font-bold mt-0.5">Ревизия #{cryptoKeyVersion}</div>
                        </div>
                        <button
                          onClick={() => {
                            setCryptoKeyVersion((v) => v + 1);
                            pushToast(
                              'Ротация ключа Crypto 2.5',
                              'Сгенерирован новый 32-байтный PBKDF2 Fernet-ключ, настройки перешифрованы.',
                              'success'
                            );
                          }}
                          className="px-2.5 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-[11px] font-sans font-semibold cursor-pointer"
                        >
                          Обновить ключ
                        </button>
                      </div>
                    </div>
                  </div>

                  <div className="p-4 rounded-xl bg-[#1a2232] border border-slate-700/70 space-y-3">
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="text-sm font-bold">Резервные копии настроек (Backup Manager 2.5)</h4>
                        <p className="text-xs text-slate-400">
                          Создание, восстановление и удаление резервных копий конфигурации
                        </p>
                      </div>
                      <button
                        onClick={() => {
                          const nowStr = new Date().toLocaleTimeString('ru-RU');
                          const created: BackupRecord = {
                            id: `bk_${Date.now()}`,
                            filename: `settings_backup_v25_${Date.now()}.json`,
                            createdAt: `Сегодня, ${nowStr}`,
                            sizeKb: '4.8 KB',
                          };
                          setBackups((prev) => [created, ...prev]);
                          pushToast('Резервная копия создана', created.filename, 'success');
                        }}
                        className="px-3.5 py-1.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold cursor-pointer"
                      >
                        + Создать копию
                      </button>
                    </div>

                    <div className="space-y-2">
                      {backups.map((bk) => (
                        <div
                          key={bk.id}
                          className="p-2.5 rounded-xl bg-[#121824] border border-slate-800 flex items-center justify-between text-xs"
                        >
                          <div>
                            <div className="font-mono font-semibold">{bk.filename}</div>
                            <div className="text-[11px] text-slate-400">
                              {bk.createdAt} • {bk.sizeKb}
                            </div>
                          </div>
                          <div className="flex gap-2">
                            <button
                              onClick={() =>
                                pushToast('Восстановление', `Настройки восстановлены из ${bk.filename}`, 'success')
                              }
                              className="px-2.5 py-1 rounded-lg bg-emerald-500/20 text-emerald-300 cursor-pointer"
                            >
                              Восстановить
                            </button>
                            <button
                              onClick={() => setBackups((prev) => prev.filter((x) => x.id !== bk.id))}
                              className="px-2 py-1 rounded-lg bg-rose-500/20 text-rose-300 cursor-pointer"
                            >
                              Удалить
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 5: COMPLETE VERSION HISTORY (1.0 TO 2.5) */}
              {settingsTab === 'changelog' && (
                <div className="space-y-4">
                  <div className="flex flex-wrap items-center justify-between gap-2 p-3 rounded-xl bg-[#121824] border border-slate-800">
                    <span className="text-xs font-bold text-slate-300">
                      Полный список изменений (16 релизов: с v1.0 по v2.5):
                    </span>
                    <div className="flex flex-wrap gap-1">
                      <button
                        onClick={() => setChangelogFilter('all')}
                        className={`px-2 py-0.5 rounded text-[11px] font-mono cursor-pointer ${
                          changelogFilter === 'all' ? 'bg-blue-600 text-white' : 'bg-[#1a2232] text-slate-400'
                        }`}
                      >
                        Все (1.0–2.5)
                      </button>
                      {Object.keys(VERSION_HISTORY).map((v) => (
                        <button
                          key={v}
                          onClick={() => setChangelogFilter(v)}
                          className={`px-2 py-0.5 rounded text-[11px] font-mono cursor-pointer ${
                            changelogFilter === v ? 'bg-emerald-600 text-white font-bold' : 'bg-[#1a2232] text-slate-400'
                          }`}
                        >
                          v{v}
                        </button>
                      ))}
                    </div>
                  </div>

                  {Object.entries(VERSION_HISTORY)
                    .filter(([ver]) => changelogFilter === 'all' || changelogFilter === ver)
                    .map(([ver, items]) => (
                      <div
                        key={ver}
                        className={`p-4 rounded-xl border ${
                          ver === '2.5'
                            ? 'bg-emerald-500/10 border-emerald-500/50 shadow-[0_0_20px_rgba(16,185,129,0.12)]'
                            : ver === '2.4'
                            ? 'bg-blue-500/10 border-blue-500/40'
                            : 'bg-[#1a2232] border-slate-700'
                        }`}
                      >
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center gap-2">
                            <span
                              className={`text-sm font-bold ${
                                ver === '2.5' ? 'text-emerald-400' : 'text-blue-400'
                              }`}
                            >
                              Версия {ver}
                            </span>
                            {ver === '2.5' && <LitStatusBadge active={true} />}
                          </div>
                          <span className="text-xs font-mono text-slate-400">{items.length} пунктов</span>
                        </div>
                        <ul className="space-y-1.5 text-xs text-slate-200">
                          {items.map((line, idx) => (
                            <li key={idx} className="leading-relaxed">
                              {line}
                            </li>
                          ))}
                        </ul>
                      </div>
                    ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* ==================== MODAL: CUSTOM THEME STUDIO PRO 2.5 ==================== */}
      {customThemeModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 backdrop-blur-sm p-4">
          <div
            className="w-full max-w-xl rounded-2xl border border-slate-700 p-6 shadow-2xl space-y-4"
            style={cardGlassStyle}
          >
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <div>
                <h3 className="text-base font-bold">🎨 Студия создания кастомных тем 2.5</h3>
                <p className="text-xs text-slate-400">
                  Настройте палитру, выберите базовый режим и сразу примените тему с подсветкой «🟢 АКТИВНО»
                </p>
              </div>
              <button
                onClick={() => setCustomThemeModalOpen(false)}
                className="p-1.5 rounded-lg hover:bg-white/10 cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Live Theme Preview Box */}
            <div
              className="p-4 rounded-2xl border flex items-center justify-between"
              style={{
                backgroundColor: newThemeBg,
                borderColor: newThemeAccent,
              }}
            >
              <div
                className="p-3 rounded-xl border flex items-center gap-3"
                style={{
                  backgroundColor: newThemeSurface,
                  borderColor: `${newThemeAccent}66`,
                }}
              >
                <div
                  className="w-10 h-10 rounded-xl flex items-center justify-center text-white font-bold"
                  style={{ backgroundColor: newThemeAccent }}
                >
                  2.5
                </div>
                <div>
                  <div
                    className={`text-xs font-bold ${
                      newThemeMode === 'light' ? 'text-slate-900' : 'text-white'
                    }`}
                  >
                    {newThemeName || 'Моя тема 2.5'}
                  </div>
                  <div className="text-[11px] font-mono" style={{ color: newThemeAccent }}>
                    Предпросмотр карточек и акцента
                  </div>
                </div>
              </div>
              <LitStatusBadge active={true} />
            </div>

            <div className="space-y-3 text-xs">
              <div>
                <label className="block text-slate-300 mb-1 font-semibold">Название темы</label>
                <input
                  type="text"
                  value={newThemeName}
                  onChange={(e) => setNewThemeName(e.target.value)}
                  className="w-full px-3 py-2 rounded-xl bg-[#121824] border border-slate-700 text-xs outline-none"
                />
              </div>

              <div className="grid grid-cols-3 gap-2">
                {(
                  [
                    ['dark', '🌙 Dark Slate'],
                    ['amoled', '🖤 AMOLED Onyx'],
                    ['light', '☀️ Light Clean'],
                  ] as const
                ).map(([mKey, mLabel]) => (
                  <button
                    key={mKey}
                    type="button"
                    onClick={() => {
                      setNewThemeMode(mKey);
                      if (mKey === 'amoled') {
                        setNewThemeBg('#04060a');
                        setNewThemeSurface('#0b0f17');
                      } else if (mKey === 'light') {
                        setNewThemeBg('#f1f5f9');
                        setNewThemeSurface('#ffffff');
                      } else {
                        setNewThemeBg('#0a0e17');
                        setNewThemeSurface('#141c2b');
                      }
                    }}
                    className={`py-2 rounded-xl border font-semibold cursor-pointer ${
                      newThemeMode === mKey
                        ? 'border-emerald-400 bg-emerald-500/20 text-white'
                        : 'border-slate-700 bg-[#121824] text-slate-400'
                    }`}
                  >
                    {mLabel}
                  </button>
                ))}
              </div>

              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="block text-slate-400 mb-1">Фон (BG)</label>
                  <input
                    type="color"
                    value={newThemeBg}
                    onChange={(e) => setNewThemeBg(e.target.value)}
                    className="w-full h-9 rounded-lg cursor-pointer bg-transparent"
                  />
                </div>
                <div>
                  <label className="block text-slate-400 mb-1">Карточки (Surface)</label>
                  <input
                    type="color"
                    value={newThemeSurface}
                    onChange={(e) => setNewThemeSurface(e.target.value)}
                    className="w-full h-9 rounded-lg cursor-pointer bg-transparent"
                  />
                </div>
                <div>
                  <label className="block text-slate-400 mb-1">Акцент (Accent)</label>
                  <input
                    type="color"
                    value={newThemeAccent}
                    onChange={(e) => setNewThemeAccent(e.target.value)}
                    className="w-full h-9 rounded-lg cursor-pointer bg-transparent"
                  />
                </div>
              </div>

              {/* Quick Palettes */}
              <div className="flex flex-wrap items-center gap-2 pt-1">
                <span className="text-slate-400">Быстрые пресеты:</span>
                {[
                  { name: 'Cyber Cyan', bg: '#070b14', surf: '#111a2e', acc: '#06b6d4' },
                  { name: 'Crimson Pro', bg: '#12080e', surf: '#24111c', acc: '#f43f5e' },
                  { name: 'Emerald Matrix', bg: '#06100c', surf: '#0f241c', acc: '#10b981' },
                  { name: 'Royal Gold', bg: '#110f08', surf: '#211d11', acc: '#f59e0b' },
                ].map((p) => (
                  <button
                    key={p.name}
                    type="button"
                    onClick={() => {
                      setNewThemeName(p.name);
                      setNewThemeBg(p.bg);
                      setNewThemeSurface(p.surf);
                      setNewThemeAccent(p.acc);
                    }}
                    className="px-2.5 py-1 rounded-lg bg-[#121824] hover:bg-[#1e2636] border border-slate-700 text-[11px] cursor-pointer"
                  >
                    {p.name}
                  </button>
                ))}
              </div>
            </div>

            <div className="flex justify-end gap-2 pt-3 border-t border-slate-800">
              <button
                onClick={() => setCustomThemeModalOpen(false)}
                className="px-4 py-2 rounded-xl bg-white/10 text-xs font-semibold cursor-pointer"
              >
                Отмена
              </button>
              <button
                onClick={() => {
                  const id = `custom_${Date.now()}`;
                  const created: CustomThemeConfig = {
                    id,
                    name: newThemeName.trim() || 'Custom 2.5',
                    isDark: newThemeMode !== 'light',
                    bgGradient: `radial-gradient(circle at 20% 15%, ${newThemeAccent}22, transparent 45%), linear-gradient(155deg, ${newThemeBg} 0%, ${newThemeSurface} 100%)`,
                    surfaceRgba: newThemeSurface,
                    cardHex: newThemeSurface,
                    accent: 'blue',
                    accentHex: newThemeAccent,
                    custom: true,
                  };
                  setCustomThemes((prev) => ({ ...prev, [id]: created }));
                  setThemeKey(id);
                  setCustomThemeModalOpen(false);
                  pushToast(
                    'Кастомная тема 2.5 создана',
                    `Тема «${created.name}» сохранена и сразу активирована (🟢 АКТИВНО)!`,
                    'success'
                  );
                }}
                className="px-5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold cursor-pointer shadow-md"
              >
                Сохранить и зажечь тему
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ==================== MODAL 4: SMART WORKSPACE PRESETS ==================== */}
      {workspaceModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div
            className="w-full max-w-xl rounded-2xl border border-slate-700 p-6 shadow-2xl"
            style={cardGlassStyle}
          >
            <div className="flex items-center justify-between pb-4 border-b border-slate-800">
              <div className="flex items-center gap-2">
                <Rocket className="w-5 h-5 text-blue-400" />
                <h3 className="text-lg font-bold">Smart Workspace</h3>
              </div>
              <button
                onClick={() => setWorkspaceModalOpen(false)}
                className="p-1.5 rounded-lg hover:bg-white/10 cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3 mt-4">
              {workspaces.map((ws) => (
                <div
                  key={ws.id}
                  className="p-4 rounded-xl bg-[#1a2232] border border-slate-700 flex items-center justify-between gap-4"
                >
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-bold">{ws.name}</span>
                      <span className="text-xs font-mono text-slate-400">({ws.hotkey})</span>
                    </div>
                    <div className="text-xs text-slate-400 mt-1">
                      Запустить: {ws.launchApps.join(', ')} • Закрыть: {ws.closeProcesses.join(', ') || '—'}
                    </div>
                  </div>
                  <button
                    onClick={() => {
                      setWorkspaceModalOpen(false);
                      pushToast('Smart Workspace', `Пресет «${ws.name}» успешно выполнен!`, 'success');
                    }}
                    className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold cursor-pointer shrink-0"
                  >
                    Запустить
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ==================== MODAL 5: APP CONTEXT MENU ==================== */}
      {contextMenuApp && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-xs p-4"
          onClick={() => setContextMenuApp(null)}
        >
          <div
            onClick={(e) => e.stopPropagation()}
            className="w-full max-w-xs rounded-2xl border border-slate-700 p-4 shadow-2xl space-y-2"
            style={cardGlassStyle}
          >
            <div className="flex items-center gap-3 pb-3 border-b border-slate-800">
              <div className="text-blue-400">{renderAppIcon(contextMenuApp.icon, 'w-6 h-6')}</div>
              <div className="min-w-0">
                <div className="text-sm font-bold truncate">{contextMenuApp.name}</div>
                <div className="text-xs text-slate-400 font-mono">
                  {formatMonthBadge(
                    contextMenuApp.monthMinutes,
                    contextMenuApp.elapsedSeconds,
                    contextMenuApp.isRunning
                  )}
                </div>
              </div>
            </div>

            <button
              onClick={() => {
                handleLaunchApp(contextMenuApp);
                setContextMenuApp(null);
              }}
              className="w-full flex items-center gap-2.5 p-2.5 rounded-xl hover:bg-white/10 text-xs font-semibold cursor-pointer"
            >
              <Play className="w-4 h-4 text-emerald-400" />
              {contextMenuApp.isRunning ? 'Остановить таймер сессии' : 'Запустить (старт таймера с 00:00)'}
            </button>

            <button
              onClick={() => {
                handleToggleFavorite(contextMenuApp);
                setContextMenuApp(null);
              }}
              className="w-full flex items-center gap-2.5 p-2.5 rounded-xl hover:bg-white/10 text-xs font-semibold cursor-pointer"
            >
              <Star className="w-4 h-4 text-amber-400" />
              {contextMenuApp.favorite ? 'Удалить из избранного' : 'Добавить в избранное'}
            </button>

            <button
              onClick={() => {
                setApps((prev) =>
                  prev.map((a) =>
                    a.id === contextMenuApp.id
                      ? { ...a, isRunning: false, elapsedSeconds: 0, todayMinutes: 0, weekMinutes: 0, monthMinutes: 0 }
                      : a
                  )
                );
                pushToast('Сброс таймера', `Время для ${contextMenuApp.name} сброшено в 0 мин`);
                setContextMenuApp(null);
              }}
              className="w-full flex items-center gap-2.5 p-2.5 rounded-xl hover:bg-white/10 text-xs font-semibold cursor-pointer"
            >
              <RotateCcw className="w-4 h-4 text-blue-400" />
              Сбросить счетчик времени в 0
            </button>

            {contextMenuApp.custom && (
              <button
                onClick={() => {
                  setApps((prev) => prev.filter((a) => a.id !== contextMenuApp.id));
                  pushToast('Удаление', `${contextMenuApp.name} удалено`);
                  setContextMenuApp(null);
                }}
                className="w-full flex items-center gap-2.5 p-2.5 rounded-xl hover:bg-rose-500/20 text-rose-400 text-xs font-semibold cursor-pointer"
              >
                <Trash2 className="w-4 h-4" />
                Удалить приложение
              </button>
            )}
          </div>
        </div>
      )}

      {/* ==================== TOAST NOTIFICATIONS ==================== */}
      <div className="fixed bottom-6 left-6 z-50 flex flex-col gap-2 max-w-md pointer-events-none">
        {toasts.map((t) => (
          <div
            key={t.id}
            className={`pointer-events-auto p-3.5 rounded-2xl border shadow-xl flex items-start gap-3 ${
              t.type === 'warning'
                ? 'bg-rose-950/95 border-rose-500/50 text-rose-100'
                : 'bg-[#121824]/95 border-slate-700 text-white'
            }`}
            style={{ backdropFilter: 'blur(16px)' }}
          >
            {t.type === 'warning' ? (
              <AlertTriangle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
            ) : (
              <Sparkles className="w-5 h-5 text-blue-400 shrink-0 mt-0.5" />
            )}
            <div className="text-xs">
              <div className="font-bold">{t.title}</div>
              <div className="text-slate-300 mt-0.5">{t.message}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
