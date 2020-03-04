import numpy as np

# Coordinate boundaries for Google Maps.
from beer_data.models import Brewery, Beer

LAT_MIN = -85
LAT_MAX = 85
LONG_MIN = -180
LONG_MAX = 180
# Id of a home (starting) node.
HOME_NODE_ID = -2
# Earth radius (in KM)
EARTH_RADIUS = 6367
# First node in the matrix is the home node.
HOME_NODE_INDEX_MATRIX = 0


# Checks if coordinates are withing boundaries.
# Returns True if coordinates are valid.
# Returns False otherwise.
def validate_coordinates(lat, long):
    if LAT_MIN <= lat <= LAT_MAX:
        if LONG_MIN <= long <= LONG_MAX:
            return True
    return False


# Returns first index associated with (elem) in given (list).
def find_index(list, elem):
    for i in range(len(list)):
        if list[i] == elem:
            return i
    return -1

# Returns a list of beers that each brewery in a list of nodes contains.
def get_beers(nodes):
    beers = []
    for node in nodes:
        if node.id == HOME_NODE_ID:
            continue
        brewery = Brewery.objects.filter(id=node.id)[0]
        brewery_beers = Beer.objects.filter(brewery=brewery)
        beers += brewery_beers
    return beers


# Returns route's distance.
# Distance between nodes is calculated from distance matrix.
def get_overall_distance(matrix, route):
    distance = 0
    for i, node in enumerate(route[:-1]):
        node_distance = matrix.get_node(route[i+1].matrix_id, route[i].matrix_id)
        route[i+1].distance = round(node_distance, 2)
        distance += node_distance
    return distance


# Calculates Harvesine distance between (lat1, lon1) and (lat2, lon2)
# Returns harvesine distance in kilometers.
def haversine(lat1, lon1, lat2, lon2):
    # If we are dealing with the same node, skip the calculations.
    if lat1 == lat2 and lon1 == lon2:
        return 0

    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    km = EARTH_RADIUS * c
    return km
