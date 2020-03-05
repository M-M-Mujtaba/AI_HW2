# import the pygame module, so you can use it

# Constants and configuration options.
import ui
import utility
import pygame
from copy import deepcopy

import random

EMPTY = 0
BLACK = 1
WHITE = 2
INFINITY = 999999999
MAX = 0
MIN = 1
DEFAULT_LEVEL = 1
HUMAN = "human"
COMPUTER = "computer"
Board_Size = 8


# simple color inverter
def change_color(color):
    if color == BLACK:
        return WHITE
    else:
        return BLACK


# it is us , we human we good
class Human:

    def __init__(self, gui, color="white"):
        self.color = color
        self.gui = gui

    def get_move(self):
        """ Uses gui to handle mouse
        """
        validMoves = self.current_board.get_valid_moves(self.color)
        while True:
            move = self.gui.get_mouse_input()
            if move in validMoves:
                break
        self.current_board.apply_move(move, self.color)
        return 0, self.current_board

    def get_current_board(self, board):
        self.current_board = board


class Computer(object):

    def __init__(self, color, prune=3):
        self.depthLimit = prune
        self.color = color

    def get_current_board(self, board):
        self.current_board = board

    def get_move(self):
        return utility.our_minimax(self.current_board, None, self.depthLimit, self.color,
                                   change_color(self.color), False)


class Board:
    """ Rules of the game """

    def __init__(self):
        global Board_Size
        self.board = [[0 for i in range(Board_Size)] for i in range(Board_Size)]
        self.board[(Board_Size // 2) - 1][Board_Size // 2] = BLACK
        self.board[Board_Size // 2][(Board_Size // 2) - 1] = BLACK
        self.board[(Board_Size // 2) - 1][(Board_Size // 2) - 1] = WHITE
        self.board[Board_Size // 2][Board_Size // 2] = WHITE
        self.valid_moves = []

    def lookup(self, row, column, color):
        # all the valid moves by a player stored in places(can be diagonal,vertical , horizontal etc
        if color == BLACK:
            other = WHITE
        else:
            other = BLACK

        places = []

        #edge case, invalid move
        if (row < 0 or row > Board_Size - 1 or column < 0 or column > Board_Size - 1):
            return places   # return empty places

        # search all the possible directions . 8 directions

        # search in up down direction . If black is below it then search until there are all the blacks or we
        # reach the bottom
        i = row - 1
        if i >= 0 and self.board[i][column] == other:
            i = i - 1
            while i >= 0 and self.board[i][column] == other:
                i = i - 1
            if i >= 0 and self.board[i][column] == 0:
                places = places + [(i, column)]

        # check for bottom right diagonal
        i = row - 1
        j = column + 1
        if i >= 0 and j < Board_Size and self.board[i][j] == other:
            i = i - 1
            j = j + 1
            while i >= 0 and j < Board_Size and self.board[i][j] == other:
                i = i - 1
                j = j + 1
            if i >= 0 and j < Board_Size and self.board[i][j] == 0:
                places = places + [(i, j)]

        #  check for the right direction
        j = column + 1
        if j < Board_Size and self.board[row][j] == other:
            j = j + 1
            while j < Board_Size and self.board[row][j] == other:
                j = j + 1
            if j < Board_Size and self.board[row][j] == 0:
                places = places + [(row, j)]

        # check for the upper right diagonals for all the possible moves .
        i = row + 1
        j = column + 1
        if i < 8 and j < Board_Size and self.board[i][j] == other:
            i = i + 1
            j = j + 1
            while i < 8 and j < Board_Size and self.board[i][j] == other:
                i = i + 1
                j = j + 1
            if i < 8 and j < Board_Size and self.board[i][j] == 0:
                places = places + [(i, j)]

        # go straight up to the heavens
        i = row + 1
        if i < Board_Size and self.board[i][column] == other:
            i = i + 1
            while i < Board_Size and self.board[i][column] == other:
                i = i + 1
            if i < Board_Size and self.board[i][column] == 0:
                places = places + [(i, column)]

        # go up and left diagonal
        i = row + 1
        j = column - 1
        if i < Board_Size and j >= 0 and self.board[i][j] == other:
            i = i + 1
            j = j - 1
            while i < Board_Size and j >= 0 and self.board[i][j] == other:
                i = i + 1
                j = j - 1
            if i < Board_Size and j >= 0 and self.board[i][j] == 0:
                places = places + [(i, j)]

        # go left all the way
        j = column - 1
        if j >= 0 and self.board[row][j] == other:
            j = j - 1
            while j >= 0 and self.board[row][j] == other:
                j = j - 1
            if j >= 0 and self.board[row][j] == 0:
                places = places + [(row, j)]

        # go to bottom left diagonal .
        i = row - 1
        j = column - 1
        if i >= 0 and j >= 0 and self.board[i][j] == other:
            i = i - 1
            j = j - 1
            while i >= 0 and j >= 0 and self.board[i][j] == other:
                i = i - 1
                j = j - 1
            if i >= 0 and j >= 0 and self.board[i][j] == 0:
                places = places + [(i, j)]

        return places

    def get_valid_moves(self, color):
        """Get the avaiable positions to put a piece of the given color. For
        each piece of the given color we search its neighbours,
        searching for pieces of the other color to determine if is
        possible to make a move. This method must be called before
        apply_move.

        """

        if color == BLACK:
            other = WHITE
        else:
            other = BLACK

        places = []

        # for all the disc of that player and find the possible valid moves for that disc, Append them all and return
        # as final result.
        for i in range(Board_Size):
            for j in range(Board_Size):
                if self.board[i][j] == color:
                    places = places + self.lookup(i, j, color)

        places = list(set(places))  # removing doubles
        self.valid_moves = places
        return places

    def apply_move(self, move, color):
        """ Determine if the move is correct and apply the changes in the game.
        """
        if move in self.valid_moves:
            self.board[move[0]][move[1]] = color
            for i in range(1, 9):
                self.flip(i, move, color)

    def flip(self, direction, position, color):
        """ invert the discs for the given direction  """

        if direction == 1:
            # going down
            row_inc = -1
            col_inc = 0
        elif direction == 2:
            # going right down
            row_inc = -1
            col_inc = 1
        elif direction == 3:
            # going right
            row_inc = 0
            col_inc = 1
        elif direction == 4:
            # going up right
            row_inc = 1
            col_inc = 1
        elif direction == 5:
            # going up and up
            row_inc = 1
            col_inc = 0
        elif direction == 6:
            # going up left
            row_inc = 1
            col_inc = -1
        elif direction == 7:
            # going left
            row_inc = 0
            col_inc = -1
        elif direction == 8:
            # going left nichy
            row_inc = -1
            col_inc = -1

        places = []  # pieces to flip
        i = position[0] + row_inc
        j = position[1] + col_inc

        if color == WHITE:
            other = BLACK
        else:
            other = WHITE

        if i in range(Board_Size) and j in range(Board_Size) and self.board[i][j] == other:
            # assures there is at least one piece to flip
            places = places + [(i, j)]
            i = i + row_inc
            j = j + col_inc
            while i in range(Board_Size) and j in range(Board_Size) and self.board[i][j] == other:
                # search for more pieces to flip
                places = places + [(i, j)]
                i = i + row_inc
                j = j + col_inc
            if i in range(Board_Size) and j in range(Board_Size) and self.board[i][j] == color:
                # found a piece of the right color to flip the pieces between
                for pos in places:
                    self.board[pos[0]][pos[1]] = color  # the flip happens here



    def game_ended(self):
        """ Is the game ended? """
        # board full or wipeout
        whites, blacks, empty = self.count_stones()
        if whites == 0 or blacks == 0 or empty == 0:
            return True

        # no valid moves for both players
        if self.get_valid_moves(BLACK) == [] and self.get_valid_moves(WHITE) == []:
            return True

        return False

    def count_stones(self):
        """ Returns the number of white pieces, black pieces and empty squares, in
        this order.
        """
        whites = 0
        blacks = 0
        empty = 0
        for i in range(Board_Size):
            for j in range(Board_Size):
                if self.board[i][j] == WHITE:
                    whites += 1
                elif self.board[i][j] == BLACK:
                    blacks += 1
                else:
                    empty += 1
        return whites, blacks, empty

    def next_states(self, color):
        """
        get current player and generate all possible boards with the moves that the current player can take .


        """
        valid_moves = self.get_valid_moves(color)
        for move in valid_moves:
            newBoard = deepcopy(self)
            newBoard.apply_move(move, color)
            yield newBoard


def get_options(gui, board):
    # set up players
    player1, player2, level = gui.show_options()
    if player1 == "human":
        now_playing = Human(gui, WHITE)
    else:
        now_playing = Computer(BLACK, level*2 )
    if player2 == "human":
        other_player = Human(gui, WHITE)
    else:
        other_player = Computer(BLACK, level*2 )

    gui.show_game()
    gui.update(board.board, board.get_valid_moves(now_playing.color),2, 2, now_playing.color)
    return now_playing, other_player


def run(gui, board, now_playing, other_player):
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        if board.game_ended():
            whites, blacks, empty = board.count_stones()
            if whites > blacks:
                winner = WHITE
            elif blacks > whites:
                winner = BLACK
            else:
                winner = None
            break
        now_playing.get_current_board(board)
        if board.get_valid_moves(now_playing.color):
            score, board = now_playing.get_move()
            whites, blacks, empty = board.count_stones()
            gui.update(board.board,board.get_valid_moves(now_playing.color), blacks, whites,
                       now_playing.color)
        now_playing, other_player = other_player, now_playing
    gui.show_winner(winner)
    pygame.time.wait(1000)
    restart(gui,  now_playing, other_player)


def restart(gui, now_playing, other_player):
    board = Board()
    get_options(gui, board)
    run(gui, board, now_playing, other_player)


# define a main function
def main():
    # initialize the pygame module
    gui = ui.Gui()
    board = Board()
    n_p, o_p = get_options(gui, board)
    run(gui, board, n_p, o_p)


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
