import random
import math

class SimulatedAnnealing(object):

    def __init__(self, solution, alpha):
        self.solution = solution
        self.N = len(solution.route)
        self.T = len(solution.route)
        self.stopping_T = 1e-5
        # Alpha is the coefficient by which temperature will be decreased.
        self.alpha = alpha
        self.fitness = solution.fitness
        self.best_fitness = solution.fitness
        self.route = solution.route
        self.best_route = solution.route
        self.fitness_list = []


    def search(self, matrix):     
        while self.T >= self.stopping_T:
            print("T: %f" % self.T)
            print('_______________________________________')
            route = list(self.solution.route)
            # Last node is the home node, exclude it from swapping.
            node_a = random.randint(2, self.N - 1)
            node_b = random.randint(0, self.N - node_a)
            print('node_a: %d node_b %d' % (node_a, node_b))
            # Swap the nodes.
            route[node_a : (node_a + node_b)] = reversed(route[node_a : (node_a + node_b)])
            self.accept(route, matrix)
            self.T *= self.alpha
            self.fitness_list.append(self.fitness)

        if self.fitness_list:
            print("Best fitness obtained: ", self.best_fitness)
            improvement = 100 * (self.fitness_list[0] - self.best_fitness) / (self.fitness_list[0])
            print(f"Improvement over greedy heuristic: {improvement : .2f}%")


        
    def accept(self, route, matrix):

        route_fitness = matrix.get_route_fitness(route)
        print("new fitness: %f old fitness: %f best fitness: %f" % (route_fitness, self.fitness, self.best_fitness))
        if route_fitness < self.fitness:
            self.fitness, self.route = route_fitness, route
            if route_fitness < self.best_fitness:
                self.best_fitness, self.best_route = route_fitness, route
        else:
            if random.random() < self.p_accept(route_fitness):
                self.fitness, self.route = route_fitness, route
    

    # Probability of accepting if the candidate is worse than current.
    # Depends on the current temperature and difference between candidate and current.
    def p_accept(self, route_fitness):
        return math.exp(-abs(route_fitness - self.fitness) / self.T)
