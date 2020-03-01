
# Coordinate boundaries for Google Maps.
LAT_MIN = -85
LAT_MAX = 85
LONG_MIN = -180
LONG_MAX = 180

# Checks if coordinates are withing boundaries.
# Returns True if coordinates are valid.
# Returns False otherwise.
def validate_coordinates(lat, long):
    if lat >= LAT_MIN and lat <= LAT_MAX:
        if long >= LONG_MIN and long <= LONG_MAX:
            return True
    return False
