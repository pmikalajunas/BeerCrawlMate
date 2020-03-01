
import numpy as np
import timeit

from .models import Brewery, Beer

# Max distance that helicopter can travel.
MAX_DISTANCE = 2000
# Id of a home (starting) node.
HOME_NODE_ID = -2
# Earth radius (in KM)
EARTH_RADIUS = 6367
# First node in the matrix is the home node.
HOME_NODE_INDEX_MATRIX = 0


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


# Finds all the nodes within (MAX_DISTANCE / 2) radius.
# Adds starting node at index HOME_NODE_INDEX_MATRIX.
# Returns a list of nodes.
def create_nodes(home_lat, home_long):
    # Start from home node, increment each time.
    node_index = HOME_NODE_INDEX_MATRIX
    # Initialize home node.
    nodes = [Node(node_index, HOME_NODE_ID, "Starting location", home_lat, home_long)]
    nodes[HOME_NODE_INDEX_MATRIX].visited = True
   
    for brewery in Brewery.objects.all():
        distance = haversine(home_lat, home_long, brewery.latitude, brewery.longitude)
        # If distance is more than it will take us to go back and forth, we'll ignore the brewery.
        if distance > (MAX_DISTANCE / 2):
            continue
        node_index += 1
        nodes.append(Node(node_index, brewery.id, brewery.name, brewery.latitude, brewery.longitude))
    return nodes


# Constructs distance matrix from a list of nodes.
# Matrix is of size n*n (n - number of nodes).
# Returns a 2D list.
def construct_distance_matrix(nodes):
    matrix = []
    for node in nodes:
        matrix.append(construct_distance_row(node, nodes))
    return matrix
        

# Calculates distance from current_node to each node from nodes.
# Returns a list with distances. 
def construct_distance_row(current_node, nodes):
    row = []
    for node in nodes:
        row.append(haversine(current_node.lat, current_node.long, node.lat, node.long))
    return row



# Returns a list of beers that each brewery in nodes contains.
def get_beers(nodes):
    beers = []
    for node in nodes:
        if node.id == HOME_NODE_ID:
            continue
        brewery = Brewery.objects.filter(id=node.id)[0]
        brewery_beers = Beer.objects.filter(brewery=brewery)
        beers += brewery_beers
    return beers

def TSP(matrix, nodes):
    # Adding the home node as the first move.
    solution_vector = [nodes[0]]
    distance_travelled = 0.0
    distance_travelled = greedy_solution(matrix, nodes, solution_vector, distance_travelled)
    return (distance_travelled, solution_vector)


def greedy_solution(matrix, nodes, solution, distance_travelled):

    N = len(matrix)
    # Getting the previously visited node, first visited is home node.
    previous_node = solution[len(solution) - 1].matrix_id

    print('_______________________________________________________________')
    print("Travelled: %f | previous_node: %d" % (distance_travelled, previous_node))
    print('Matrix:')
    if len(matrix) < 10:
        print(matrix)
    print('Nodes:')
    for node in nodes:
        print(node)

    min, index = find_min(matrix[previous_node], nodes)



    print("Found node id: %d with distance %f" % (index, min))

    home_distance = matrix[index][0]
    # Amount of remaining mileage we would have, if we would go to the node and back home.
    mileage_left = MAX_DISTANCE - (distance_travelled + min + home_distance)    
    print("Mileage left: %f home_distance: %f" % (mileage_left, home_distance))

    # If all nodes are visited or we don't have enough remaining mileage, we go home.
    if min == float('inf') or mileage_left < 0:
        print('No more nodes/mileage, going back home!')
        # Calculate distance from previous node, because index is set to home.
        home_distance = matrix[previous_node][HOME_NODE_INDEX_MATRIX]
        distance_travelled += home_distance
        solution.append(nodes[HOME_NODE_INDEX_MATRIX])
        return distance_travelled


    # Lookahead, if we would be able to go home by visiting current node.

    # Mark node as visited.
    nodes[index].visited = True
    # Update and round node's distance.
    nodes[index].distance = round(min)     
    distance_travelled += min
    solution.append(nodes[index])
    return greedy_solution(matrix, nodes, solution, distance_travelled)




# Finds the node with minimum distane in the given row.
# Returns both the node and its index.
# Returns float('inf') and index of the home node ...
# if there are no unvisited nodes.
def find_min(row, nodes):
    min = float('inf')
    index = HOME_NODE_INDEX_MATRIX
    
    for i in range(len(row)):
        # We start from 1 to avoid checking the home node.
        if i == 0:
            continue
        if row[i] <= min and nodes[i].visited == False:
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
        self.distance = 0

    def __str__(self):
        return ("matrix_id: %d id: %d name: %s lat: %f long: %f" % 
                (self.matrix_id, self.id, self.name, self.lat, self.long))
