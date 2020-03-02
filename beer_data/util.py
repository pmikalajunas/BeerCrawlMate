import numpy as np


# Coordinate boundaries for Google Maps.
LAT_MIN = -85
LAT_MAX = 85
LONG_MIN = -180
LONG_MAX = 180

# Earth radius (in KM)
EARTH_RADIUS = 6367
# First node in the matrix is the home node.
HOME_NODE_INDEX_MATRIX = 0

# Checks if coordinates are withing boundaries.
# Returns True if coordinates are valid.
# Returns False otherwise.
def validate_coordinates(lat, long):
    if lat >= LAT_MIN and lat <= LAT_MAX:
        if long >= LONG_MIN and long <= LONG_MAX:
            return True
    return False


# Calculates Harvesine distance between (lat1, lon1) and (lat2, lon2)
# Returns harvesine distance in kilometers.
def haversine(lat1, lon1, lat2, lon2): 
    # If we are dealing with the same node, skip the calculations.
    if lat1 == lat2 and lon1 == lon2:
        return 0

    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    km = EARTH_RADIUS * c
    return km



