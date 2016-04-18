# File: Player.py
# Author(s) names AND netid's: Andy Bayer, arb495
# Date: 4/12/16
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm
# You will also define the score function in the MancalaPlayer class,
# a subclass of the Player class.

import itertools

from random import *
from decimal import *
from copy import *
from MancalaBoard import *
# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4

    def __init__(self, playerNum, playerType, ply=0):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)

    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score

    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            return 50.0

    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.
    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """

        # crib the code from minimaxMove
        move = -1
        score = -INFINITY
        alpha = -INFINITY
        beta = INFINITY
        turn = self

        for m in board.legalMoves(self):
            print "Thinking about {}, with alpha = {} and beta = {}".format(m, alpha, beta)
            if ply == 0:
                # return a tuple of the move and the score for it
                return (self.score(board), m)
            if board.gameOver():
                # nothing to do
                return -1, -1
            next_board = deepcopy(board)
            next_board.makeMove(self, m)
            opponent = Player(self.opp, self.type, self.ply)
            # check opponent's next move
            m_score = opponent.minAlphaBetaValue(next_board, ply - 1, turn, alpha, beta)
            print "That would have a score of {}".format(m_score)
            if m_score > score:
                print "My current move was {}, so I'm updating".format(score)
                # update current move if it's favorable
                move = m
                score = m_score

            # update alpha for next children
            alpha = max(score, alpha)
            print "---------------------"
        return score, move

    def maxAlphaBetaValue(self, board, ply, turn, alpha, beta):
        """ Find the alpha-beta value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            score = max(score, opponent.minAlphaBetaValue(nextBoard, ply - 1, turn, alpha, beta))
            # pruning condition: if the score is higher than beta value, there's nothing we can do
            if score >= beta:
                print "Pruning a path with value {}, beta of {}".format(score, beta)
                return score
            # update alpha for other children
            alpha = max(alpha, score)
        return score

    def minAlphaBetaValue(self, board, ply, turn, alpha, beta):
        """ Find the alpha-beta value for the next move for this player
        at a given board configuration. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            score = min(score, opponent.maxAlphaBetaValue(nextBoard, ply - 1, turn, alpha, beta))
            # pruning condition: if the score is lower than the alpha condition, there's nothing we can do
            if score <= alpha:
                print "Pruning a path with value {}, alpha of {}".format(score, alpha)
                return score
            # update beta for other children
            beta = min(beta, score)
        return score

    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            # print "chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            # print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            # TODO: Implement a custom player
            # You should fill this in with a call to your best move choosing
            # function.  You may use whatever search algorithm and scoring
            # algorithm you like.  Remember that your player must make
            # each move in about 10 seconds or less.
            cups = board.P1Cups if self.num == 1 else board.P2Cups
            val, move = self.minimaxMove(board, self.ply)
            # print "custom player using minimax, chose to move {} marbles from {} with val {}".format(cups[move-1], move, val)
            return move
        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be your netid
class arb495(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def custom_score(self, alg_ch):

        def score_func(board):
            score = 0
            attributes = []
            attributes += board.scoreCups
            attributes += board.P1Cups
            attributes += board.P2Cups

            operands = attributes

            weight_ch = alg_ch.weight_chromosome
            op_ch = alg_ch.operator_chromosome

            for i in xrange(len(attributes)):
                attributes[i] *= weight_ch.chromosome[i]

            iters = [iter(attributes), iter(op_ch.chromosome_to_operators())]
            expression = list(it.next() for it in itertools.cycle(iters))
            string_expression = ' '.join(str(x) for x in expression)

            try:
                score = eval(string_expression)
            except Exception as e:
                raise e

            return score

        return score_func

    def score(self, board):
        """ Evaluate the Mancala board for this player """
        # print "Calling score in arb495"

        # return self.custom_score(board, weights, operations)
        if board.hasWon(self.num):
          return 100.0
        elif board.hasWon(self.opp):
          return 0.0

        score = 0.0

        if self.num == 1:
          cups = board.P1Cups
          oppCups = board.P2Cups
          scoreCup = board.scoreCups[0]
          oppScoreCup = board.scoreCups[1]
        else:
          cups = board.P2Cups
          oppCups = board.P2Cups
          scoreCup = board.scoreCups[1]
          oppScoreCup = board.scoreCups[0]

        # iterate over our cups
        for i, marbles in enumerate(cups):
          # how far this move will take us
          endCup = i + marbles % 14
          # the distance between current cup and our mancala
          distanceToMancala = board.NCUPS - endCup
          if distanceToMancala == 0:
            # favor extras
            score += Constants.EXTRA_SCORE
          elif distanceToMancala > 0:
            # favor non-overflows
            score += Constants.NON_OVERFLOW_SCORE
          elif marbles == 0:
            # empty pits are good
            score += Constants.EMPTY_SCORE
          else:
            # don't favor overflows
            score += Constants.OVERFLOW_SCORE

        # iterate over opponent's cups
        for i, marbles in enumerate(oppCups):
          # punish leaving captures open
          if marbles == 0 and cups[1] > 0:
            score += Constants.CAPTURE_SCORE

        score += Constants.MANCALA_SCORE + Constants.OPP_MANCALA_SCORE

        # print "arb495 gave a board score of {}".format(score)

        return score
