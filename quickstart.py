from MancalaGUI import *
from GeneticAlgorithmTrainer import *

w = WeightChromosome(8, 5)
w.chromosome =  [9.2895948465511253, -5.5518479301435502, 3.7198795657176493, -4.994530957107699, 2.9397499989367311, 0.067329476348763961, -5.7550748932949647, 3.0386549697777028, 4.4171703527080091]

o = OperatorChromosome(7)
o.chromosome =  [0, 1, 0, 1, 1, 1, 1, 0]

a = AlgorithmChromosome(w, o)

p2 = arb495(2, Player.ABPRUNE, 9)
# p2.score = p2.custom_score(a)

startGame(Player(1, Player.HUMAN), p2)
