import React, { useState, useCallback } from 'react'
import Sidebar from './components/sidebar/sidebar'
import MapView from './components/main/MapView'

const App = () => {
    // Active overlay panel: null | 'aqi-legend' | 'locations' | 'about'
    const [activePanel, setActivePanel] = useState(null)
    // Map tile theme: 'dark' | 'satellite' | 'standard'
    const [mapTheme, setMapTheme] = useState('dark')
    // Location history
    const [locationHistory, setLocationHistory] = useState([])

    const togglePanel = useCallback((panel) => {
        setActivePanel((prev) => (prev === panel ? null : panel))
    }, [])

    const cycleTheme = useCallback(() => {
        setMapTheme((prev) => {
            if (prev === 'dark') return 'standard'
            if (prev === 'standard') return 'satellite'
            return 'dark'
        })
    }, [])

    const addLocation = useCallback((loc) => {
        setLocationHistory((prev) => [loc, ...prev].slice(0, 20))
    }, [])

    const clearHistory = useCallback(() => {
        setLocationHistory([])
    }, [])

    return (
        <>
            <Sidebar
                activePanel={activePanel}
                onTogglePanel={togglePanel}
                onCycleTheme={cycleTheme}
                mapTheme={mapTheme}
                onClearHistory={clearHistory}
                historyCount={locationHistory.length}
            />
            <MapView
                activePanel={activePanel}
                onClosePanel={() => setActivePanel(null)}
                mapTheme={mapTheme}
                locationHistory={locationHistory}
                onAddLocation={addLocation}
                onClearHistory={clearHistory}
            />
        </>
    )
}

export default App