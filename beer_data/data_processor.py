
import numpy as np
import timeit

from .models import Brewery

# Max distance that helicopter can travel.
MAX_DISTANCE = 2000
# Id of a home (starting) node.
HOME_NODE = -2
# Earth radius (in KM)
EARTH_RADIUS = 6367

def haversine(lat1, lon1, lat2, lon2):

    # If we are dealing with the same node, we want infinite distance.
    if lat1 == lat2 and lon1 == lon2:
        return float('inf')

    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = EARTH_RADIUS * c
    return km


def create_nodes(home_lat, home_long):
    nodes = [Node(HOME_NODE, home_lat, home_long)]
    for brewery in Brewery.objects.all():
        distance = haversine(home_lat, home_long, brewery.latitude, brewery.longitude)
        # If distance is more than it will take us to go forth and back, we'll ignore the brewery.
        if distance > (MAX_DISTANCE / 2):
            continue
        nodes.append(Node(brewery.id, brewery.latitude, brewery.longitude))
    return nodes


def construct_distance_matrix(nodes):
    start = timeit.default_timer()
    matrix = []
    for node in nodes:
        matrix.append(construct_distance_row(node, nodes))

    stop = timeit.default_timer()
    time = stop - start;
    return (matrix, time)
        

def construct_distance_row(current_node, nodes):
    row = []
    for node in nodes:
        row.append(
            haversine(current_node.lat, current_node.long, node.lat, node.long)
        )
    return row


def brute_force(matrix, nodes):
    # Adding the home node as the first move.
    solution_vector = [nodes[0]]
    for row in matrix:
        min, index = find_min(row)


def find_min(row):
    min = float('inf')
    index = 0
    for i in range(len(row)):
        if row[i] < min:
            min = row[i]
            index = i
    return (min, index)

class Node:
    def __init__(self, id, lat, long):
        self.id = id
        self.lat = lat
        self.long = long
        self.visited = False
