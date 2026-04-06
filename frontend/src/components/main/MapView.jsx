import React, { useState, useCallback, useMemo } from 'react'
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import './MapView.css'

// Fix default marker icon
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
})

const pulsingIcon = new L.DivIcon({
  className: 'pulsing-marker',
  html: `<div class="marker-pin"></div><div class="marker-pulse"></div>`,
  iconSize: [20, 20],
  iconAnchor: [10, 10],
})

const historyIcon = new L.DivIcon({
  className: 'history-marker',
  html: `<div class="history-pin"></div>`,
  iconSize: [12, 12],
  iconAnchor: [6, 6],
})

const INDIA_BOUNDS = [
  [6.5, 68.0],
  [37.5, 97.5],
]

const TILE_URLS = {
  dark: {
    url: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
    attr: '&copy; OpenStreetMap &copy; CARTO',
  },
  standard: {
    url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attr: '&copy; OpenStreetMap contributors',
  },
  satellite: {
    url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr: '&copy; Esri &mdash; Source: Esri, Maxar, Earthstar Geographics',
  },
}

const AQI_SCALE = [
  { range: '0–50', label: 'Good', color: '#22c55e', desc: 'Air quality is satisfactory' },
  { range: '51–100', label: 'Moderate', color: '#eab308', desc: 'Acceptable for most people' },
  { range: '101–150', label: 'Unhealthy (Sensitive)', color: '#f97316', desc: 'Sensitive groups affected' },
  { range: '151–200', label: 'Unhealthy', color: '#ef4444', desc: 'Health effects for everyone' },
  { range: '201–300', label: 'Very Unhealthy', color: '#a855f7', desc: 'Serious health effects' },
  { range: '301–500', label: 'Hazardous', color: '#991b1b', desc: 'Emergency conditions' },
]

function ClickHandler({ onClick }) {
  useMapEvents({ click(e) { onClick(e.latlng) } })
  return null
}

const MapView = ({ activePanel, onClosePanel, mapTheme, locationHistory, onAddLocation, onClearHistory }) => {
  const [position, setPosition] = useState(null)
  const [aqi, setAqi] = useState(null)

  const tileConfig = useMemo(() => TILE_URLS[mapTheme] || TILE_URLS.dark, [mapTheme])

  const handleClick = useCallback((latlng) => {
    const point = {
      lat: latlng.lat.toFixed(6),
      lng: latlng.lng.toFixed(6),
      timestamp: new Date().toLocaleTimeString(),
      date: new Date().toLocaleDateString(),
    }
    setPosition(point)
    setAqi(null)
    onAddLocation(point)
  }, [onAddLocation])

  const goToLocation = useCallback((loc) => {
    setPosition(loc)
    setAqi(null)
  }, [])

  return (
    <div className="map-container">
      {/* Header */}
      <div className="map-header">
        <div className="map-header-left">
          <div className="header-icon">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
              <circle cx="12" cy="10" r="3"/>
            </svg>
          </div>
          <div>
            <h1 className="map-title">EcoAir Insight</h1>
            <p className="map-subtitle">Click anywhere on the map to get coordinates & AQI</p>
          </div>
        </div>
        {position && (
          <div className="coords-badge">
            <span className="coords-lat">{position.lat}°</span>
            <span className="coords-divider">|</span>
            <span className="coords-lng">{position.lng}°</span>
          </div>
        )}
      </div>

      {/* Map */}
      <div className="map-wrapper">
        <MapContainer
          center={[22.5, 82.0]}
          zoom={5}
          minZoom={4}
          maxZoom={18}
          maxBounds={INDIA_BOUNDS}
          maxBoundsViscosity={1.0}
          className="leaflet-map"
          zoomControl={false}
        >
          <TileLayer
            key={mapTheme}
            attribution={tileConfig.attr}
            url={tileConfig.url}
          />
          <ClickHandler onClick={handleClick} />

          {/* History markers */}
          {locationHistory.slice(1).map((loc, i) => (
            <Marker
              key={`hist-${i}`}
              position={[parseFloat(loc.lat), parseFloat(loc.lng)]}
              icon={historyIcon}
            />
          ))}

          {/* Active marker */}
          {position && (
            <Marker
              position={[parseFloat(position.lat), parseFloat(position.lng)]}
              icon={pulsingIcon}
            >
              <Popup className="custom-popup">
                <div className="popup-content">
                  <div className="popup-title">Selected Location</div>
                  <div className="popup-row">
                    <span className="popup-label">Latitude</span>
                    <span className="popup-value">{position.lat}°</span>
                  </div>
                  <div className="popup-row">
                    <span className="popup-label">Longitude</span>
                    <span className="popup-value">{position.lng}°</span>
                  </div>
                  <div className="popup-row">
                    <span className="popup-label">AQI</span>
                    <span className="popup-value aqi-pending">{aqi !== null ? aqi : '—'}</span>
                  </div>
                  <div className="popup-time">{position.timestamp}</div>
                </div>
              </Popup>
            </Marker>
          )}
        </MapContainer>

        {/* ── Floating Info Card ── */}
        <div className="info-card">
          {position ? (
            <>
              <div className="info-card-header">
                <div className="info-dot"></div>
                <span>Location Selected</span>
              </div>
              <div className="info-grid">
                <div className="info-item">
                  <span className="info-label">LAT</span>
                  <span className="info-value">{position.lat}°</span>
                </div>
                <div className="info-item">
                  <span className="info-label">LNG</span>
                  <span className="info-value">{position.lng}°</span>
                </div>
              </div>
              <div className="aqi-section">
                <div className="aqi-box">
                  <span className="aqi-label">AQI</span>
                  <span className="aqi-value">{aqi !== null ? aqi : '—'}</span>
                  <span className="aqi-status">
                    {aqi !== null ? 'From ML Model' : 'Awaiting prediction'}
                  </span>
                </div>
              </div>
            </>
          ) : (
            <div className="info-empty">
              <div className="info-empty-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" opacity="0.5">
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M2 12h20"/>
                  <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
                </svg>
              </div>
              <p>Click on the map to select a location</p>
            </div>
          )}
        </div>

        {/* ── AQI Legend Overlay ── */}
        {activePanel === 'aqi-legend' && (
          <div className="overlay-panel aqi-legend-panel">
            <div className="overlay-header">
              <h3>AQI Scale</h3>
              <button className="overlay-close" onClick={onClosePanel}>✕</button>
            </div>
            <div className="aqi-legend-list">
              {AQI_SCALE.map((item, i) => (
                <div key={i} className="aqi-legend-row">
                  <div className="aqi-legend-color" style={{ background: item.color }}></div>
                  <div className="aqi-legend-info">
                    <div className="aqi-legend-top">
                      <span className="aqi-legend-range">{item.range}</span>
                      <span className="aqi-legend-label">{item.label}</span>
                    </div>
                    <span className="aqi-legend-desc">{item.desc}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── Locations Panel ── */}
        {activePanel === 'locations' && (
          <div className="overlay-panel locations-panel">
            <div className="overlay-header">
              <h3>Saved Locations</h3>
              <button className="overlay-close" onClick={onClosePanel}>✕</button>
            </div>
            {locationHistory.length === 0 ? (
              <div className="overlay-empty">
                <p>No locations saved yet. Click on the map to save a location.</p>
              </div>
            ) : (
              <div className="locations-list">
                {locationHistory.map((loc, i) => (
                  <div
                    key={i}
                    className={`location-row ${position && position.lat === loc.lat && position.lng === loc.lng ? 'location-active' : ''}`}
                    onClick={() => goToLocation(loc)}
                  >
                    <div className="location-index">{i + 1}</div>
                    <div className="location-details">
                      <div className="location-coords">
                        {loc.lat}°, {loc.lng}°
                      </div>
                      <div className="location-time">{loc.timestamp} · {loc.date}</div>
                    </div>
                    <svg className="location-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <polyline points="9 18 15 12 9 6"/>
                    </svg>
                  </div>
                ))}
                <button className="clear-all-btn" onClick={onClearHistory}>
                  Clear All
                </button>
              </div>
            )}
          </div>
        )}

        {/* ── About Overlay ── */}
        {activePanel === 'about' && (
          <div className="overlay-panel about-panel">
            <div className="overlay-header">
              <h3>About</h3>
              <button className="overlay-close" onClick={onClosePanel}>✕</button>
            </div>
            <div className="about-content">
              <div className="about-logo">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M9.59 4.59A2 2 0 1 1 11 8H2" />
                  <path d="M12.59 19.41A2 2 0 1 0 14 16H2" />
                  <path d="M17.73 7.73A2.5 2.5 0 1 1 19.5 12H2" />
                </svg>
              </div>
              <h2 className="about-title">EcoAir Insight</h2>
              <p className="about-version">v1.0.0</p>
              <p className="about-desc">
                Interactive air quality monitoring tool for India. Click anywhere on the map to get location coordinates and AQI predictions powered by our ML model.
              </p>
              <div className="about-features">
                <div className="about-feature">
                  <span className="about-feature-icon">🗺️</span>
                  <span>Interactive India map</span>
                </div>
                <div className="about-feature">
                  <span className="about-feature-icon">📍</span>
                  <span>Click-to-locate coordinates</span>
                </div>
                <div className="about-feature">
                  <span className="about-feature-icon">🤖</span>
                  <span>ML-powered AQI predictions</span>
                </div>
                <div className="about-feature">
                  <span className="about-feature-icon">💬</span>
                  <span>LLM assistant (coming soon)</span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default MapView
