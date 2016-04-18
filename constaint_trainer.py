from __future__ import division
from random import uniform

from MancalaGUI import *
import MancalaConstants as Constants


def adjust(constant, win_counter, loss_counter):
  rand_choice = uniform(-5.0, 5.0)
  win_weight =  loss_counter / (win_counter + 1)
  return constant + win_weight * rand_choice

def run_trials():
  hero = arb495(1, Player.CUSTOM)
  opponent = Player(2, Player.RANDOM)

  board = MancalaBoard()

  game_counter = 0
  loss_counter = 0
  win_counter = 0

  ntrials = input("n trials: ")
  while ntrials > 0:
    ntrials -= 1
    board.hostGame(opponent, hero)
    game_counter += 1
    if board.hasWon(2):
      loss_counter += 1
      # very bad, opponent has succeeded
      Constants.EXTRA_SCORE = adjust(Constants.EXTRA_SCORE, win_counter, loss_counter)
      Constants.NON_OVERFLOW_SCORE = adjust(Constants.NON_OVERFLOW_SCORE, win_counter, loss_counter)
      Constants.EMPTY_SCORE = adjust(Constants.EMPTY_SCORE, win_counter, loss_counter)
      Constants.OVERFLOW_SCORE = adjust(Constants.OVERFLOW_SCORE, win_counter, loss_counter)
      Constants.CAPTURE_SCORE = adjust(Constants.CAPTURE_SCORE, win_counter, loss_counter)
      Constants.MANCALA_SCORE = adjust(Constants.MANCALA_SCORE, win_counter, loss_counter)
      Constants.OPP_MANCALA_SCORE = adjust(Constants.OPP_MANCALA_SCORE, win_counter, loss_counter)
    else:
      win_counter += 1


  print "{}/{}".format(win_counter, game_counter)
  print "{}: Constants.EXTRA_SCORE".format(Constants.EXTRA_SCORE)
  print "{}: Constants.NON_OVERFLOW_SCORE".format(Constants.NON_OVERFLOW_SCORE)
  print "{}: Constants.EMPTY_SCORE".format(Constants.EMPTY_SCORE)
  print "{}: Constants.OVERFLOW_SCORE".format(Constants.OVERFLOW_SCORE)
  print "{}: Constants.CAPTURE_SCORE".format(Constants.CAPTURE_SCORE)
  print "{}: Constants.MANCALA_SCORE".format(Constants.MANCALA_SCORE)
  print "{}: Constants.OPP_MANCALA_SCORE".format(Constants.OPP_MANCALA_SCORE)

if __name__ == '__main__':
  run_trials()

