/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useMemo, useRef } from 'react';
import {
  Rocket,
  Search,
  Filter,
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
  RefreshCw,
  Copy,
  FileCode,
  Sparkles,
  PlayCircle,
  PauseCircle,
  ShieldAlert,
  Sliders,
  History,
  LayoutGrid,
} from 'lucide-react';
import {
  AppItem,
  AppType,
  ClockStyleKey,
  CLOCK_STYLE_OPTIONS,
  DetoxGroup,
  formatDurationRu,
  formatMonthBadge,
  GlassIntensity,
  INITIAL_APPS,
  INITIAL_DETOX_GROUPS,
  INITIAL_PLUGINS,
  INITIAL_WORKSPACES,
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
};

const ICON_NAMES = Object.keys(ICON_MAP);
const WEEKDAYS_RU = ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'];

interface ToastMessage {
  id: string;
  title: string;
  message: string;
  type?: 'info' | 'warning' | 'success';
}

export default function App() {
  // --- Core Theme & Glassmorphism State ---
  const [themeKey, setThemeKey] = useState<ThemeKey>('dark');
  const [glassEnabled, setGlassEnabled] = useState<boolean>(true);
  const [glassIntensity, setGlassIntensity] = useState<GlassIntensity>('medium');
  const [glassOpacity, setGlassOpacity] = useState<number>(58);
  const [smoothAnimations, setSmoothAnimations] = useState<boolean>(true);

  // --- Clock Styles State (v2.4) ---
  const [clockStyle, setClockStyle] = useState<ClockStyleKey>('standard');
  const [timeFormat, setTimeFormat] = useState<'24' | '12'>('24');
  const [showSeconds, setShowSeconds] = useState<boolean>(true);
  const [showDate, setShowDate] = useState<boolean>(true);
  const [showWeekday, setShowWeekday] = useState<boolean>(true);
  const [clockGlassFrame, setClockGlassFrame] = useState<boolean>(true);
  const [timeColor, setTimeColor] = useState<string>('#f8fafc');
  const [dateColor, setDateColor] = useState<string>('#94a3b8');
  const [timeFontSize, setTimeFontSize] = useState<number>(20);
  const [now, setNow] = useState<Date>(new Date());

  // --- Navigation & Section Transition State ---
  const [activeSection, setActiveSection] = useState<'apps' | 'tracker' | 'python_code'>('apps');
  const [sectionAnimating, setSectionAnimating] = useState<boolean>(false);
  const [currentFilter, setCurrentFilter] = useState<'all' | 'web' | 'app' | 'system' | 'custom'>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');

  // --- Apps, Session Tracker & Detox Groups ---
  const [apps, setApps] = useState<AppItem[]>(INITIAL_APPS);
  const [detoxGroups, setDetoxGroups] = useState<DetoxGroup[]>(INITIAL_DETOX_GROUPS);
  const [trackerPeriod, setTrackerPeriod] = useState<'day' | 'week' | 'month'>('month');
  const [plugins, setPlugins] = useState<PluginItem[]>(INITIAL_PLUGINS);
  const [workspaces, setWorkspaces] = useState<WorkspacePreset[]>(INITIAL_WORKSPACES);

  // --- Background System Audio Controller State ---
  const [volume, setVolume] = useState<number>(68);
  const [isMuted, setIsMuted] = useState<boolean>(false);
  const [volumePopupOpen, setVolumePopupOpen] = useState<boolean>(false);
  const [audioBgStatus, setAudioBgStatus] = useState<string>('CoreAudio Worker Ready');
  const audioCtxRef = useRef<AudioContext | null>(null);

  // --- Floating HUD & Modals ---
  const [floatingHudVisible, setFloatingHudVisible] = useState<boolean>(false);
  const [cpuLoad, setCpuLoad] = useState<number>(18);
  const [ramLoad, setRamLoad] = useState<number>(44);

  const [addAppModalOpen, setAddAppModalOpen] = useState<boolean>(false);
  const [settingsModalOpen, setSettingsModalOpen] = useState<boolean>(false);
  const [settingsTab, setSettingsTab] = useState<'appearance' | 'clock' | 'plugins' | 'system' | 'changelog'>('appearance');
  const [pluginsModalOpen, setPluginsModalOpen] = useState<boolean>(false);
  const [workspaceModalOpen, setWorkspaceModalOpen] = useState<boolean>(false);
  const [contextMenuApp, setContextMenuApp] = useState<AppItem | null>(null);
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

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

  // --- Python Source Code Viewer State ---
  const [selectedPyFile, setSelectedPyFile] = useState<string>(PYTHON_PROJECT_FILES[0].path);
  const [pyFileContent, setPyFileContent] = useState<string>('Загрузка исходного кода Python...');
  const [copiedCode, setCopiedCode] = useState<boolean>(false);

  const currentTheme = THEMES[themeKey];
  const sessionTrackerEnabled = useMemo(
    () => plugins.find((p) => p.id === 'session_tracker_plugin')?.enabled ?? true,
    [plugins]
  );

  // Sync dark class on <html>
  useEffect(() => {
    const html = document.documentElement;
    if (currentTheme.isDark) {
      html.classList.add('dark');
    } else {
      html.classList.remove('dark');
    }
  }, [currentTheme.isDark]);

  // Real-time clock & HUD telemetry ticker
  useEffect(() => {
    const timer = setInterval(() => {
      setNow(new Date());
      setCpuLoad((prev) => Math.max(8, Math.min(65, prev + Math.floor(Math.random() * 7) - 3)));
    }, 1000);
    return () => clearInterval(timer);
  }, []);

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
    }, 4200);
  };

  // Smooth section transition helper
  const handleSwitchSection = (target: 'apps' | 'tracker' | 'python_code') => {
    if (target === activeSection) return;
    if (smoothAnimations) {
      setSectionAnimating(true);
      setTimeout(() => {
        setActiveSection(target);
        setSectionAnimating(false);
      }, 140);
    } else {
      setActiveSection(target);
    }
  };

  // Background audio volume handler with subtle WebAudio gain sync
  const handleVolumeChange = (newVol: number) => {
    const clamped = Math.max(0, Math.min(100, newVol));
    setVolume(clamped);
    if (clamped > 0 && isMuted) setIsMuted(false);
    setAudioBgStatus(`pycaw SetMasterVolumeScalar(${(clamped / 100).toFixed(2)}) [Daemon Thread]`);
    try {
      if (!audioCtxRef.current && typeof window !== 'undefined') {
        const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
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
    pushToast('Системный звук', nextMute ? 'Звук системы приглушен (Mute) в фоновом режиме' : `Громкость системы: ${volume}%`);
  };

  // Check detox limits and notify if exceeded
  const checkDetoxLimits = (updatedApp: AppItem, allUpdatedApps: AppItem[]) => {
    if (updatedApp.dailyLimitMinutes > 0 && updatedApp.todayMinutes >= updatedApp.dailyLimitMinutes) {
      pushToast(
        `⚠️ Превышен лимит: ${updatedApp.name}`,
        `Вы провели в ${updatedApp.name} уже ${formatDurationRu(updatedApp.todayMinutes)} сегодня (дневной лимит: ${formatDurationRu(updatedApp.dailyLimitMinutes)}).`,
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
          `Дневной лимит группы «${groupCfg.name}» превышен (${formatDurationRu(groupTotal)} из ${formatDurationRu(groupCfg.dailyLimitMinutes)}). Рекомендуем сделать перерыв!`,
          'warning'
        );
      }
    }
  };

  // Launch or toggle running state for an app
  const handleLaunchApp = (app: AppItem) => {
    setApps((prev) => {
      const next = prev.map((item) => {
        if (item.id !== app.id) return item;
        const addedMin = 15;
        const updated: AppItem = {
          ...item,
          isRunning: true,
          todayMinutes: item.todayMinutes + addedMin,
          weekMinutes: item.weekMinutes + addedMin,
          monthMinutes: item.monthMinutes + addedMin,
        };
        setTimeout(() => checkDetoxLimits(updated, prev), 80);
        return updated;
      });
      return next;
    });
    pushToast(
      `Запуск ${app.name}`,
      sessionTrackerEnabled
        ? `${app.name} запущено • Session Tracker ведет учет времени в фоне`
        : `${app.name} (${app.url}) запущено`,
      'success'
    );
  };

  const handleAddSessionMinutes = (appId: string, minutesToAdd: number) => {
    setApps((prev) => {
      let targetUpdated: AppItem | null = null;
      const next = prev.map((item) => {
        if (item.id !== appId) return item;
        targetUpdated = {
          ...item,
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
    const detectedType: AppType = newAppUrl.trim().toLowerCase().startsWith('http')
      ? 'web'
      : newAppType;

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
      monthMinutes: 60,
      weekMinutes: 30,
      todayMinutes: 15,
      dailyLimitMinutes: Number(newAppLimit) || 120,
      detoxGroup: newAppCategory === 'Games' ? 'Игры' : newAppCategory === 'Social' ? 'Соцсети и мессенджеры' : 'Браузеры',
    };

    setApps((prev) => [created, ...prev]);
    setNewAppName('');
    setNewAppUrl('');
    setNewAppArgs('');
    setAddAppModalOpen(false);
    pushToast('Приложение добавлено', `«${cleanName}» добавлено в библиотеку и подключено к Session Tracker`, 'success');
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
      description: 'Пользовательское расширение, сгенерированное через Plugin SDK 2.4.',
      enabled: true,
      file: `plugins/${slug}.py`,
      hooks: ['on_load', 'on_app_launched', 'get_ui_component'],
    };
    setPlugins((prev) => [newPlugin, ...prev]);
    setNewPluginSlug('');
    setNewPluginTitle('');
    pushToast('Plugin SDK 2.4', `Шаблон плагина «${title}» (plugins/${slug}.py) создан и активирован!`, 'success');
  };

  // Filtered apps
  const filteredApps = useMemo(() => {
    return apps.filter((app) => {
      if (currentFilter === 'web' && app.type !== 'web') return false;
      if (currentFilter === 'app' && app.type !== 'app') return false;
      if (currentFilter === 'system' && app.type !== 'system') return false;
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
  }, [apps, currentFilter, searchQuery]);

  const favoriteApps = useMemo(() => apps.filter((a) => a.favorite), [apps]);

  const categoriesMap = useMemo(() => {
    const map: Record<string, AppItem[]> = {};
    for (const app of filteredApps) {
      if (!map[app.category]) map[app.category] = [];
      map[app.category].push(app);
    }
    return map;
  }, [filteredApps]);

  // Formatted clock strings according to v2.4 settings
  const formattedClock = useMemo(() => {
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

    if (clockStyle === 'stacked') {
      return { time: `${hrs}\n${mins}`, date: fullDate, isStacked: true };
    }
    if (clockStyle === 'minimal' || clockStyle === 'pill_glass') {
      return { time: `${hrs}:${mins}${ampm}`, date: fullDate, isStacked: false };
    }
    if (clockStyle === 'cyber_mono') {
      return {
        time: showSeconds ? `[ ${hrs} : ${mins} : ${secs} ]` : `[ ${hrs} : ${mins} ]`,
        date: fullDate,
        isStacked: false,
      };
    }
    if (clockStyle === 'compact_badge') {
      return {
        time: `${weekday} • ${hrs}:${mins}`,
        date: dateBase,
        isStacked: false,
      };
    }
    return {
      time: showSeconds ? `${hrs}:${mins}:${secs}${ampm}` : `${hrs}:${mins}${ampm}`,
      date: fullDate,
      isStacked: false,
    };
  }, [now, clockStyle, timeFormat, showSeconds, showWeekday]);

  // Glassmorphism dynamic CSS styles
  const blurPx = glassEnabled
    ? glassIntensity === 'light'
      ? 'blur(8px)'
      : glassIntensity === 'medium'
      ? 'blur(16px)'
      : 'blur(28px)'
    : 'none';

  const cardGlassStyle: React.CSSProperties = {
    backgroundColor: glassEnabled
      ? currentTheme.isDark
        ? `rgba(32, 37, 50, ${(glassOpacity / 100).toFixed(2)})`
        : `rgba(255, 255, 255, ${(Math.max(55, glassOpacity) / 100).toFixed(2)})`
      : currentTheme.isDark
      ? '#222630'
      : '#ffffff',
    backdropFilter: blurPx,
    WebkitBackdropFilter: blurPx,
  };

  const renderAppIcon = (iconName: string, className = 'w-8 h-8') => {
    const IconComponent = ICON_MAP[iconName] || Rocket;
    return <IconComponent className={className} />;
  };

  return (
    <div
      className={`min-h-screen w-full flex flex-col select-none transition-colors duration-300 ${
        currentTheme.isDark ? 'text-slate-100' : 'text-slate-900'
      }`}
      style={{ background: currentTheme.bgGradient }}
    >
      {/* ==================== TOP HEADER (Flet Header 2.4) ==================== */}
      <header
        className={`sticky top-0 z-30 flex items-center justify-between gap-4 px-5 py-2.5 border-b transition-all ${
          currentTheme.isDark ? 'border-white/10' : 'border-slate-300/80'
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
              Launcher Hab 2.4
            </span>
          </div>

          {/* Section Switcher with smooth transition */}
          <nav className="hidden md:flex items-center gap-1 p-1 rounded-xl bg-black/20 dark:bg-white/5 border border-white/10 ml-2">
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
              Game & App Session Tracker
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
              Python Код v2.4 (11 файлов)
            </button>
          </nav>
        </div>

        {/* Center/Right: System Devices + Customizable Clock + Audio + Plugins + Settings */}
        <div className="flex items-center gap-3 shrink-0">
          {/* Devices Monitor (Battery & Wi-Fi) */}
          <div className="hidden lg:flex items-center gap-3 px-3 py-1.5 rounded-xl bg-white/5 border border-white/10 text-xs">
            <div className="flex items-center gap-1.5 text-emerald-400">
              <BatteryCharging className="w-4 h-4" />
              <span className="font-mono tabular-nums">94%</span>
            </div>
            <span className="opacity-30">•</span>
            <div className="flex items-center gap-1.5 text-emerald-400">
              <Wifi className="w-4 h-4" />
              <span>Wi-Fi</span>
            </div>
          </div>

          {/* Customizable Clock Widget (6 Styles in v2.4) */}
          <button
            onClick={() => {
              setSettingsTab('clock');
              setSettingsModalOpen(true);
            }}
            title="Нажмите для изменения стиля часов (6 стилей в v2.4)"
            className={`px-3.5 py-1.5 rounded-xl transition-all cursor-pointer text-right ${
              clockGlassFrame
                ? 'bg-white/10 hover:bg-white/15 border border-white/15 shadow-sm'
                : 'hover:bg-white/5'
            }`}
          >
            {clockStyle === 'pill_glass' ? (
              <div className="flex items-center gap-2">
                <Clock className="w-3.5 h-3.5 text-blue-400" />
                <span
                  className="font-bold font-mono tabular-nums"
                  style={{ color: timeColor, fontSize: `${Math.max(13, timeFontSize - 4)}px` }}
                >
                  {formattedClock.time}
                </span>
                {showDate && (
                  <>
                    <span className="opacity-40">•</span>
                    <span className="text-xs font-mono tabular-nums" style={{ color: dateColor }}>
                      {formattedClock.date}
                    </span>
                  </>
                )}
              </div>
            ) : (
              <div className="flex flex-col items-center leading-tight">
                <span
                  className={`font-bold tabular-nums ${
                    clockStyle === 'cyber_mono' ? 'font-mono tracking-wider' : ''
                  } ${formattedClock.isStacked ? ' whitespace-pre-line text-center leading-none py-0.5' : ''}`}
                  style={{
                    color: timeColor,
                    fontSize: `${formattedClock.isStacked ? Math.min(24, timeFontSize) : Math.min(22, timeFontSize)}px`,
                  }}
                >
                  {formattedClock.time}
                </span>
                {showDate && (
                  <span
                    className="text-[11px] font-mono tabular-nums mt-0.5"
                    style={{ color: dateColor }}
                  >
                    {formattedClock.date}
                  </span>
                )}
              </div>
            )}
          </button>

          {/* Background System Audio Controller */}
          <div className="relative flex items-center gap-1.5">
            <button
              onClick={() => setVolumePopupOpen((v) => !v)}
              title="Управление системной громкостью (Фоновый контроллер v2.4)"
              className={`p-2 rounded-xl border transition-all cursor-pointer ${
                volumePopupOpen
                  ? 'bg-blue-500/20 border-blue-500/40 text-blue-400'
                  : 'bg-white/5 hover:bg-white/10 border-white/10'
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
                className="flex items-center gap-2.5 px-3 py-1.5 rounded-xl border border-white/15 shadow-lg animate-in fade-in duration-150"
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
                  className="w-28 accent-blue-500 cursor-pointer"
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
            title="Управление плагинами и расширениями (API 2.4)"
            className="p-2 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 transition-all cursor-pointer"
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
                : 'bg-white/5 hover:bg-white/10 border-white/10'
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
            title="Настройки Launcher Hab 2.4"
            className="p-2 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 transition-all cursor-pointer"
          >
            <Settings className="w-4 h-4" />
          </button>

          {/* Direct Download Python v2.4 ZIP */}
          <a
            href="/launcher_hab2.4.zip"
            download="launcher_hab2.4.zip"
            className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold shadow-sm transition-all whitespace-nowrap"
          >
            <Download className="w-3.5 h-3.5" />
            Скачать Python v2.4 (.zip)
          </a>
        </div>
      </header>

      {/* ==================== MAIN BODY (Sidebar + Animated Main Viewport) ==================== */}
      <div className="flex-1 flex overflow-hidden relative">
        {/* LEFT SIDEBAR (340px, matches Flet UIPanels.create_sidebar) */}
        <aside
          className={`w-80 lg:w-88 shrink-0 flex flex-col border-r transition-all ${
            currentTheme.isDark ? 'border-white/10' : 'border-slate-300/80'
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
              {apps.length} прил.
            </span>
          </div>

          {/* Search & Filter Row */}
          <div className="px-4 py-2 flex items-center gap-2">
            <div className="relative flex-1">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Поиск приложений..."
                className={`w-full pl-9 pr-7 py-2 rounded-xl text-xs border outline-none transition-all ${
                  currentTheme.isDark
                    ? 'bg-white/5 border-white/10 focus:border-blue-500/60 text-white placeholder:text-slate-500'
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

          {/* Filter Pills */}
          <div className="px-4 pb-2.5 flex items-center gap-1 overflow-x-auto">
            {(
              [
                ['all', 'Все'],
                ['app', 'EXE'],
                ['web', 'Web'],
                ['system', 'Система'],
                ['custom', 'Мои'],
              ] as const
            ).map(([key, label]) => (
              <button
                key={key}
                onClick={() => setCurrentFilter(key)}
                className={`px-2.5 py-1 rounded-lg text-[11px] font-medium transition-all cursor-pointer whitespace-nowrap ${
                  currentFilter === key
                    ? 'bg-blue-600 text-white'
                    : 'bg-white/5 hover:bg-white/10 text-slate-400'
                }`}
              >
                {label}
              </button>
            ))}
          </div>

          <div className="border-t border-white/10" />

          {/* Sidebar Apps List */}
          <div className="flex-1 overflow-y-auto p-3 space-y-1.5">
            {filteredApps.map((app) => {
              const badge = sessionTrackerEnabled ? formatMonthBadge(app.monthMinutes) : null;
              return (
                <div
                  key={app.id}
                  onClick={() => handleLaunchApp(app)}
                  className={`group flex items-center gap-3 p-2.5 rounded-xl border transition-all cursor-pointer ${
                    currentTheme.isDark
                      ? 'bg-white/[0.04] hover:bg-blue-500/15 border-white/[0.07] hover:border-blue-500/40'
                      : 'bg-white/60 hover:bg-blue-50 border-slate-200/80 hover:border-blue-400'
                  }`}
                >
                  <div
                    className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border ${
                      app.type === 'web'
                        ? 'text-blue-400 bg-blue-500/10 border-blue-500/20'
                        : 'text-slate-100 bg-white/5 border-white/10'
                    }`}
                  >
                    {renderAppIcon(app.icon, 'w-5 h-5')}
                  </div>

                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-1.5">
                      <p className="text-xs font-semibold truncate">{app.name}</p>
                      {app.isRunning && (
                        <span className="text-[10px] font-mono text-emerald-400">● Активно</span>
                      )}
                    </div>
                    <p className="text-[11px] text-slate-400 truncate font-mono tabular-nums">
                      {app.category} {badge ? `• ${badge}` : `• ${app.type.toUpperCase()}`}
                    </p>
                  </div>

                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setContextMenuApp(app);
                    }}
                    title="Меню приложения"
                    className="p-1.5 rounded-lg opacity-70 hover:opacity-100 hover:bg-white/10 transition-all cursor-pointer"
                  >
                    <MoreVertical className="w-4 h-4 text-slate-400" />
                  </button>
                </div>
              );
            })}
          </div>

          <div className="border-t border-white/10" />

          {/* Add App Button at Bottom of Sidebar */}
          <div className="p-3.5">
            <button
              onClick={() => setAddAppModalOpen(true)}
              className="w-full flex items-center gap-3 p-3 rounded-xl bg-blue-500/15 hover:bg-blue-500/25 border border-blue-500/35 transition-all cursor-pointer text-left"
            >
              <div className="w-10 h-10 rounded-xl bg-blue-500/25 flex items-center justify-center text-blue-400 shrink-0">
                <Plus className="w-5 h-5" />
              </div>
              <div className="min-w-0">
                <div className="text-xs font-bold">Добавить приложение</div>
                <div className="text-[11px] text-slate-400 truncate">
                  Единое окно v2.4 • Превью и лимит
                </div>
              </div>
            </button>
          </div>
        </aside>

        {/* ==================== MAIN CONTENT AREA (AnimatedSwitcher) ==================== */}
        <main className="flex-1 overflow-y-auto p-5 relative">
          <div
            className={`transition-all duration-200 ${
              sectionAnimating ? 'opacity-0 scale-[0.99] translate-y-1' : 'opacity-100 scale-100 translate-y-0'
            }`}
          >
            {/* -------------------- SECTION 1: APPS & FAVORITES -------------------- */}
            {activeSection === 'apps' && (
              <div className="space-y-5 max-w-6xl mx-auto">
                {/* Quick Info Strip for v2.4 */}
                <div
                  className="flex flex-wrap items-center justify-between gap-3 px-4 py-3 rounded-2xl border border-white/15 shadow-lg"
                  style={cardGlassStyle}
                >
                  <div className="flex items-center gap-3">
                    <Sparkles className="w-4 h-4 text-blue-400 shrink-0" />
                    <span className="text-xs font-medium">
                      <strong>Launcher Hab 2.4</strong> (Python + Flet): прозрачное стекло <code className="text-blue-400">ft.Blur</code>, фоновый звук <code className="text-blue-400">pycaw</code> и плагин <strong>Game &amp; App Session Tracker</strong>
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleSwitchSection('tracker')}
                      className="px-3 py-1.5 rounded-lg bg-blue-500/20 hover:bg-blue-500/30 border border-blue-500/30 text-blue-300 text-xs font-semibold transition-all cursor-pointer"
                    >
                      Открыть графики времени
                    </button>
                    <button
                      onClick={() => handleSwitchSection('python_code')}
                      className="px-3 py-1.5 rounded-lg bg-emerald-500/20 hover:bg-emerald-500/30 border border-emerald-500/30 text-emerald-300 text-xs font-semibold transition-all cursor-pointer"
                    >
                      Смотреть Python-код 2.4
                    </button>
                  </div>
                </div>

                {/* FAVORITES GLASS CARD */}
                <section
                  className="rounded-2xl border border-white/15 p-5 shadow-xl transition-all"
                  style={cardGlassStyle}
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2.5">
                      <Star className="w-5 h-5 text-amber-400 fill-amber-400" />
                      <h3 className="text-base font-bold">Избранное</h3>
                      <span className="text-xs text-slate-400 font-mono tabular-nums">
                        {favoriteApps.length}/10
                      </span>
                    </div>
                    <span className="text-xs text-slate-400">
                      Клик — запуск и учет сессии • ПКМ / меню — управление
                    </span>
                  </div>

                  {favoriteApps.length === 0 ? (
                    <div className="py-8 text-center text-slate-400 text-xs">
                      Добавьте приложения в избранное через меню карточки
                    </div>
                  ) : (
                    <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-6 gap-4">
                      {favoriteApps.map((app) => {
                        const monthBadge = sessionTrackerEnabled ? formatMonthBadge(app.monthMinutes) : null;
                        return (
                          <div
                            key={app.id}
                            onClick={() => handleLaunchApp(app)}
                            onContextMenu={(e) => {
                              e.preventDefault();
                              setContextMenuApp(app);
                            }}
                            className="group relative flex flex-col items-center p-3 rounded-2xl hover:scale-105 transition-all duration-200 cursor-pointer"
                          >
                            <div
                              className={`w-20 h-20 rounded-2xl flex items-center justify-center relative border shadow-md transition-all ${
                                app.isRunning
                                  ? 'border-emerald-400/70 bg-emerald-500/10 shadow-emerald-500/10'
                                  : 'border-white/15 bg-white/[0.07] group-hover:border-blue-400/50 group-hover:bg-blue-500/10'
                              }`}
                              style={{ backdropFilter: blurPx }}
                            >
                              <div className={app.type === 'web' ? 'text-blue-400' : 'text-white'}>
                                {renderAppIcon(app.icon, 'w-9 h-9')}
                              </div>
                              <div className="absolute bottom-1.5 right-1.5">
                                {app.isRunning ? (
                                  <PlayCircle className="w-4 h-4 text-emerald-400 fill-emerald-950" />
                                ) : (
                                  <Star className="w-3.5 h-3.5 text-amber-400 fill-amber-400" />
                                )}
                              </div>
                            </div>

                            <span className="mt-2 text-xs font-semibold text-center truncate w-full">
                              {app.name}
                            </span>
                            <span
                              className={`text-[11px] font-mono tabular-nums text-center truncate w-full ${
                                app.isRunning ? 'text-emerald-400 font-medium' : 'text-slate-400'
                              }`}
                            >
                              {monthBadge ? `${monthBadge}` : app.type.toUpperCase()}
                            </span>
                          </div>
                        );
                      })}
                    </div>
                  )}
                </section>

                {/* CATEGORY GLASS SECTIONS */}
                {Object.entries(categoriesMap).map(([category, catApps]) => (
                  <section
                    key={category}
                    className="rounded-2xl border border-white/15 p-5 shadow-xl transition-all"
                    style={cardGlassStyle}
                  >
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center gap-2.5">
                        <span className="w-2 h-5 rounded-full bg-blue-500" />
                        <h3 className="text-base font-bold">{category}</h3>
                        <span className="text-xs text-slate-400 font-mono tabular-nums">
                          · {catApps.length}
                        </span>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-6 gap-4">
                      {catApps.map((app) => {
                        const monthBadge = sessionTrackerEnabled ? formatMonthBadge(app.monthMinutes) : null;
                        return (
                          <div
                            key={app.id}
                            onClick={() => handleLaunchApp(app)}
                            onContextMenu={(e) => {
                              e.preventDefault();
                              setContextMenuApp(app);
                            }}
                            className="group relative flex flex-col items-center p-3 rounded-2xl hover:scale-105 transition-all duration-200 cursor-pointer"
                          >
                            <div
                              className={`w-20 h-20 rounded-2xl flex items-center justify-center relative border shadow-md transition-all ${
                                app.isRunning
                                  ? 'border-emerald-400/70 bg-emerald-500/10'
                                  : 'border-white/15 bg-white/[0.07] group-hover:border-blue-400/50 group-hover:bg-blue-500/10'
                              }`}
                              style={{ backdropFilter: blurPx }}
                            >
                              <div className={app.type === 'web' ? 'text-blue-400' : 'text-slate-100'}>
                                {renderAppIcon(app.icon, 'w-9 h-9')}
                              </div>
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  setContextMenuApp(app);
                                }}
                                className="absolute top-1.5 right-1.5 opacity-0 group-hover:opacity-100 p-1 rounded-lg bg-black/40 hover:bg-black/70 text-slate-200 transition-opacity cursor-pointer"
                              >
                                <MoreVertical className="w-3.5 h-3.5" />
                              </button>
                              <div className="absolute bottom-1.5 right-1.5">
                                {app.isRunning ? (
                                  <PlayCircle className="w-4 h-4 text-emerald-400" />
                                ) : (
                                  <Check className="w-3.5 h-3.5 text-emerald-400/80" />
                                )}
                              </div>
                            </div>

                            <span className="mt-2 text-xs font-semibold text-center truncate w-full">
                              {app.name}
                            </span>
                            <span className="text-[11px] font-mono tabular-nums text-slate-400 text-center truncate w-full">
                              {monthBadge ? `${monthBadge}` : app.type.toUpperCase()}
                            </span>
                          </div>
                        );
                      })}
                    </div>
                  </section>
                ))}
              </div>
            )}

            {/* -------------------- SECTION 2: GAME & APP SESSION TRACKER -------------------- */}
            {activeSection === 'tracker' && (
              <div className="space-y-5 max-w-6xl mx-auto">
                <section
                  className="rounded-2xl border border-white/15 p-6 shadow-xl"
                  style={cardGlassStyle}
                >
                  <div className="flex flex-wrap items-center justify-between gap-4 pb-5 border-b border-white/10">
                    <div>
                      <div className="flex items-center gap-2.5">
                        <BarChart3 className="w-6 h-6 text-blue-400" />
                        <h2 className="text-xl font-bold">
                          Game &amp; App Session Tracker (Трекер активности и игрового времени)
                        </h2>
                      </div>
                      <p className="text-xs text-slate-400 mt-1">
                        Аналог статистики Steam и «Экранного времени»: учет часов по каждому приложению, графики за день/неделю/месяц и лимиты цифрового детокса.
                      </p>
                    </div>

                    {/* Period Selector: День | Неделя | Месяц */}
                    <div className="flex items-center gap-1 p-1 rounded-xl bg-black/25 border border-white/10">
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

                  {/* Top Summary Metrics */}
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 my-5">
                    <div className="p-4 rounded-xl bg-white/5 border border-white/10">
                      <span className="text-xs text-slate-400">Всего времени за выбранный период</span>
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
                          )
                        )}
                      </div>
                      <span className="text-[11px] text-slate-400">
                        Отслеживается {apps.length} приложений в фоне
                      </span>
                    </div>

                    <div className="p-4 rounded-xl bg-white/5 border border-white/10">
                      <span className="text-xs text-slate-400">Лидер активности (Steam / Игры)</span>
                      <div className="text-2xl font-bold font-mono tabular-nums mt-1 text-emerald-400">
                        Steam — {formatMonthBadge(apps.find((a) => a.id === 'steam')?.monthMinutes || 2520)}
                      </div>
                      <span className="text-[11px] text-slate-400">
                        Отображается на карточке приложения
                      </span>
                    </div>

                    <div className="p-4 rounded-xl bg-white/5 border border-white/10">
                      <span className="text-xs text-slate-400">Статус цифрового детокса</span>
                      <div className="text-2xl font-bold font-mono tabular-nums mt-1 text-amber-400">
                        {detoxGroups.filter((g) => g.enabled).length} активных групп
                      </div>
                      <span className="text-[11px] text-slate-400">
                        Авто-уведомления при превышении лимита
                      </span>
                    </div>
                  </div>

                  {/* Per-Application Activity Bars */}
                  <div className="space-y-3">
                    <h3 className="text-sm font-bold text-slate-300">
                      Рейтинг приложений по проведенному времени ({trackerPeriod === 'day' ? 'Сегодня' : trackerPeriod === 'week' ? 'За 7 дней' : 'За 30 дней'})
                    </h3>

                    {[...apps]
                      .sort((a, b) => {
                        const va = trackerPeriod === 'day' ? a.todayMinutes : trackerPeriod === 'week' ? a.weekMinutes : a.monthMinutes;
                        const vb = trackerPeriod === 'day' ? b.todayMinutes : trackerPeriod === 'week' ? b.weekMinutes : b.monthMinutes;
                        return vb - va;
                      })
                      .slice(0, 8)
                      .map((app) => {
                        const val =
                          trackerPeriod === 'day'
                            ? app.todayMinutes
                            : trackerPeriod === 'week'
                            ? app.weekMinutes
                            : app.monthMinutes;
                        const maxVal = trackerPeriod === 'day' ? 240 : trackerPeriod === 'week' ? 1000 : 3000;
                        const percent = Math.min(100, Math.round((val / maxVal) * 100));
                        const isOverDailyLimit = app.todayMinutes >= app.dailyLimitMinutes;

                        return (
                          <div
                            key={app.id}
                            className="p-3.5 rounded-xl bg-white/[0.04] border border-white/10 flex flex-col gap-2"
                          >
                            <div className="flex flex-wrap items-center justify-between gap-2">
                              <div className="flex items-center gap-2.5">
                                <div className="text-blue-400">{renderAppIcon(app.icon, 'w-5 h-5')}</div>
                                <span className="text-sm font-bold">
                                  {app.name} —{' '}
                                  <span className="font-mono tabular-nums text-blue-400">
                                    {trackerPeriod === 'month' ? formatMonthBadge(val) : formatDurationRu(val)}
                                  </span>
                                </span>
                                <span className="text-xs text-slate-400">
                                  · Группа детокса: {app.detoxGroup}
                                </span>
                              </div>

                              <div className="flex items-center gap-2">
                                <span
                                  className={`text-xs font-mono tabular-nums ${
                                    isOverDailyLimit ? 'text-rose-400 font-semibold' : 'text-slate-400'
                                  }`}
                                >
                                  Сегодня: {formatDurationRu(app.todayMinutes)} / Лимит: {formatDurationRu(app.dailyLimitMinutes)}
                                </span>
                                <button
                                  onClick={() => handleAddSessionMinutes(app.id, 30)}
                                  title="Симулировать +30 мин активности (проверка уведомления детокса)"
                                  className="px-2.5 py-1 rounded-lg bg-blue-500/20 hover:bg-blue-500/30 border border-blue-500/30 text-blue-300 text-xs font-mono cursor-pointer transition-all"
                                >
                                  +30 мин
                                </button>
                              </div>
                            </div>

                            <div className="w-full h-2 rounded-full bg-black/40 overflow-hidden">
                              <div
                                className={`h-full rounded-full transition-all duration-500 ${
                                  isOverDailyLimit ? 'bg-rose-500' : 'bg-blue-500'
                                }`}
                                style={{ width: `${percent}%` }}
                              />
                            </div>
                          </div>
                        );
                      })}
                  </div>
                </section>

                {/* Digital Detox Groups Configuration */}
                <section
                  className="rounded-2xl border border-white/15 p-6 shadow-xl"
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
                              : 'bg-white/5 border-white/10'
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
                  className="rounded-2xl border border-white/15 p-6 shadow-xl"
                  style={cardGlassStyle}
                >
                  <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-white/10">
                    <div>
                      <div className="flex items-center gap-2">
                        <FileCode className="w-5 h-5 text-emerald-400" />
                        <h2 className="text-lg font-bold">
                          Исходный код Python — Launcher Hab 2.4 (Flet)
                        </h2>
                      </div>
                      <p className="text-xs text-slate-400 mt-1">
                        Все изменения написаны на языке Python с сохранением архитектуры проекта. Вы можете просмотреть каждый обновленный модуль или скачать готовый архив <code className="text-emerald-400">launcher_hab2.4.zip</code>.
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
                                ? 'bg-blue-600/20 border-blue-500/50 text-white'
                                : 'bg-white/5 hover:bg-white/10 border-white/10 text-slate-300'
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
                    <div className="lg:col-span-8 flex flex-col rounded-xl bg-[#0d1017] border border-white/10 overflow-hidden">
                      <div className="px-4 py-2.5 bg-white/5 border-b border-white/10 flex items-center justify-between text-xs font-mono text-slate-300">
                        <span>launcher_hab2.4/{selectedPyFile}</span>
                        <span className="text-slate-400">Python 3.11 • Flet 0.24.1</span>
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
              className="fixed right-6 top-20 z-20 p-4 rounded-2xl border border-white/20 shadow-2xl w-52 animate-in fade-in duration-200"
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
                  <span className="text-slate-400">Избранных:</span>
                  <span>{favoriteApps.length}/10</span>
                </div>
              </div>
            </div>
          )}

          {/* FIXED RECYCLE BIN FAB (Bottom Right) */}
          <button
            onClick={() => pushToast('Корзина', 'Открыта системная корзина (RecycleBinFolder)')}
            title="Открыть корзину"
            className="fixed right-6 bottom-6 z-20 p-3.5 rounded-2xl border border-white/20 shadow-xl hover:scale-105 transition-all cursor-pointer"
            style={cardGlassStyle}
          >
            <Trash2 className="w-5 h-5" />
          </button>
        </main>
      </div>

      {/* ==================== MODAL 1: IMPROVED ADD APPLICATION (v2.4) ==================== */}
      {addAppModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/65 backdrop-blur-sm p-4">
          <div
            className="w-full max-w-2xl rounded-2xl border border-white/20 p-6 shadow-2xl max-h-[90vh] overflow-y-auto"
            style={cardGlassStyle}
          >
            <div className="flex items-center justify-between pb-4 border-b border-white/10">
              <div className="flex items-center gap-2.5">
                <Plus className="w-5 h-5 text-blue-400" />
                <h3 className="text-lg font-bold">Добавить приложение (Единое окно v2.4)</h3>
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
              <div className="p-4 rounded-2xl bg-white/5 border border-white/15 flex items-center gap-4">
                <div className="w-16 h-16 rounded-2xl bg-blue-500/15 border border-blue-500/35 flex items-center justify-center text-blue-400 shrink-0">
                  {renderAppIcon(newAppIcon, 'w-8 h-8')}
                </div>
                <div className="min-w-0 flex-1">
                  <div className="text-[10px] font-mono uppercase tracking-wider text-blue-400 font-bold">
                    Предпросмотр стеклянной карточки
                  </div>
                  <div className="text-sm font-bold truncate mt-0.5">
                    {newAppName.trim() || 'Новое приложение'}
                  </div>
                  <div className="text-xs text-slate-400 font-mono tabular-nums mt-0.5">
                    {newAppCategory} • {newAppUrl.toLowerCase().startsWith('http') ? 'WEB' : newAppType.toUpperCase()} • Лимит детокса: {newAppLimit} мин/день
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div className="sm:col-span-1">
                  <label className="text-xs text-slate-300 block mb-1">Название *</label>
                  <input
                    type="text"
                    required
                    value={newAppName}
                    onChange={(e) => setNewAppName(e.target.value)}
                    placeholder="Cyberpunk 2077 / VS Code"
                    className="w-full px-3 py-2 rounded-xl bg-white/5 border border-white/15 text-xs outline-none focus:border-blue-500"
                  />
                </div>

                <div>
                  <label className="text-xs text-slate-300 block mb-1">Категория</label>
                  <select
                    value={newAppCategory}
                    onChange={(e) => setNewAppCategory(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-[#1e2330] border border-white/15 text-xs outline-none"
                  >
                    <option value="Games">Games</option>
                    <option value="Browser">Browser</option>
                    <option value="Media">Media</option>
                    <option value="Music">Music</option>
                    <option value="Social">Social</option>
                    <option value="Office">Office</option>
                    <option value="System">System</option>
                    <option value="Custom">Custom</option>
                  </select>
                </div>

                <div>
                  <label className="text-xs text-slate-300 block mb-1">Тип запуска</label>
                  <select
                    value={newAppType}
                    onChange={(e) => setNewAppType(e.target.value as AppType)}
                    className="w-full px-3 py-2 rounded-xl bg-[#1e2330] border border-white/15 text-xs outline-none"
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
                    className="w-full px-3 py-2 rounded-xl bg-white/5 border border-white/15 text-xs outline-none focus:border-blue-500 font-mono"
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
                    className="w-full px-3 py-2 rounded-xl bg-white/5 border border-white/15 text-xs outline-none font-mono tabular-nums"
                  />
                </div>
              </div>

              <div>
                <label className="text-xs text-slate-300 block mb-1">Аргументы командной строки (CLI параметры)</label>
                <input
                  type="text"
                  value={newAppArgs}
                  onChange={(e) => setNewAppArgs(e.target.value)}
                  placeholder="--fullscreen -novid"
                  className="w-full px-3 py-2 rounded-xl bg-white/5 border border-white/15 text-xs outline-none font-mono"
                />
              </div>

              <div className="flex items-center gap-4">
                <label className="flex items-center gap-2 text-xs cursor-pointer">
                  <input
                    type="checkbox"
                    checked={newAppFav}
                    onChange={(e) => setNewAppFav(e.target.checked)}
                    className="accent-blue-500"
                  />
                  Добавить сразу в Избранное
                </label>
              </div>

              {/* Icon Picker with Search */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-semibold">Выбор иконки</span>
                  <input
                    type="text"
                    value={newAppIconSearch}
                    onChange={(e) => setNewAppIconSearch(e.target.value)}
                    placeholder="Поиск иконки..."
                    className="px-2.5 py-1 rounded-lg bg-white/5 border border-white/10 text-xs outline-none"
                  />
                </div>
                <div className="grid grid-cols-7 sm:grid-cols-10 gap-2 p-2.5 rounded-xl bg-black/20 border border-white/10 max-h-36 overflow-y-auto">
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
                          : 'bg-white/5 border-transparent hover:bg-white/10 text-slate-300'
                      }`}
                    >
                      {renderAppIcon(iconKey, 'w-5 h-5')}
                    </button>
                  ))}
                </div>
              </div>

              <div className="flex items-center justify-end gap-2 pt-3 border-t border-white/10">
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

      {/* ==================== MODAL 2: PLUGIN MANAGER & SDK 2.4 ==================== */}
      {pluginsModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/65 backdrop-blur-sm p-4">
          <div
            className="w-full max-w-3xl rounded-2xl border border-white/20 p-6 shadow-2xl max-h-[90vh] overflow-y-auto"
            style={cardGlassStyle}
          >
            <div className="flex items-center justify-between pb-4 border-b border-white/10">
              <div className="flex items-center gap-2.5">
                <Puzzle className="w-5 h-5 text-blue-400" />
                <div>
                  <h3 className="text-lg font-bold">Платформа плагинов и расширений (Plugin API 2.4)</h3>
                  <p className="text-xs text-slate-400">
                    Поддержка хуков жизненного цикла on_load, on_app_launched, on_tick и бейджей карточек
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

            {/* Plugin SDK Template Generator */}
            <div className="my-4 p-4 rounded-xl bg-blue-500/10 border border-blue-500/25">
              <div className="flex items-center gap-2 text-xs font-bold text-blue-300 mb-2">
                <Code2 className="w-4 h-4" />
                Plugin SDK 2.4 — Быстрый генератор шаблона расширения (.py)
              </div>
              <div className="flex flex-col sm:flex-row gap-2">
                <input
                  type="text"
                  value={newPluginSlug}
                  onChange={(e) => setNewPluginSlug(e.target.value)}
                  placeholder="ID плагина (напр. steam_overlay_plugin)"
                  className="flex-1 px-3 py-2 rounded-xl bg-black/30 border border-white/15 text-xs font-mono outline-none"
                />
                <input
                  type="text"
                  value={newPluginTitle}
                  onChange={(e) => setNewPluginTitle(e.target.value)}
                  placeholder="Название расширения"
                  className="flex-1 px-3 py-2 rounded-xl bg-black/30 border border-white/15 text-xs outline-none"
                />
                <button
                  onClick={handleCreatePluginTemplate}
                  className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold cursor-pointer whitespace-nowrap"
                >
                  + Создать плагин
                </button>
              </div>
            </div>

            {/* Plugins List */}
            <div className="space-y-3">
              {plugins.map((plugin) => (
                <div
                  key={plugin.id}
                  className="p-4 rounded-xl bg-white/5 border border-white/10 flex flex-col gap-2"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-bold">{plugin.name}</span>
                        <span className="text-xs font-mono text-blue-400">v{plugin.version}</span>
                        <span className="text-xs font-mono text-slate-400">({plugin.file})</span>
                      </div>
                      <p className="text-xs text-slate-300 mt-1">{plugin.description}</p>
                      <div className="flex flex-wrap items-center gap-2 mt-2 text-[11px] font-mono text-slate-400">
                        <span>Hooks: {plugin.hooks.join(' · ')}</span>
                      </div>
                    </div>

                    <div className="flex items-center gap-2 shrink-0">
                      {plugin.id === 'session_tracker_plugin' && (
                        <button
                          onClick={() => {
                            setPluginsModalOpen(false);
                            handleSwitchSection('tracker');
                          }}
                          className="px-3 py-1.5 rounded-lg bg-blue-600/30 hover:bg-blue-600/50 border border-blue-400/40 text-xs font-semibold text-blue-200 cursor-pointer"
                        >
                          Открыть трекер
                        </button>
                      )}
                      <label className="flex items-center gap-1.5 text-xs cursor-pointer">
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
                              val ? 'Плагин включен и загружен в ядро' : 'Плагин выгружен'
                            );
                          }}
                          className="w-4 h-4 accent-blue-500 cursor-pointer"
                        />
                        <span>{plugin.enabled ? 'Активен' : 'Выкл'}</span>
                      </label>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ==================== MODAL 3: SETTINGS & CLOCK STYLES & CHANGELOG 2.4 ==================== */}
      {settingsModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/65 backdrop-blur-sm p-4">
          <div
            className="w-full max-w-3xl rounded-2xl border border-white/20 p-6 shadow-2xl max-h-[90vh] flex flex-col"
            style={cardGlassStyle}
          >
            <div className="flex items-center justify-between pb-4 border-b border-white/10">
              <div className="flex items-center gap-2.5">
                <Sliders className="w-5 h-5 text-blue-400" />
                <h3 className="text-lg font-bold">Настройки Launcher Hab 2.4</h3>
              </div>
              <button
                onClick={() => setSettingsModalOpen(false)}
                className="p-1.5 rounded-lg hover:bg-white/10 cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Settings Tabs */}
            <div className="flex items-center gap-1.5 py-3 border-b border-white/10 overflow-x-auto">
              {(
                [
                  ['appearance', 'Стекломорфизм и темы'],
                  ['clock', '🕒 Стили часов (v2.4)'],
                  ['system', '🔊 Звук и система'],
                  ['changelog', '📜 История версий (2.4)'],
                ] as const
              ).map(([tabKey, tabLabel]) => (
                <button
                  key={tabKey}
                  onClick={() => setSettingsTab(tabKey)}
                  className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all cursor-pointer whitespace-nowrap ${
                    settingsTab === tabKey
                      ? 'bg-blue-600 text-white'
                      : 'bg-white/5 hover:bg-white/10 text-slate-300'
                  }`}
                >
                  {tabLabel}
                </button>
              ))}
            </div>

            <div className="flex-1 overflow-y-auto py-4 space-y-5">
              {/* TAB 1: APPEARANCE & GLASSMORPHISM */}
              {settingsTab === 'appearance' && (
                <div className="space-y-5">
                  <div className="p-4 rounded-xl bg-white/5 border border-white/10 space-y-3">
                    <h4 className="text-sm font-bold">Тема оформления</h4>
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                      {(Object.keys(THEMES) as ThemeKey[]).map((tKey) => (
                        <button
                          key={tKey}
                          onClick={() => setThemeKey(tKey)}
                          className={`p-3 rounded-xl border text-xs font-semibold transition-all cursor-pointer ${
                            themeKey === tKey
                              ? 'border-blue-400 bg-blue-500/20'
                              : 'border-white/10 bg-white/5 hover:bg-white/10'
                          }`}
                        >
                          {THEMES[tKey].name}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="p-4 rounded-xl bg-white/5 border border-white/10 space-y-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="text-sm font-bold">Эффект прозрачного стекла (Glassmorphism 2.4)</h4>
                        <p className="text-xs text-slate-400">
                          Реальное размытие заднего фона ft.Blur и полупрозрачные стеклянные панели
                        </p>
                      </div>
                      <input
                        type="checkbox"
                        checked={glassEnabled}
                        onChange={(e) => setGlassEnabled(e.target.checked)}
                        className="w-5 h-5 accent-blue-500 cursor-pointer"
                      />
                    </div>

                    <div className="grid grid-cols-3 gap-3">
                      {(
                        [
                          ['light', 'Слабое размытие (8px)'],
                          ['medium', 'Среднее размытие (16px)'],
                          ['strong', 'Сильное размытие (28px)'],
                        ] as const
                      ).map(([intKey, intLabel]) => (
                        <button
                          key={intKey}
                          onClick={() => setGlassIntensity(intKey)}
                          className={`p-2.5 rounded-xl border text-xs font-medium cursor-pointer ${
                            glassIntensity === intKey
                              ? 'border-blue-400 bg-blue-500/20'
                              : 'border-white/10 bg-white/5'
                          }`}
                        >
                          {intLabel}
                        </button>
                      ))}
                    </div>

                    <div className="flex items-center gap-3">
                      <span className="text-xs text-slate-300">Непрозрачность стекла:</span>
                      <input
                        type="range"
                        min={20}
                        max={90}
                        value={glassOpacity}
                        onChange={(e) => setGlassOpacity(Number(e.target.value))}
                        className="flex-1 accent-blue-500 cursor-pointer"
                      />
                      <span className="text-xs font-mono tabular-nums w-10">{glassOpacity}%</span>
                    </div>

                    <div className="flex items-center justify-between pt-2 border-t border-white/10">
                      <div>
                        <div className="text-xs font-bold">Плавная анимация переходов между разделами</div>
                        <div className="text-[11px] text-slate-400">
                          Анимация ft.AnimatedSwitcher (EASE_OUT_CUBIC) при переключении вкладок и фильтров
                        </div>
                      </div>
                      <input
                        type="checkbox"
                        checked={smoothAnimations}
                        onChange={(e) => setSmoothAnimations(e.target.checked)}
                        className="w-4 h-4 accent-blue-500 cursor-pointer"
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 2: EXTENDED CLOCK STYLES (v2.4) */}
              {settingsTab === 'clock' && (
                <div className="space-y-4">
                  <div className="p-4 rounded-xl bg-white/5 border border-white/10 space-y-3">
                    <h4 className="text-sm font-bold">Выбор стиля часов (6 пресетов в v2.4)</h4>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                      {CLOCK_STYLE_OPTIONS.map((opt) => (
                        <button
                          key={opt.id}
                          onClick={() => setClockStyle(opt.id)}
                          className={`p-3 rounded-xl border text-left transition-all cursor-pointer flex items-center justify-between ${
                            clockStyle === opt.id
                              ? 'border-blue-400 bg-blue-500/20'
                              : 'border-white/10 bg-white/5 hover:bg-white/10'
                          }`}
                        >
                          <span className="text-xs font-semibold">{opt.label}</span>
                          <span className="text-xs font-mono text-blue-300">{opt.sample}</span>
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="p-4 rounded-xl bg-white/5 border border-white/10 space-y-3">
                    <h4 className="text-sm font-bold">Формат и детали отображения</h4>
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
                      <label className="flex items-center gap-2 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={showSeconds}
                          onChange={(e) => setShowSeconds(e.target.checked)}
                          className="accent-blue-500"
                        />
                        Показывать секунды
                      </label>
                      <label className="flex items-center gap-2 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={showDate}
                          onChange={(e) => setShowDate(e.target.checked)}
                          className="accent-blue-500"
                        />
                        Показывать дату
                      </label>
                      <label className="flex items-center gap-2 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={showWeekday}
                          onChange={(e) => setShowWeekday(e.target.checked)}
                          className="accent-blue-500"
                        />
                        День недели (Пн, Вт)
                      </label>
                      <label className="flex items-center gap-2 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={clockGlassFrame}
                          onChange={(e) => setClockGlassFrame(e.target.checked)}
                          className="accent-blue-500"
                        />
                        Стеклянная рамка
                      </label>
                    </div>

                    <div className="flex items-center gap-3 pt-2">
                      <span className="text-xs text-slate-300">Размер шрифта часов:</span>
                      <input
                        type="range"
                        min={14}
                        max={34}
                        value={timeFontSize}
                        onChange={(e) => setTimeFontSize(Number(e.target.value))}
                        className="flex-1 accent-blue-500 cursor-pointer"
                      />
                      <span className="text-xs font-mono tabular-nums">{timeFontSize}px</span>
                    </div>

                    <div className="flex flex-wrap items-center gap-3 pt-2">
                      <span className="text-xs text-slate-300">Быстрый цвет времени:</span>
                      {['#f8fafc', '#60a5fa', '#34d399', '#fbbf24', '#f472b6', '#c084fc'].map((hex) => (
                        <button
                          key={hex}
                          onClick={() => setTimeColor(hex)}
                          className={`w-6 h-6 rounded-full border-2 cursor-pointer ${
                            timeColor === hex ? 'border-white scale-110' : 'border-transparent'
                          }`}
                          style={{ backgroundColor: hex }}
                        />
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 3: BACKGROUND AUDIO CONTROLLER */}
              {settingsTab === 'system' && (
                <div className="p-4 rounded-xl bg-white/5 border border-white/10 space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="text-sm font-bold">Фоновый контроллер системной громкости (v2.4)</h4>
                      <p className="text-xs text-slate-400">
                        Работает через демон-очередь в отдельном потоке (pycaw IAudioEndpointVolume + COM CoInitialize)
                      </p>
                    </div>
                    <span className="text-xs font-mono text-emerald-400">{audioBgStatus}</span>
                  </div>

                  <div className="flex items-center gap-3">
                    <button
                      onClick={handleToggleMute}
                      className="px-3 py-1.5 rounded-xl bg-white/10 hover:bg-white/15 text-xs font-semibold cursor-pointer"
                    >
                      {isMuted ? 'Включить звук' : 'Mute'}
                    </button>
                    <input
                      type="range"
                      min={0}
                      max={100}
                      value={isMuted ? 0 : volume}
                      onChange={(e) => handleVolumeChange(Number(e.target.value))}
                      className="flex-1 accent-blue-500 cursor-pointer"
                    />
                    <span className="text-sm font-mono tabular-nums w-12 text-right">
                      {isMuted ? '0%' : `${volume}%`}
                    </span>
                  </div>
                </div>
              )}

              {/* TAB 4: VERSION 2.4 HISTORY */}
              {settingsTab === 'changelog' && (
                <div className="space-y-4">
                  {Object.entries(VERSION_HISTORY).map(([ver, items]) => (
                    <div
                      key={ver}
                      className={`p-4 rounded-xl border ${
                        ver === '2.4'
                          ? 'bg-blue-500/10 border-blue-500/40'
                          : 'bg-white/5 border-white/10'
                      }`}
                    >
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-bold text-blue-400">Version {ver}</span>
                        <span className="text-xs font-mono text-slate-400">{items.length} обновлений</span>
                      </div>
                      <ul className="space-y-1.5 text-xs text-slate-200">
                        {items.map((line, idx) => (
                          <li key={idx}>{line}</li>
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

      {/* ==================== MODAL 4: SMART WORKSPACE PRESETS ==================== */}
      {workspaceModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/65 backdrop-blur-sm p-4">
          <div
            className="w-full max-w-xl rounded-2xl border border-white/20 p-6 shadow-2xl"
            style={cardGlassStyle}
          >
            <div className="flex items-center justify-between pb-4 border-b border-white/10">
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
                  className="p-4 rounded-xl bg-white/5 border border-white/10 flex items-center justify-between gap-4"
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
            className="w-full max-w-xs rounded-2xl border border-white/20 p-4 shadow-2xl space-y-2"
            style={cardGlassStyle}
          >
            <div className="flex items-center gap-3 pb-3 border-b border-white/10">
              <div className="text-blue-400">{renderAppIcon(contextMenuApp.icon, 'w-6 h-6')}</div>
              <div className="min-w-0">
                <div className="text-sm font-bold truncate">{contextMenuApp.name}</div>
                <div className="text-xs text-slate-400 font-mono">
                  {formatMonthBadge(contextMenuApp.monthMinutes)}
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
              Запустить приложение
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
                handleAddSessionMinutes(contextMenuApp.id, 30);
                setContextMenuApp(null);
              }}
              className="w-full flex items-center gap-2.5 p-2.5 rounded-xl hover:bg-white/10 text-xs font-semibold cursor-pointer"
            >
              <Clock className="w-4 h-4 text-blue-400" />
              +30 мин в Session Tracker (тест детокса)
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

      {/* ==================== TOAST NOTIFICATIONS (System & Detox Alerts) ==================== */}
      <div className="fixed bottom-6 left-6 z-50 flex flex-col gap-2 max-w-md pointer-events-none">
        {toasts.map((t) => (
          <div
            key={t.id}
            className={`pointer-events-auto p-3.5 rounded-2xl border shadow-xl flex items-start gap-3 animate-in slide-in-from-bottom-2 duration-200 ${
              t.type === 'warning'
                ? 'bg-rose-950/90 border-rose-500/50 text-rose-100'
                : 'bg-slate-900/90 border-white/20 text-white'
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
