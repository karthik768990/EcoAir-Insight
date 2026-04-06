import React, { useState } from 'react'
import './sidebar.css'

/* ── Inline SVG Icons ── */
const Icon = ({ children, size = 22 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none"
    stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    {children}
  </svg>
)

const MenuIcon = () => (
  <Icon>
    <line x1="3" y1="6" x2="21" y2="6" />
    <line x1="3" y1="12" x2="21" y2="12" />
    <line x1="3" y1="18" x2="21" y2="18" />
  </Icon>
)

const PlusIcon = () => (
  <Icon>
    <circle cx="12" cy="12" r="10" />
    <line x1="12" y1="8" x2="12" y2="16" />
    <line x1="8" y1="12" x2="16" y2="12" />
  </Icon>
)

const ChatIcon = () => (
  <Icon size={18}>
    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
  </Icon>
)

const AirQualityIcon = () => (
  <Icon>
    <path d="M9.59 4.59A2 2 0 1 1 11 8H2" />
    <path d="M12.59 19.41A2 2 0 1 0 14 16H2" />
    <path d="M17.73 7.73A2.5 2.5 0 1 1 19.5 12H2" />
  </Icon>
)

const MapPinIcon = () => (
  <Icon>
    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
    <circle cx="12" cy="10" r="3" />
  </Icon>
)

const HistoryIcon = () => (
  <Icon>
    <circle cx="12" cy="12" r="10" />
    <polyline points="12 6 12 12 16 14" />
  </Icon>
)

const SettingsIcon = () => (
  <Icon>
    <circle cx="12" cy="12" r="3" />
    <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" />
  </Icon>
)

const InfoIcon = () => (
  <Icon>
    <circle cx="12" cy="12" r="10" />
    <line x1="12" y1="16" x2="12" y2="12" />
    <line x1="12" y1="8" x2="12.01" y2="8" />
  </Icon>
)

// Map theme icons
const DarkThemeIcon = () => (
  <Icon size={16}>
    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
  </Icon>
)
const LightThemeIcon = () => (
  <Icon size={16}>
    <circle cx="12" cy="12" r="5" />
    <line x1="12" y1="1" x2="12" y2="3" />
    <line x1="12" y1="21" x2="12" y2="23" />
    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
    <line x1="1" y1="12" x2="3" y2="12" />
    <line x1="21" y1="12" x2="23" y2="12" />
    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
    <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
  </Icon>
)
const SatelliteIcon = () => (
  <Icon size={16}>
    <circle cx="12" cy="12" r="10" />
    <path d="M2 12h20" />
    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
  </Icon>
)

const THEME_LABELS = { dark: 'Dark', standard: 'Standard', satellite: 'Satellite' }
const THEME_ICONS = { dark: <DarkThemeIcon />, standard: <LightThemeIcon />, satellite: <SatelliteIcon /> }

const Sidebar = ({ activePanel, onTogglePanel, onCycleTheme, mapTheme, onClearHistory, historyCount }) => {
  const [extended, setExtended] = useState(false)

  return (
    <div className={`sidebar ${extended ? 'sidebar-extended' : ''}`}>
      <div className="top">
        <button className="menu-btn" onClick={() => setExtended(prev => !prev)} aria-label="Toggle sidebar">
          <MenuIcon />
        </button>

        <div className="new-chat" role="button" tabIndex={0} title="New Chat (LLM coming soon)">
          <PlusIcon />
          {extended && <span>New Chat</span>}
          {extended && <span className="coming-soon-tag">Soon</span>}
        </div>

        {extended && (
          <div className="recent">
            <p className="recent-title">Recent</p>
            <div className="recent-entry">
              <ChatIcon />
              <p>What is react ...</p>
            </div>
          </div>
        )}
      </div>

      <div className="bottom">
        {/* AQI Legend */}
        <div
          className={`bottom-item recent-entry ${activePanel === 'aqi-legend' ? 'active' : ''}`}
          onClick={() => onTogglePanel('aqi-legend')}
          title="AQI Scale Legend"
        >
          <AirQualityIcon />
          {extended && <p>AQI Legend</p>}
        </div>

        {/* Saved Locations */}
        <div
          className={`bottom-item recent-entry ${activePanel === 'locations' ? 'active' : ''}`}
          onClick={() => onTogglePanel('locations')}
          title="Saved Locations"
        >
          <MapPinIcon />
          {extended && <p>Locations</p>}
          {!extended && historyCount > 0 && <span className="icon-badge">{historyCount}</span>}
          {extended && historyCount > 0 && <span className="count-tag">{historyCount}</span>}
        </div>

        {/* Clear History */}
        <div
          className={`bottom-item recent-entry ${historyCount === 0 ? 'disabled' : ''}`}
          onClick={historyCount > 0 ? onClearHistory : undefined}
          title={historyCount > 0 ? 'Clear all location history' : 'No history to clear'}
        >
          <HistoryIcon />
          {extended && <p>Clear History</p>}
        </div>

        {/* About */}
        <div
          className={`bottom-item recent-entry ${activePanel === 'about' ? 'active' : ''}`}
          onClick={() => onTogglePanel('about')}
          title="About EcoAir Insight"
        >
          <InfoIcon />
          {extended && <p>About</p>}
        </div>

        {/* Map Theme Toggle */}
        <div
          className="bottom-item recent-entry theme-toggle"
          onClick={onCycleTheme}
          title={`Map theme: ${THEME_LABELS[mapTheme]} (click to cycle)`}
        >
          <SettingsIcon />
          {extended && (
            <div className="theme-info">
              <p>Theme</p>
              <span className="theme-badge">
                {THEME_ICONS[mapTheme]}
                {THEME_LABELS[mapTheme]}
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Sidebar