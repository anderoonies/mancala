from MancalaGUI import *
from GeneticAlgorithmTrainer import *

w = WeightChromosome(14, 5)
w.chromosome = [-19.324693584065173, -8.5211372453045779, -7.0681502161954599, -2.6632353034934324, 6.4298546416384657, -1.1518015250488278, -0.15603487405772043, -5.2061468861846825, -2.5765429665544115, -8.0580530708738731, 5.4702788919164895, 6.1139516513237826, 16.860081778662668, -11.596907844699503]

o = OperatorChromosome(13)
o.chromosome = [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0]

a = AlgorithmChromosome(w, o)

p2 = arb495(2, Player.ABPRUNE, 5)
p2.score = p2.custom_score(a)

startGame(Player(1, Player.HUMAN), p2)
