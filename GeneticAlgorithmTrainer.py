
"""Genetic Algorithmn Implementation
see:
http://www.obitko.com/tutorials/genetic-algorithms/ga-basic-description.php
"""

from random import uniform, getrandbits, randint
from functools import partial
import sys
import pdb

# from MancalaBoard import *
from Player import *

class AlgorithmChromosome():
    def __init__(self, weight_ch, op_ch):
        self.weight_chromosome = weight_ch
        self.operator_chromosome = op_ch

    def __str__(self):
        return "{} {}\n".format(self.weight_chromosome.chromosome, self.operator_chromosome.chromosome)

    def mutate(self):
        vary = uniform(-2, 2)
        w_i = randint(0, len(self.weight_chromosome.chromosome) - 1)
        o_i = randint(0, len(self.operator_chromosome.chromosome) - 1)
        self.weight_chromosome.chromosome[w_i] += vary
        self.operator_chromosome.chromosome[o_i] ^= 1
        return self

    @staticmethod
    def crossover(p1, p2):
        """ Makes two children from parents, randomly crossed over between two indices. """

        p1_weight_ch = p1.weight_chromosome.chromosome
        p1_op_ch = p1.operator_chromosome.chromosome
        p2_weight_ch = p2.weight_chromosome.chromosome
        p2_op_ch = p2.operator_chromosome.chromosome

        w_i1 = randint(1, len(p1_weight_ch) - 2)
        w_i2 = randint(1, len(p1_weight_ch) - 2)
        o_i1 = randint(1, len(p1_op_ch) - 1)
        o_i2 = randint(1, len(p1_op_ch) - 1)

        if w_i1 > w_i2: w_i1, w_i2 = w_i2, w_i1
        if o_i1 > o_i2: o_i1, o_i2 = o_i2, o_i1

        c1_weight = p1.weight_chromosome
        c1_op = p1.operator_chromosome

        c2_weight = p2.weight_chromosome
        c2_op = p2.operator_chromosome

        c1_weight.chromosome = p1_weight_ch[:w_i1] + p2_weight_ch[w_i1:w_i2] + p1_weight_ch[w_i2:]
        c1_op.chromosome = p1_op_ch[:o_i1] + p2_op_ch[o_i1:o_i2] + p1_op_ch[o_i2:]


        c2_weight.chromosome = p2_weight_ch[:w_i1] + p1_weight_ch[w_i1:w_i2] + p2_weight_ch[w_i2:]
        c2_op.chromosome = p2_op_ch[:o_i1] + p1_op_ch[o_i1:o_i2] + p2_op_ch[o_i2:]

        child1 = AlgorithmChromosome(c1_weight, c1_op)
        child2 = AlgorithmChromosome(c2_weight, c2_op)

        return (child1, child2)


class WeightChromosome():
    def __init__(self, n_weights, spread):
        self.chromosome = [self.random_gene(spread) for i in xrange(n_weights)]

    def random_gene(self, spread):
        return uniform((0 - spread), spread)

    def chromosome_to_weights(self):
        return self.chromosome


class OperatorChromosome():
    def __init__(self, n_operators):
        self.chromosome = []
        for i in xrange(n_operators):
            self.chromosome += self.random_gene(1)

        self.encoding = {
            '0': '+',
            '1': '-',
            # '[0, 1, 0]': '*',
            # '[0, 1, 1]': '+',
            # '[1, 0, 0]': '-',
            # '[1, 0, 1]': '+',
            # '[1, 1, 0]': '*',
            # '[1, 1, 1]': '+',
        }

    def random_gene(self, n_bits):
        return [int(getrandbits(1)) for i in xrange(n_bits)]

    def chromosome_to_operators(self):
        operators = []
        for i in xrange(0, len(self.chromosome)):
            operators.append(self.encoding[str(self.chromosome[i])])
        return operators


class GeneticAlgorithm(object):
    def __init__(self, genetics):
        self.genetics = genetics
        pass

    def run(self, n_iterations):
        population = self.genetics.initial()
        n = 0
        while n < n_iterations:
            print "Population interation {0}".format(n)
            n += 1
            fits_pop = [(self.genetics.fitness(alg_chromo, population), alg_chromo) for alg_chromo in population]
            if self.genetics.check_stop(fits_pop): break
            population = self.next(fits_pop)
        return population

    def next(self, fits):
        parents_generator = self.genetics.parents(fits)
        size = len(fits)
        nexts = []
        while len(nexts) < size:
            parents = next(parents_generator)
            cross = random() < self.genetics.probability_crossover()
            children = self.genetics.crossover(parents) if cross else parents
            for ch in children:
                mutate = random() < self.genetics.probability_mutation()
                nexts.append(self.genetics.mutation(ch) if mutate else ch)
                pass
            pass
        return nexts[0:size]
    pass

class GeneticFunctions(object):
    def probability_crossover(self):
        r"""returns rate of occur crossover(0.0-1.0)"""
        return 1.0

    def probability_mutation(self):
        r"""returns rate of occur mutation(0.0-1.0)"""
        return 0.0

    def initial(self):
        r"""returns list of initial population
        """
        return []

    def fitness(self, chromosome):
        r"""returns domain fitness value of chromosome
        """
        return len(chromosome)

    def check_stop(self, fits_populations):
        r"""stop run if returns True
        - fits_populations: list of (fitness_value, chromosome)
        """
        return False

    def parents(self, fits_populations):
        r"""generator of selected parents
        """
        gen = iter(sorted(fits_populations))
        while True:
            f1, ch1 = next(gen)
            f2, ch2 = next(gen)
            yield (ch1, ch2)
            pass
        return

    def crossover(self, parents):
        r"""breed children
        """
        return parents

    def mutation(self, chromosome):
        r"""mutate chromosome
        """
        return chromosome
    pass


class TrainHeuristic(GeneticFunctions):
    def __init__(self, limit=200, size=100,
                 prob_crossover=0.9, prob_mutation=0.2):
        # self.target = self.al(target_text)
        self.counter = 0

        self.limit = limit
        self.size = size
        self.prob_crossover = prob_crossover
        self.prob_mutation = prob_mutation

    # GeneticFunctions interface impls
    def probability_crossover(self):
        return self.prob_crossover

    def probability_mutation(self):
        return self.prob_mutation

    def initial(self):
        return [AlgorithmChromosome(
                    (WeightChromosome(9, 10)),
                    OperatorChromosome(8)
                ) for i in xrange(self.size)]

    def fitness(self, p1_chromo, population):
        player1 = arb495(1, Player.ABPRUNE, 2)
        player1.score = player1.custom_score(p1_chromo)
        player2 = arb495(2, Player.ABPRUNE, 2)

        board = MancalaBoard()

        wins = 0.0

        for p2_chromo in population:
            player2.score = player2.custom_score(p2_chromo)

            # play some games!
            board.hostGame(player1, player2)
            if board.hasWon(1):
                wins += 1.0
            board.reset()

        return wins/len(population)

    def check_stop(self, fits_populations):
        self.counter += 1
        best_match = list(sorted(fits_populations))[-1][1]
        fits = [f for f, ch in fits_populations]
        best = max(fits)
        worst = min(fits)
        ave = sum(fits) / len(fits)
        print(
            "[G {0}] score=({1}, {2}, {3}): {4}".format(
                self.counter, best, ave, worst, best_match)
            )
        pass
        return best_match > 8.0 and ave > 5.0

    def parents(self, fits_populations):
        while True:
            father = self.tournament(fits_populations)
            mother = self.tournament(fits_populations)
            yield (father, mother)
            pass
        pass

    def crossover(self, parents):
        parent1, parent2 = parents
        return AlgorithmChromosome.crossover(parent1, parent2)

    def mutation(self, chromosome):
        return chromosome.mutate()

    # internals
    def tournament(self, fits_populations):
        alicef, alice = self.select_random(fits_populations)
        bobf, bob = self.select_random(fits_populations)
        # print "In tournament between {} ({}) and {} ({})".format(alice, alicef, bob, bobf)
        return alice if alicef > bobf else bob

    def select_random(self, fits_populations):
        return fits_populations[randint(0, len(fits_populations)-1)]
