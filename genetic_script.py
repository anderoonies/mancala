from GeneticAlgorithmTrainer import *
from MancalaBoard import *

# w1 = WeightChromosome(4, 10)
# o1 = OperatorChromosome(3)
#
# w2 = WeightChromosome(4, 10)
# o2 = OperatorChromosome(3)
#
# a1 = AlgorithmChromosome(w1, o1)
# a2 = AlgorithmChromosome(w2, o2)
#
# c1, c2 = AlgorithmChromosome.crossover(a1, a2)
#
# print "Weight Parents: {}  {}\n Weight Children: {}  {}\n".format(w1.chromosome, w2.chromosome, c1.weight_chromosome.chromosome, c2.weight_chromosome.chromosome)

population = GeneticAlgorithm(TrainHeuristic()).run(100)

print "RESULTS:"

for alg_chromo in population:
    print "{} - {}".format(alg_chromo, TrainHeuristic().fitness(alg_chromo))
