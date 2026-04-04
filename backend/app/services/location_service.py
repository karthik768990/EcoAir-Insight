import numpy as np
from typing import Tuple, Optional


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate great circle distance between two points."""
    R = 6371
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c


def validate_coordinates(latitude: float, longitude: float) -> Tuple[bool, Optional[str]]:
    """Validate if coordinates are in valid range."""
    if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
        return False, "Latitude and longitude must be numeric"
    
    if latitude < -90 or latitude > 90:
        return False, "Latitude must be between -90 and 90"
    
    if longitude < -180 or longitude > 180:
        return False, "Longitude must be between -180 and 180"
    
    return True, None
