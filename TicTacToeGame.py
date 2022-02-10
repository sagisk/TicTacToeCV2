#!/usr/bin/env python3
from math import inf as infinity
from random import choice
import platform
import time
from os import system
from GameBoard import Board

import cv2

HUMAN = -1
COMP = +1


class TicTacToe:
    def __init__(self, state, b):
        self.state = state
        self.b = b

    def evaluate(self):
        """
        Evaluates the state of the game.
        :return: +1 if the computer wins, -1 if the human wins, 0 draw
        """
        if self.wins(COMP):
            score = +1
        elif self.wins(HUMAN):
            score = -1
        else:
            score = 0
        return score

    def wins(self, player):
        """
        Tests if a specific player wins.
        :param player: a human or a computer
        :return: True if the player wins
        """
        win_state = [
            [self.state[0][0], self.state[0][1], self.state[0][2]],
            [self.state[1][0], self.state[1][1], self.state[1][2]],
            [self.state[2][0], self.state[2][1], self.state[2][2]],
            [self.state[0][0], self.state[1][0], self.state[2][0]],
            [self.state[0][1], self.state[1][1], self.state[2][1]],
            [self.state[0][2], self.state[1][2], self.state[2][2]],
            [self.state[0][0], self.state[1][1], self.state[2][2]],
            [self.state[2][0], self.state[1][1], self.state[0][2]],
        ]
        if [player, player, player] in win_state:
            return True
        else:
            return False

    def game_over(self):
        """
        Test if the human or computer wins
        :return: True if the human or computer wins
        """
        return self.wins(HUMAN) or self.wins(COMP)

    def empty_cells(self):
        """
        Adds empty cells into cells' list
        :return: a list of empty cells
        """
        cells = []
        for x, row in enumerate(self.state):
            for y, cell in enumerate(row):
                if cell == 0:
                    cells.append([x, y])
        return cells

    def valid_move(self, x, y):
        """
        A move is valid if the chosen cell is empty
        :param x: X coordinate
        :param y: Y coordinate
        :return: True if the board[x][y] is empty
        """
        if [x, y] in self.empty_cells():
            return True
        else:
            return False


    def set_move(self, x, y, player):
        """
        Set the move on board, if the coordinates are valid
        :param x: X coordinate
        :param y: Y coordinate
        :param player: the current player
        :return: True if the move is valid, else False
        """
        if self.valid_move(x, y):
            self.state[x][y] = player
            return True
        else:
            return False

    def minimax(self, depth, player):
        """
        AI function to choose the best move for the given state
        :param depth: node index in the tree (0 <= depth <= 9),
        but never nine in this case (see iaturn() function)
        :param player: an human or a computer
        :return: a list with [the best row, best col, best score]
        """
        if player == COMP:
            best = [-1, -1, -infinity]
        else:
            best = [-1, -1, +infinity]

        if depth == 0 or self.game_over():
            score = self.evaluate()
            return [-1, -1, score]

        for cell in self.empty_cells():
            x, y = cell[0], cell[1]
            self.state[x][y] = player
            score = self.minimax(depth - 1, -player)
            self.state[x][y] = 0
            score[0], score[1] = x, y

            if player == COMP:
                if score[2] > best[2]:
                    best = score  # max value
            else:
                if score[2] < best[2]:
                    best = score  # min value
        return best

    def ai_turn(self, imgCanvas, imgBoard, comp_choice):
        """
        It calls the minimax function if the depth < 9,
        else chooses a random coordinate.
        :param comp_choice: computer's choice X or O
        :return:
        """
        moves = {
            (0, 0): 0, (0, 1): 1, (0, 2): 2,
            (1, 0): 3, (1, 1): 4, (1, 2): 5,
            (2, 0): 6, (2, 1): 7, (2, 2): 8,
        }

        depth = len(self.empty_cells())
        if depth == 0 or self.game_over():
            print("AI wins")
            return

        if depth == 9:
            x = choice([0, 1, 2])
            y = choice([0, 1, 2])
        else:
            move = self.minimax(depth, COMP)
            x, y = move[0], move[1]

        self.set_move(x, y, COMP) 
        # draw move
        key = moves[(x, y)]
        xMin, xMax, yMin, yMax = imgBoard[key]
        if comp_choice=='X':
            self.b.drawX(imgCanvas, xMin, xMax, yMin, yMax)
        else:
            cv2.circle(imgCanvas, ((xMin+xMax)//2, (yMin+yMax)//2),
                                     25, (0,0,255))
            # self.b.drawO(imgCanvas, xMin, xMax, yMin, yMax)
        return x, y

    def human_turn(self, imgCanvas, lmList, gameBoard):
        """
        The Human plays choosing a valid move.
        :param c_choice: computer's choice X or O
        :return: void
        """
        moves = {
            0: [0, 0], 1: [0, 1], 2: [0, 2],
            3: [1, 0], 4: [1, 1], 5: [1, 2],
            6: [2, 0], 7: [2, 1], 8: [2, 2],
        }
        imgCanvas, move, res = gameBoard.detectCell(imgCanvas, lmList)
        coord = moves[move]
        if res == 1:
            can_move = self.set_move(coord[0], coord[1], HUMAN)

        depth = len(self.empty_cells())
        if depth == 0 or self.game_over():
            print('END')
            return