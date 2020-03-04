import networkx as nx
import copy

from .util import haversine

# Id of the starting(home) node.
HOME_NODE = 0
# Distance after
DISTANCE_LOWER_BOUND = 1750
# Overall distance limit that we can't exceed.
DISTANCE_HIGHER_BOUND = 2000


class Christofides(object):

    def __init__(self, nodes):
        self.graph = nx.Graph()
        self.nodes = nodes
        # Add all the nodes.
        for node in nodes:
            self.graph.add_node(node)
        self.add_edges(nodes, self.graph)
        self.mst = nx.minimum_spanning_tree(self.graph)
        self.distance = 0
        self.route = []

    # Performs search using Christofides algorithm.
    # Find a minimum-weight perfect matching min_weight in the subgraph given by the vertices from odd_nodes
    # Combine the edges of min_weight and mst to form a connected multigraph H in which each vertex has even degree.
    def search(self):
        odd_nodes = self.get_nodes_with_odd_degree(self.mst)
        subgraph = self.graph.subgraph(odd_nodes)

        min_weight = self.min_weight_matching(subgraph)

        self.add_matching_to_mst(min_weight)
        path = self.hamilton_circuit(self.nodes[HOME_NODE])
        return path, self.distance

    # Returns optimal path.
    def hamilton_circuit(self, home_node):
        ham_path = [home_node]
        path_found = self.hamilton_circuit_helper(self.mst, home_node, ham_path)

        if not path_found:
            return None

        return ham_path

    # Make a Hamilton circuit by skipping repeated vertices.
    # Path can be considered as finished once distance is between ...
    # DISTANCE_LOWER_BOUND and DISTANCE_HIGHER_BOUND
    # Then, we try to go to the home node, if we can't, we backtrack.
    def hamilton_circuit_helper(self, graph, home_node, ham_path):

        if DISTANCE_LOWER_BOUND < self.distance < DISTANCE_HIGHER_BOUND:
            distance_to_home = haversine(
                ham_path[-1].lat, ham_path[-1].long, self.nodes[HOME_NODE].lat, self.nodes[HOME_NODE].long
            )
            distance = self.distance + distance_to_home
            if distance < DISTANCE_HIGHER_BOUND:
                ham_path.append(home_node)
                self.distance += distance_to_home
                return True
            else:
                return False

        for node in graph.nodes:
            edge = graph.get_edge_data(ham_path[-1], node, default=None)

            if edge is not None and node not in ham_path:
                ham_path.append(node)
                node.distance = round(edge['weight'], 2)
                self.distance += edge['weight']
                if self.hamilton_circuit_helper(graph, home_node, ham_path):
                    return True

                # Else, the path wasn't proper, so backtrack
                ham_path.pop(len(ham_path) - 1)
                self.distance -= edge['weight']

        return False

    # Combine the edges of min_weight and mst to form a connected multigraph.
    def add_matching_to_mst(self, min_matching):
        for u, v, weight in min_matching:
            self.mst.add_edge(u, v, weight=weight)

    @staticmethod
    # Add edges into the graph corresponding to the distance between two points.
    def add_edges(nodes, graph):
        # Add edges into the graph corresponding to the distance between two points.
        for i in nodes:
            for j in nodes:
                if i is not j:
                    distance = haversine(i.lat, i.long, j.lat, j.long)
                    graph.add_edge(i, j, weight=distance)
                    x = i
                    y = j

    @staticmethod
    # Finds all the vertices with odd degree.
    def get_nodes_with_odd_degree(graph):
        nodes = []
        for node in graph.nodes:
            if nx.degree(graph, node) % 2 == 1:
                nodes.append(node)
        return nodes

    @staticmethod
    # Find a minimum-weight perfect matching M in the induced subgraph given the vertices from O.
    def min_weight_matching(graph):
        nodes = copy.copy(set(graph.nodes))
        matching = set()

        while nodes:
            v = nodes.pop()
            min_weight = float('inf')
            closest = None

            for u in nodes:
                edge = graph.get_edge_data(u, v, default=None)
                if edge is not None and edge['weight'] < min_weight:
                    min_weight = edge['weight']
                    closest = u

            matching.add((v, closest, min_weight))
            nodes.remove(closest)

        return matching
