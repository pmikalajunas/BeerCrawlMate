


from .models import Brewery, Beer
from .node import *
from .util import *
from .matrix import Matrix




def TSP(matrix, nodes):
    # Adding the home node as the first move.
    solution_vector = [nodes[0]]
    distance_travelled = 0.0
    distance_travelled = nearest_neighbour(matrix, nodes, solution_vector, distance_travelled)
    # Set fitness.
    return (distance_travelled, solution_vector)


def nearest_neighbour(matrix, nodes, solution, distance_travelled):

    # Getting the previously visited node, first visited is home node.
    previous_node = solution[len(solution) - 1].matrix_id

    print('_______________________________________________________________')
    print("Travelled: %f | previous_node: %d" % (distance_travelled, previous_node))
    print('Matrix:')
    print('Nodes:')
    for node in nodes:
        print(node)

    min, index = matrix.find_min(previous_node, nodes)

    print("Found node id: %d with distance %f" % (index, min))

    home_distance = matrix.get_node(0, index)

    # Amount of remaining mileage we would have, if we would go to the node and back home.
    mileage_left = MAX_DISTANCE - (distance_travelled + min + home_distance)    
    print("Mileage left: %f home_distance: %f" % (mileage_left, home_distance))

    # If all nodes are visited or we don't have enough remaining mileage, we go home.
    if min == float('inf') or mileage_left < 0:
        print('No more nodes/mileage, going back home!')
        # Calculate distance from previous node, because index is set to home.
        home_distance = matrix.get_node(HOME_NODE_INDEX_MATRIX, previous_node)        
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
    return nearest_neighbour(matrix, nodes, solution, distance_travelled)


def find_min_heuristic(row, nodes):
    min = float('inf')
    index = HOME_NODE_INDEX_MATRIX

    for i in range(len(row)):
        # We start from 1 to avoid checking the home node.
        if i == 0:
            continue
        if get_heuristic_distance(row, nodes) <= min and nodes[i].visited == False:
            min = row[i]
            index = i
    return (min, index)


def get_heuristic_distance(row, nodes):
    # We don't want to go to the brewery without beers.
    if nodes[i].beer_count == 0:
        return 0
    else:
        return row[i] / nodes[i].beer_count




