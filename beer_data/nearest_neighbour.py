from beer_data.graph import Graph
from .node import *


class NearestNeighbour(object):

    def __init__(self, nodes):
        self.distance = 0
        self.nodes = nodes
        self.route = [nodes[HOME_NODE]]
        self.graph = Graph(nodes)


    def search(self):
        # Getting the previously visited node, first visited is home node.
        previous_node = self.route[-1]

        node, min = self.graph.get_min_distance(previous_node)
        home_distance = self.graph.get_home_distance(node)

        # Amount of remaining mileage we would have, if we would go to the node and back home.
        mileage_left = MAX_DISTANCE - (self.distance + min + home_distance)

        # If all nodes are visited or we don't have enough remaining mileage, we go home.
        if min == float('inf') or mileage_left < 0:
            # Calculate distance from previous node, because index is set to home.
            home_distance = self.graph.get_home_distance(previous_node)
            self.distance += home_distance
            self.route.append(self.nodes[HOME_NODE])
            return

        # Mark node as visited.
        node.visited = True
        # Update and round node's distance.
        node.distance = round(min)
        self.distance += min
        self.route.append(node)
        return self.search()

