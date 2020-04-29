class GAResult(object):
    
    def __init__(self, fitnesses, best_individual, feasible_list):
        self.fitnesses = fitnesses
        self.best_individual = best_individual
        self.feasible_list = feasible_list
