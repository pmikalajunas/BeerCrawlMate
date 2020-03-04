import timeit
from .nearest_neighbour import *
from .node import Node
from .models import Beer
from .matrix import Matrix
from .christofides import Christofides
from beer_data.simulated_annealing import SimulatedAnnealing

# Every solution will have 2 home nodes, as we have to get back home.
HOME_NODE_COUNT = 2
# Floating point precision for running time.
TIME_PRECISION = 4
# Factor by which temperature will be decreased with each Annealing iteration.
ALPHA = 0.95

# In case you get lost, go back to the city that you love the most.
LAT_KAUNAS = 54.8985
LONG_KAUNAS = 23.9036


# Defines solution to a beer test problem.
# Solution contains route, beers and other parameters.
class Solution(object):

    # If no parameters are passed, we initialize solution with empty values.
    def __init__(self, route=[], beers=[], distance=0, time=0, lat=LAT_KAUNAS, long=LONG_KAUNAS):
        self.route = route
        self.beers = beers
        self.distance_travelled = round(distance)
        self.running_time = round(time, TIME_PRECISION)
        self.home_lat = lat
        self.home_long = long
        self.beer_count = len(beers)
        self.brewery_count = len(route) - HOME_NODE_COUNT
        self.fitness = self.brewery_count + self.beer_count
        # Improvement over greedy heuristic (percent), only set if other algorithm is used.
        self.improvement = 0


# Generates solution from given lat and long.
def retrieve_solution(home_lat, home_long, algorithm):
    solution = Solution()
    nodes = Node.create_nodes(home_lat, home_long)

    # Avoid processing, if we don't have any reachable nodes.
    if len(nodes) > 1:
        if algorithm == 'Nearest Neighbour':
            solution, matrix = get_nn_solution(nodes, home_lat, home_long)
            return solution

        elif algorithm == 'Christofides':
            return get_christofides_solution(nodes, home_lat, home_long)

        elif algorithm == 'Simulated Annealing':
            return get_sa_solution(nodes, home_lat, home_long)

    return solution


def get_sa_solution(nodes, home_lat, home_long):
    # Generate initial greedy solution and then alter.
    solution, matrix = get_nn_solution(nodes, home_lat, home_long)
    greedy_time = solution.running_time

    start = timeit.default_timer()
    annealing = SimulatedAnnealing(solution, ALPHA)
    annealing.search(matrix, nodes)
    stop = timeit.default_timer()

    time = greedy_time + (stop - start)
    beers = Beer.get_beers(annealing.best_route)

    solution = Solution(
        annealing.best_route, beers, annealing.best_distance, time, home_lat, home_long
    )
    solution.improvement = round(annealing.improvement, 2)


def get_christofides_solution(nodes, home_lat, home_long):
    start = timeit.default_timer()
    christofides = Christofides(nodes)
    route, distance_travelled = christofides.tsp_circuit(nodes)
    stop = timeit.default_timer()
    solution = Solution(
        route, Beer.get_beers(route), distance_travelled, (stop - start), home_lat, home_long
    )
    return solution


def get_nn_solution(nodes, home_lat, home_long):
    start = timeit.default_timer()
    matrix = Matrix()
    matrix.construct_distance_matrix(nodes)

    nn = NearestNeighbour(nodes, matrix)
    nn.search()

    stop = timeit.default_timer()
    solution = Solution(
        nn.route, Beer.get_beers(nn.route), nn.distance, (stop - start), home_lat, home_long
    )
    return solution, matrix
