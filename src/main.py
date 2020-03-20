import random
import matplotlib.pyplot as plt

from util import load_graph
from PopGenerator import PopGenerator
from GA import GA


random.seed(0)

instance = './data/kroa100.tsp'
graph = load_graph(instance)
m = 3

evaluator = GA.get_min_by_penalty
generator = PopGenerator(graph, PopGenerator.generate_breaks_fully_random)

ga = GA(generator)
result = ga.start(graph, m, evaluator) 

plt.plot(result.fitnesses)
plt.ylabel('best fitness')
plt.show()