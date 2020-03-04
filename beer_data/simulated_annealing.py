import random
import math

from beer_data.node import MAX_DISTANCE
from beer_data.solution import Beer
from beer_data.util import find_index, get_overall_distance

# Every solution will have 2 home nodes, as we have to get back home.
HOME_NODE_COUNT = 2


class SimulatedAnnealing(object):

    def __init__(self, solution, alpha):
        # Solution generated using greedy heuristic (nearest-neighbour).
        self.solution = solution
        self.N = len(solution.route)
        # Temperature is proportional to node count in route.
        self.T = len(solution.route)
        # Stopping temperature defines when we stop our search.
        self.stopping_T = 1e-5
        # Alpha is the coefficient by which temperature will be decreased.
        self.alpha = alpha
        # Fitness of the solution is beer count + brewery count.
        self.fitness = solution.fitness
        self.best_fitness = solution.fitness
        self.route = solution.route
        self.best_route = solution.route
        self.fitness_list = [solution.fitness]
        # Improvement over greedy heuristic (percentage).
        self.improvement = 0
        # Distance that we have travelled.
        self.distance = solution.distance_travelled
        self.best_distance = solution.distance_travelled

    # TODO: Unecessary O(n) we could update distance of the nodes that changed.
    # Simulated Annealing search, that randomly picks two nodes to be swapped.
    # One from current route, another from a list of reachable nodes.
    # Probability of accepting lower quality solution decreases with temperature.
    def search(self, matrix, nodes):
        while self.T >= self.stopping_T:
            # Create a temporary route.
            route = list(self.solution.route)
            # Pick one node from the current route, avoid home nodes.
            node_a = random.randint(1, self.N - 2)
            # Pick one node from reachable nodes, avoid home node.
            node_b = random.randint(1, len(nodes) - 1)

            # If the node is not in the route, bring the node in.
            if not nodes[node_b].visited:
                route[node_a] = nodes[node_b]
                nodes[node_b].visited = True
                distance = get_overall_distance(matrix, route)
            # If both are in current route, swap them.
            else:
                b_index = find_index(route, nodes[node_b])
                route[node_a], route[b_index] = route[b_index], route[node_a]
                distance = get_overall_distance(matrix, route)

            self.accept(route, distance)
            self.T *= self.alpha
            self.fitness_list.append(self.fitness)

        if self.fitness_list:
            # Improvement over greedy heuristic (percentage).
            self.improvement = ((self.best_fitness * 100) / (self.fitness_list[0])) - 100

    # Accepts/rejects the altered solution.
    # If solution's current fitness is better, it accepts it.
    # Based on probability and temperature, accepts the solution even if it's worse.
    def accept(self, route, distance):
        # Fitness is beer count added with the brewery count.
        route_fitness = (len(route) - HOME_NODE_COUNT) + len(Beer.get_beers(route))

        # Solution should not exceed the travel limitations.
        if distance > MAX_DISTANCE:
            return

        if route_fitness > self.fitness:
            self.fitness, self.route = route_fitness, route
            self.distance = distance
            if route_fitness > self.best_fitness:
                self.best_fitness, self.best_route = route_fitness, route
                self.best_distance = distance
        else:
            if random.random() < self.p_accept(route_fitness):
                self.fitness, self.route = route_fitness, route
                self.distance = distance

    # Probability of accepting if the candidate is worse than current.
    # Depends on the current temperature and difference between candidate and current.
    def p_accept(self, route_fitness):
        return math.exp(-abs(route_fitness - self.fitness) / self.T)
