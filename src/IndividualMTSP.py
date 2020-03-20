class IndividualMTSP(object):
    
    fitness = None  #fitness value of individual
    feasibility = None  # degree of feasibility of individual

    def __init__(self, route, breaks):
        super().__init__()
        self.route = route
        self.breaks = breaks

    def is_feasible(self):
        if self.feasibility is None:
            raise 
        return self.feasibility == 0

    # penalized fitness value
    def p_f(self):
        n = len(self.route)
        return self.fitness*(1+self.feasibility/n)