import timeit
from .data_processor import *
from .node import Node
from .models import Beer
from .matrix import Matrix

# Every solution will have 2 home nodes, as we have to get back home.
HOME_NODE_COUNT = 2
# Floating point precision for running time.
TIME_PRECISION = 4

# Defines solution to a beer test problem.
# Solution contains route, beers and other parameters.
class Solution(object):

    # If no parameters are passed, we initialize solution with empty values.
    def __init__(self, route = [], beers = [], distance = 0, time = 0, lat = 54.8985, long = 23.9036):
        self.route = route
        self.beers = beers
        self.distance_travelled = round(distance)
        self.running_time = round(time, TIME_PRECISION)
        self.home_lat = lat
        self.home_long = long
        self.beer_count = len(beers)
        self.brewery_count = len(route) - HOME_NODE_COUNT
        # With increased beer count we reduce distance. 
        # That is, fitness = distance / beer_count
        self.fitness = 0
    
    # Generates solution from given lat and long.
    def retrieve_solution(home_lat, home_long):
        solution = Solution()
        # Measure execution time.
        start = timeit.default_timer()
        nodes = Node.create_nodes(home_lat, home_long)

        # Avoid processing, if we don't have any reachable nodes.
        if len(nodes) > 1:
            matrix = Matrix()
            matrix.construct_distance_matrix(nodes)
            distance_travelled, route = TSP(matrix, nodes)
            stop = timeit.default_timer()
            solution = Solution(
                route, Beer.get_beers(route), distance_travelled, (stop - start), home_lat, home_long
            )
            solution.fitness = solution.distance_travelled / solution.beer_count
        return solution