import random
import matplotlib.pyplot as plt
import statistics
import time
from util import load_graph
from PopGenerator import PopGenerator
from GA import GA


random.seed()

instance = './data/kroa100.tsp'
graph = load_graph(instance)
m = 2
max_iters = 1000
experiments_count = 3

evaluators_conf = (GA.get_min_by_fitness, GA.get_min_by_penalty,
                   GA.get_min_by_DEB, GA.get_min_by_hierarchy)
breaks_generator_conf = (PopGenerator.generate_breaks_rules, PopGenerator.generate_breaks_fully_random,
                         PopGenerator.generate_breaks_fully_random, PopGenerator.generate_breaks_fully_random)
names_conf = ('Constrained generation', 'Penalization function',
              "Deb's rules", "Stochastic hierarchy")


print(instance+' '+str(m))
for i_conf in range(0, len(evaluators_conf)):
    print(names_conf[i_conf]+'\n')
    experiments_list = []
    evaluator = evaluators_conf[i_conf]
    generator = PopGenerator(graph, breaks_generator_conf[i_conf])
    total_time = 0
    feasible_count = 0
    for i in range(0, experiments_count):
        start = time.time()
        ga = GA(generator)
        result = ga.start(max_iters, graph, m, evaluator)
        end = time.time()
        total_time += end - start
        if result.best_individual.is_feasible():
            experiments_list.append(result)
            print(result.best_individual.fitness)
            feasible_count += 1

    best_fitnesses = [e.best_individual.fitness for e in experiments_list]
    experiments_list.sort(key=lambda x: x.best_individual.fitness)
    mid_exp = experiments_list[int(experiments_count/2)]
    print('\n' + names_conf[i_conf])
    print('feasible count:' + str(feasible_count))
    print('best: ' + str(min(best_fitnesses)))
    print('average: ' + str(statistics.mean(best_fitnesses)))
    print('std: ' + str(statistics.stdev(best_fitnesses)))
    # print('total time: ' + str(total_time))
    print('time per running: ' + str(total_time/experiments_count))
    print('============================\n')

    plt.plot(mid_exp.fitnesses, label=names_conf[i_conf])

    plt.title('kroa100, m='+str(m))
    plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    plt.ylabel('best fitness')
    plt.xlabel('iterations')
    plt.legend()
plt.show()
