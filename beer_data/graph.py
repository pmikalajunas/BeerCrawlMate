import networkx as nx
import copy

from beer_data.node import HOME_NODE
from beer_data.util import haversine


class Graph(object):

    def __init__(self, nodes):
        self.graph = nx.Graph()
        self.nodes = nodes
        # Add all the nodes.
        for node in nodes:
            self.graph.add_node(node)
        self.add_edges(nodes)

    # Returns distance from given to the home node.
    def get_home_distance(self, source):
        home_node = self.nodes[HOME_NODE]
        return self.get_distance(source, home_node)

    # Returns distance between given source to the given target node.
    def get_distance(self, source, target):
        edge = self.graph.get_edge_data(source, target, default=None)
        if edge is None:
            return 0
        return edge['weight']

    # Finds the node with minimum distance from the given node.
    # Returns a tuple (node, distance)
    # Where node is the minimum distance node.
    # And distance is the distance between two nodes.
    def get_min_distance(self, source):
        min = float('inf')
        node = self.nodes[HOME_NODE]

        for target in self.nodes:
            edge = self.graph.get_edge_data(source, target, default=None)
            if target == source or edge is None:
                continue
            if edge['weight'] < min and not target.visited:
                min = edge['weight']
                node = target
        return node, min

    # Add edges into the graph corresponding to the distance between two points.
    def add_edges(self, nodes):
        # Add edges into the graph corresponding to the distance between two points.
        for i in nodes:
            for j in nodes:
                if i is not j:
                    distance = haversine(i.lat, i.long, j.lat, j.long)
                    self.graph.add_edge(i, j, weight=distance)

    # Finds all the vertices with odd degree.
    def get_nodes_with_odd_degree(self):
        nodes = []
        for node in self.graph.nodes:
            if nx.degree(self.graph, node) % 2 == 1:
                nodes.append(node)
        return nodes

    def get_odd_node_subgraph(self):
        odd_nodes = self.get_nodes_with_odd_degree()
        return self.graph.subgraph(odd_nodes)

    def get_mst(self):
        return nx.minimum_spanning_tree(self.graph)


# Find a minimum-weight perfect matching M in the induced subgraph.
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
