from random import random
import math

class Selectors(object):

    def roulettewheel(self, pop):

        n = len(pop[0].route)

        # create roulette
        roulette = [0] * (len(pop)+1)

        sum_fitness = sum(i.fitness for i in pop)
        i = 1
        while i < len(roulette):
            roulette[i] = roulette[i-1] + 1 - pop[i-1].fitness/sum_fitness
            i += 1

        parents_selection = []
        for i in range(0, len(pop)):
            # to wheel roulette and search parent selected with BS
            wheel = random() * roulette[-1]
            left = 0
            right = len(roulette)-1
            while True:
                mid = math.ceil((right+left)/2)
                if wheel >= roulette[mid-1] and wheel <= roulette[mid]:
                    parents_selection.append(pop[mid-1])
                    break
                
                if wheel < roulette[mid-1]:
                    right = mid-1
                else:
                    left = mid + 1

        return parents_selection