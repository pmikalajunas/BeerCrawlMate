
import numpy as np
import timeit


MAX_DISTANCE = 2000

from .models import Brewery

# Earth radius (in KM)
EARTH_RADIUS = 6367

def haversine(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = EARTH_RADIUS * c
    return km

def construct_distance_matrix(lat, long):
    start = timeit.default_timer()
    # Pick out breweries that are less than (MAX_DISTANCE / 2)
    matrix = []
    # Calculate distance from current node to every brewery.
    matrix.append(construct_distance_row(lat, long))
    for brewery in Brewery.objects.all():
        matrix.append(construct_distance_row(lat, long))

    stop = timeit.default_timer()
    time = stop - start;
    return (matrix, time)
        

def construct_distance_row(lat, long):
    row = []
    for brewery in Brewery.objects.all():
        row.append(haversine(lat, long, brewery.latitude, brewery.longitude))
    return row


