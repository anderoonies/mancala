from TicTacToe import *
from Player import *

p1 = Player(1, Player.HUMAN)
p2 = Player(2, Player.ABPRUNE, 10)

ttt = TTTBoard()
ttt.hostGame(p1, p2)
