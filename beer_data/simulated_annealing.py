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


    def search(self, matrix, nodes): 
        while self.T >= self.stopping_T:
            print("T: %f" % self.T)
            print('_______________________________________')
            route = list(self.solution.route)
            # Pick one node from the current route.
            node_a = random.randint(1, self.N - 1)
            # Pick one node from reachable nodes.
            node_b = random.randint(1, len(nodes) - 1)

            print('node_a: %d node_b %d' % (node_a, node_b))
            # Put the
            
            # If the node is not in the route, swap the nodes.
            if not nodes[node_b].visited:
                route[node_a] = nodes[node_b]
                nodes[node_b].visited = True
            # Otherwise both nodes are already in the current route.    
            else:
                b_index = self.find_index(route, nodes[node_b])
                route[node_a], route[b_index] = route[b_index], route[node_a]
                
            self.accept(route, matrix)
            self.T *= self.alpha
            self.fitness_list.append(self.fitness)


        if self.fitness_list:
            print("Best fitness obtained: ", self.best_fitness)
            improvement = 100 * (self.fitness_list[0] - self.best_fitness) / (self.fitness_list[0])
            print(f"Improvement over greedy heuristic: {improvement : .2f}%")
        return (self.best_route, self.best_fitness)


    def find_index(self, route, node):
        for i in range(len(route)):
            if route[i] == node:
                return i
        return -1

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
