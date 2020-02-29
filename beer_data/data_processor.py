
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
    node_index = 0
    # Initialize home node.
    nodes = [Node(node_index, HOME_NODE, "Starting location", home_lat, home_long)]
    nodes[node_index].visited = True
   
    for brewery in Brewery.objects.all():
        distance = haversine(home_lat, home_long, brewery.latitude, brewery.longitude)
        # If distance is more than it will take us to go back and forth, we'll ignore the brewery.
        if distance > (MAX_DISTANCE / 2):
            continue
        node_index += 1
        nodes.append(Node(node_index, brewery.id, brewery.name, brewery.latitude, brewery.longitude))
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


def TSP(matrix, nodes):
    # Adding the home node as the first move.
    solution_vector = [nodes[0]]
    visited = [False] * len(matrix)
    visited[0] = True
    distance_travelled = 0.0
    distance_travelled = greedy_solution(matrix, nodes, solution_vector, visited, distance_travelled)
    return (distance_travelled, solution_vector)


def greedy_solution(matrix, nodes, solution, visited, distance_travelled):

    N = len(matrix)
    # Getting the previously visited node.
    row = solution[len(solution) - 1].matrix_id
    print('_______________________________________________________________')
    print("Travelled: %f | Row id: %d" % (distance_travelled, row))

    min, index = find_min(matrix[row], nodes)
    print("Found node id: %d with distance %f" % (index, min))
    # Can we go back home with remaining fuel?
    home_distance = matrix[index][0]
    mileage_left = MAX_DISTANCE - (distance_travelled + min + home_distance)    
    print("Mileage left: %f home_distance: %f" % (mileage_left, home_distance))
    # Mark node as visited.
    nodes[index].visited = True
    # If we can return home, add the home node and end search.
    if mileage_left < 100 and mileage_left > 0:
        distance_travelled += min + home_distance
        solution.append(nodes[index])
        solution.append(nodes[0])
        return distance_travelled
    # If we can't make it to the closest node, we go back home.    
    if mileage_left < 0:
        distance_travelled += home_distance
        solution.append(nodes[0])
        return distance_travelled

    distance_travelled += min
    solution.append(nodes[index])
    return greedy_solution(matrix, nodes, solution, visited, distance_travelled)


def find_min(row, nodes):
    min = float('inf')
    index = 0
    for i in range(len(row)):
        if row[i] < min and nodes[i].visited == False:
            min = row[i]
            index = i
    return (min, index)

class Node:
    # matrix_id - node's index in the matrix.
    def __init__(self, matrix_id, id, name, lat, long):
        self.matrix_id = matrix_id
        self.id = id
        self.name = name
        self.lat = lat
        self.long = long
        self.visited = False
