import networkx as nx
import copy

from .util import haversine

HOME_NODE = 0

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

    def tsp_circuit(self, nodes):

        odd_nodes = self.get_nodes_with_odd_degree(self.mst)
        subgraph = self.graph.subgraph(odd_nodes)

        min_weight = self.min_weight_matching(subgraph)

        self.add_matching_to_mst(min_weight)
        path = self.hamilton_circuit(self.nodes[HOME_NODE])
        return path, self.distance


    def hamilton_circuit(self, source):
        ham_path = [source]

        path_found = self.hamilton_circuit_helper(self.mst, source, ham_path)

        if not path_found:
            return None

        return ham_path

    def hamilton_circuit_helper(self, graph, source, ham_path):

        if 1800 < self.distance < 2000:
            distance_to_source = haversine(
                ham_path[-1].lat, ham_path[-1].long, self.nodes[HOME_NODE].lat, self.nodes[HOME_NODE].long
            )
            distance = self.distance + distance_to_source
            if distance < 2000:
                ham_path.append(source)
                self.distance += distance_to_source
                return True
            else:
                return False

        for node in graph.nodes:
            edge = graph.get_edge_data(ham_path[-1], node, default=None)

            if edge is not None and node not in ham_path:
                ham_path.append(node)
                self.distance += edge['weight']
                if self.hamilton_circuit_helper(graph, source, ham_path):
                    return True

                # Else, the path wasn't proper, so backtrack
                ham_path.pop(len(ham_path) - 1)
                self.distance -= edge['weight']

        return False


    def add_matching_to_mst(self, min_matching):
        for u, v, weight in min_matching:
            self.mst.add_edge(u, v, weight=weight)



    @staticmethod
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
    def get_nodes_with_odd_degree(graph):
        nodes = []
        for node in graph.nodes:
            if nx.degree(graph, node) % 2 == 1:
                nodes.append(node)
        return nodes


    @staticmethod
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
