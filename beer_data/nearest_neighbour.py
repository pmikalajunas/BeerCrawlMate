from .node import *
from .util import *


class NearestNeighbour(object):

    def __init__(self, nodes, matrix):
        self.distance = 0
        self.nodes = nodes
        self.route = [nodes[HOME_NODE_INDEX_MATRIX]]
        self.matrix = matrix


    def search(self):
        # Getting the previously visited node, first visited is home node.
        previous_node = self.route[-1].matrix_id

        min, index = self.matrix.find_min(previous_node, self.nodes)
        home_distance = self.matrix.get_node(0, index)

        # Amount of remaining mileage we would have, if we would go to the node and back home.
        mileage_left = MAX_DISTANCE - (self.distance + min + home_distance)

        # If all nodes are visited or we don't have enough remaining mileage, we go home.
        if min == float('inf') or mileage_left < 0:
            # Calculate distance from previous node, because index is set to home.
            home_distance = self.matrix.get_node(HOME_NODE_INDEX_MATRIX, previous_node)
            self.distance += home_distance
            self.route.append(self.nodes[HOME_NODE_INDEX_MATRIX])
            return

        # Mark node as visited.
        self.nodes[index].visited = True
        # Update and round node's distance.
        self.nodes[index].distance = round(min)
        self.distance += min
        self.route.append(self.nodes[index])
        return self.search()

