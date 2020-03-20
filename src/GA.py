
import math
import random
import copy
import time
from random import randint
from PopGenerator import PopGenerator
from Selectors import Selectors
from Intraroute import Intraroute
from IndividualMTSP import IndividualMTSP
from GAResult import GAResult

class GA():

    def __init__(self, pop_generator):
        super().__init__()
        self.pop_generator = pop_generator

    def fitness_function(self, ind, graph):
        fitness_value = 0
        n = len(ind.route)
        i_break = 0
        for i in range(0, n):
            if i == n-1 or (i_break < len(ind.breaks) and  i+1 == ind.breaks[i_break]):
                fitness_value += graph[ind.route[i]
                                    ][ind.route[0 if i_break - 1 < 0 else ind.breaks[i_break-1]]]
                i_break += 1
            else:
                fitness_value += graph[ind.route[i]][ind.route[i+1]]
        ind.fitness = fitness_value
        return ind

    def tsp_fitness_function(self, tour, graph):
        fitness_value = 0
        n = len(tour)
        i_break = 0
        for i in range(0, n-1):
            fitness_value += graph[tour[i]][tour[i+1]]
        return fitness_value

    def ga_operation_IPGA(self, population, n, m, min_nodes, max_nodes, graph, evaluator_min):
        pop_size = len(population)
        offspring = []

        pop_suffled = random.sample(range(pop_size), pop_size)
        for i_bucket in range(0, pop_size, 10):
            
            # Step 1: Randomly select 10 individuals that have not been selected from the contemporary population
            i_pop_temp = pop_suffled[i_bucket:i_bucket+10]

            # Step 2: Find the best individual that has the best fitness in 10 individuals just selected
            pop_tmp = [population[i_pop_temp[i]] for i in range(0, 10)]
            best_tmp = evaluator_min(pop_tmp, min_nodes, max_nodes)

            # Step 3: Create a temporary population that consists of 10 individuals.
            # All of the 10 individuals are assigned to the best individual found in procedure 2
            pop_best = [copy.deepcopy(best_tmp) for i in range(0, 10)]

            # Step 4: Generate 2 random mutation segment selection points I and J,
            # and the mutation segment insertion location P
            intraroute = Intraroute()
            # intraroute.load_params(best_tmp)

            # Step 5: Mutate each individual in the temporary population created in
            # procedure 3 in different ways: do nothing, FlipInsert, SwapInsert,
            # LSlideInsert, RSlideInsert or Modify Breaks. The specific process
            # is as follows:

            # (1) Do nothing to the first individual.

            # (2) The second individual performs the FlipInsert operation.
            pop_best[1].route = intraroute.flipinsert(pop_best[1])

            # (3) The third individual performs the SwapInsert operation.
            pop_best[2].route = intraroute.swapinsert(pop_best[2])

            # (4) The fourth individual performs the LSlideInsert operation.
            pop_best[3].route = intraroute.lslideinsert(pop_best[3])

            # (5) The fifth individual performs the RSlideInsert operation.
            pop_best[4].route = intraroute.rslideinsert(pop_best[4])

            # (6) The sixth individual performs the Modify Breaks operation.
            pop_best[5].breaks = self.pop_generator.breaks_generator(n, m, min_nodes, max_nodes)

            # (7) The seventh individual performs the FlipInsert operation
            # and the Modify Breaks operation.
            pop_best[6].route = intraroute.flipinsert(pop_best[6])
            pop_best[6].breaks = self.pop_generator.breaks_generator(n, m, min_nodes, max_nodes)

            # (8) The eighth individual performs the SwapInsert operation
            # and the Modify Breaks operation.
            pop_best[7].route = intraroute.swapinsert(pop_best[7])
            pop_best[7].breaks = self.pop_generator.breaks_generator(n, m, min_nodes, max_nodes)

            # (9) The ninth individual performs the LSlideInsert operation
            # and the Modify Breaks operation.
            pop_best[8].route = intraroute.lslideinsert(pop_best[8])
            pop_best[8].breaks = self.pop_generator.breaks_generator(n, m, min_nodes, max_nodes)

            # (10) The tenth individual performs the RSlideInsert operation
            # and the Modify Breaks operation.
            pop_best[9].route = intraroute.lslideinsert(pop_best[9])
            pop_best[9].breaks = self.pop_generator.breaks_generator(n, m, min_nodes, max_nodes)

            # Join the temporary population that has already performed mutation operation into new population
            offspring += pop_best

        return offspring

    def compute_feasibility_degree(self, ind, min_nodes, max_nodes):
        breaks = [0]
        breaks.extend(ind.breaks)
        breaks.append(len(ind.route))
        feasibility = 0
        for i in range(0, len(breaks)-1):
            nodes_count = breaks[i+1]-breaks[i]
            if nodes_count < min_nodes:
                feasibility += min_nodes - nodes_count
            elif nodes_count > max_nodes:
                    feasibility += nodes_count - max_nodes

        ind.feasibility = feasibility
        return ind
                
    @staticmethod
    def deb_rules(ind1, ind2, min_nodes, max_nodes):

        # first case
        if ind1.is_feasible() and ind2.is_feasible():
            return ind1 if ind1.fitness < ind2.fitness else ind2

        # second case
        if not ind1.is_feasible() and not ind2.is_feasible():
            return ind1 if ind1.feasibility < ind2.feasibility else ind2

        # third case
        if ind1.is_feasible() and not ind2.is_feasible():
            return ind1
        if not ind1.is_feasible() and ind2.is_feasible():
            return ind2

    @staticmethod
    def get_min_by_DEB(population, min_nodes, max_nodes):
        best_tmp = population[0]
        for i in range(0, len(population)):
            best_tmp = GA.deb_rules(best_tmp, population[i], min_nodes, max_nodes) 

        return best_tmp

    @staticmethod
    def get_min_by_fitness(population, min_nodes, max_nodes):
        best_tmp = population[0]
        for i in range(0, len(population)):
            if population[i].fitness < best_tmp.fitness:
                best_tmp = population[i]

        return best_tmp

    @staticmethod
    def get_min_by_penalty(population, min_nodes, max_nodes):
        best_tmp = population[0]
        for i in range(0, len(population)):
            if population[i].p_f() < best_tmp.p_f():
                best_tmp = population[i]

        return best_tmp

    def start(self, graph, m, evaluator_min):

        n = len(graph)
        min_nodes = int(n/(m+1))
        max_nodes = int(n/(m-1))
        # min_nodes = 15
        # max_nodes = 30

        intraroute = Intraroute()

        population = self.pop_generator.create_population(100, n, m, min_nodes, max_nodes)
        best_global = None

        start = time.time()
        max_iters = 8000
        iter = 0
        data = []
        while iter < max_iters:
            # evaluate population
            population = [self.fitness_function(i, graph) for i in population]
            population = [self.compute_feasibility_degree(i, min_nodes, max_nodes) for i in population]
            
            # get best individual of this generation
            best_local = evaluator_min(population, min_nodes, max_nodes)
            data.append(best_local.fitness)    

            # replace global best if necessary
            if best_global is None:
                best_global = best_local
            else:
                best_global = evaluator_min([best_global, best_local], min_nodes, max_nodes)

            print(str(iter)+': '+str(best_local.fitness))

            # mutate full population
            population = self.ga_operation_IPGA(population, n, m, min_nodes, max_nodes, graph, evaluator_min)
            iter += 1

        result = GAResult(data, best_global)
        print('constraints violated: '+str(best_global.feasibility))
        print(best_global.route)
        print(best_global.breaks)
        print('best found: '+str(best_global.fitness))
        end = time.time()
        print('time elapsed: '+str(end - start))

        return result
