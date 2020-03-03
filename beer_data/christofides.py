import networkx as nx
import copy

from .util import haversine


def min_weight_matching(G, nodess):
    nodes = copy.deepcopy(set(G.nodes))

    matching = set()

    a = G.get_edge_data(nodess[212], nodess[59], default=None)

    while nodes:
        v = nodes.pop()
        min_weight = float('inf')
        closest = None

        if not nodes:
            raise ValueError("G has an odd number of nodes")

        edge1 = G.get_edge_data(0, 1, default=None)
        a = nodes.pop()
        edge2 = G.get_edge_data(v, a, default=None)

        for u in nodes:
            edge = G.get_edge_data(u, v, default=None)
            if edge is not None and edge['weight'] < min_weight:
                min_weight = edge['weight']
                closest = u

        matching.add((v, closest, min_weight))
        nodes.remove(closest)

    return matching


class Christofides(object):

    def __init__(self):
        self.graph = nx.Graph()

    def tsp_circuit(self, nodes):

        # Add all the nodes.
        for node in nodes:
            self.graph.add_node(node)

        self.add_edges(nodes, self.graph)

        x = None
        y = None

        a = self.graph.get_edge_data(nodes[0], nodes[188], default=None)

        mst = nx.minimum_spanning_tree(self.graph)

        a = mst.get_edge_data(nodes[0], nodes[188], default=None)

        # odd_nodes = self.get_nodes_with_odd_degree(mst)
        # subgraph = self.graph.subgraph(odd_nodes)
        # a = subgraph.get_edge_data(nodes[212], nodes[59], default=None)

        min_weight = min_weight_matching(mst, nodes)

        print(min_weight)


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
