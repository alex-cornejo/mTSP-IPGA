import random
from random import randint
from IndividualMTSP import IndividualMTSP


class PopGenerator(object):

    def __init__(self, graph, breaks_generator):
        super().__init__()
        self.graph = graph
        self.breaks_generator = breaks_generator

    def create_population(self, pop_size, n, m, min_nodes, max_nodes):

        # create population routes with random permutation of vertices
        pop_routes = [random.sample(range(n), n) for i in range(0, pop_size)]
        # pop_routes = [self.nearest_neighbor(
        #      self.graph) for i in range(0, pop_size)]

        # create population of breakpoints
        pop_breakpoints = [self.breaks_generator(
            n, m, min_nodes, max_nodes) for i in range(0, pop_size)]

        population = [IndividualMTSP(i[0], i[1])
                      for i in zip(pop_routes, pop_breakpoints)]
        return population

    @staticmethod
    def generate_breaks_rules(n, m, min_nodes, max_nodes=None):

        valid = False

        while valid is False:
            valid = True

            # Rule 1: Generate individual in increasing order
            breakpoints = sorted(random.sample(range(n), m-1))

            # Rule 2: The difference between every two adjacent numbers should not be less than min.
            for i in range(0, len(breakpoints)-1):
                if breakpoints[i+1] - breakpoints[i] < min_nodes or (max_nodes is not None and breakpoints[i+1] - breakpoints[i] > max_nodes):
                    valid = False
                    break

            if not valid:
                continue

            # Rule 3: The first number should not be less than min
            if breakpoints[0] < min_nodes or (max_nodes is not None and breakpoints[0] > max_nodes):
                valid = False
                continue

            # Rule 4: The difference between N and the last number should not be less than min
            if n - breakpoints[-1] < min_nodes or (max_nodes is not None and n - breakpoints[-1] > max_nodes):
                valid = False

        return breakpoints

    @staticmethod
    def generate_breaks_fully_random(n, m, min, max_nodes=None):
        breakpoints = sorted(random.sample(range(n), m-1))
        return breakpoints

    def nearest_neighbor(self, graph):
        n = len(graph)
        depot = randint(0, n-1)
        tour = [depot]

        for i in range(1, n):
            min_dist = None
            next_v = None
            for j in range(0, n):
                if i != j and j not in tour:
                    if min_dist is None or (min_dist > graph[tour[-1]][j]):
                        min_dist = graph[tour[-1]][j]
                        next_v = j
            tour.append(next_v)

        return tour
