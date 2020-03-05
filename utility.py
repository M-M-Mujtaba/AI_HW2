
EMPTY = 0
BLACK = 1
WHITE = 2
INFINITY = 999999999
depth_input = 0

def get_eval( player,curr_board):
    """Return the piece differential score Given a board resultant of the
    difference between the initial board and the board after the
    move and a weight band returns the count of the pieces the
    player has gained minus the same count for the opponent.

    """

    whites, blacks, empty = curr_board.count_stones()
    if player == WHITE:
        myScore = whites
        yourScore = blacks
    else:
        myScore = blacks
        yourScore = whites
    return (myScore - yourScore)



def our_minimax( board, parentBoard, depth, player, opponent, isMax, alfa=-INFINITY, beta=INFINITY, ):
    bestChild = board
    if depth == 0:
        return (get_eval( player, board), board)
    if (isMax):
        score = -INFINITY
        for child in board.next_states(player):
            get_score, newChild = our_minimax(child, board, depth - 1,opponent, player,not (isMax),alfa, beta)
            if get_score > score:
                score = get_score
                bestChild = child
            alfa = max(alfa, get_score)
            if alfa >= beta:
                break
    else: # min level
        score = INFINITY
        for child in board.next_states(player):
            get_score, newChild = our_minimax(child, board, depth - 1, opponent, player,not (isMax),alfa, beta)
            if get_score < score:
                score = get_score
                bestChild = child
            beta = min(beta, get_score)
            if alfa >= beta:
                break
    return ((get_eval( player, bestChild), bestChild))