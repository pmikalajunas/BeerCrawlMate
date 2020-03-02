
from .util import haversine, HOME_NODE_INDEX_MATRIX

class Matrix(object):

    def __init__(self):
        self.matrix = []


   # Calculates distance from current_node to each node from nodes.
    # Returns a list with distances. 
    def construct_distance_row(self, current_node, nodes):
        row = []
        for node in nodes:
            row.append(haversine(current_node.lat, current_node.long, node.lat, node.long))
        return row


    # Constructs distance matrix from a list of nodes.
    # Matrix is of size n*n (n - number of nodes).
    def construct_distance_matrix(self, nodes):
        for node in nodes:
            self.matrix.append(self.construct_distance_row(node, nodes))


    # Finds the node with minimum distane in the given row.
    # Returns both the node and its index.
    # Returns float('inf') and index of the home node ...
    # if there are no unvisited nodes.
    def find_min(self, row_index, nodes):
        row = self.matrix[row_index]
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


    def get_route_fitness(self, route):
        fitness = 0
        # Last node is the home node, hence -1.
        i = 0
        while i != (len(route) - 1):
            # Distance from current to next node in the route.
            current = route[i].matrix_id
            next = route[i+1].matrix_id
            distance = self.get_node(next, current)
            beer_count = route[i+1].beer_count
            if beer_count > 0:
                fitness += (distance / route[i+1].beer_count)
            else:
                fitness += distance
            i += 1
        return fitness


    def get_node(self, x, y):
        return self.matrix[y][x]