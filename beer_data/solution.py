import timeit
from .data_processor import *

# Every solution will have 2 home nodes, as we have to get back home.
HOME_NODE_COUNT = 2
# Floating point precision for running time.
TIME_PRECISION = 4

# Defines solution to a beer test problem.
# Solution contains route, beers and other parameters.
class Solution:

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
    
    # Generates solution from given lat and long.
    def retrieve_solution(home_lat, home_long):
        solution = Solution()
        # Measure execution time.
        start = timeit.default_timer()
        nodes = create_nodes(home_lat, home_long)

        # Avoid processing, if we don't have any reachable nodes.
        if len(nodes) > 1:
            matrix = construct_distance_matrix(nodes)
            distance_travelled, route = TSP(matrix, nodes)
            stop = timeit.default_timer()
            solution = Solution(
                route, get_beers(route), distance_travelled, (stop - start), home_lat, home_long
            )
        return solution