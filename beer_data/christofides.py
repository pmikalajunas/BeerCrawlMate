from beer_data.graph import Graph, min_weight_matching
from beer_data.node import HOME_NODE
from .util import haversine

# Distance after
DISTANCE_LOWER_BOUND = 1600
# Overall distance limit that we can't exceed.
DISTANCE_HIGHER_BOUND = 2000


class Christofides(object):

    def __init__(self, nodes):
        self.graph = Graph(nodes)
        self.nodes = nodes
        self.mst = self.graph.get_mst()
        self.distance = 0
        self.route = []

    # Performs search using Christofides algorithm.
    # Find a minimum-weight perfect matching min_weight in the subgraph given by the vertices from odd_nodes
    # Combine the edges of min_weight and mst to form a connected multigraph H in which each vertex has even degree.
    def search(self):
        subgraph = self.graph.get_odd_node_subgraph()
        min_weight = min_weight_matching(subgraph)

        self.add_matching_to_mst(min_weight)
        path = self.hamilton_circuit(self.nodes[HOME_NODE])
        return path, self.distance

    # Returns optimal path.
    def hamilton_circuit(self, home_node):
        ham_path = [home_node]
        path_found = self.hamilton_circuit_helper(home_node, ham_path)

        if not path_found:
            return None
        return ham_path

    # Make a Hamilton circuit by skipping repeated vertices.
    # Path can be considered as finished once distance is between ...
    # DISTANCE_LOWER_BOUND and DISTANCE_HIGHER_BOUND
    # Then, we try to go to the home node, if we can't, we backtrack.
    def hamilton_circuit_helper(self, home_node, ham_path):

        # If we have travelled at least DISTANCE_LOWER_BOUND, check if we can go home.
        if self.distance > DISTANCE_LOWER_BOUND:
            distance_to_home = self.graph.get_home_distance(ham_path[-1])
            distance = self.distance + distance_to_home
            if distance < DISTANCE_HIGHER_BOUND:
                ham_path.append(home_node)
                self.distance += distance_to_home
                return True
            else:
                return False

        for node in self.mst.nodes:
            edge = self.mst.get_edge_data(ham_path[-1], node, default=None)

            if edge is not None and node not in ham_path:
                ham_path.append(node)
                node.distance = round(edge['weight'], 2)
                self.distance += edge['weight']
                if self.hamilton_circuit_helper(home_node, ham_path):
                    return True

                # Else, the path wasn't proper, so backtrack
                ham_path.pop(len(ham_path) - 1)
                self.distance -= edge['weight']

        return False

    # Combine the edges of min_weight and mst to form a connected multigraph.
    def add_matching_to_mst(self, min_matching):
        for u, v, weight in min_matching:
            self.mst.add_edge(u, v, weight=weight)


