import random
from time import sleep
from pdb import set_trace as tr


class AI():
    def __init__(self, board, is_white):
        self.b = board
        self.is_white = is_white

    def make_move(self):
        # Make the best move!!
        (best_move, best_points) = self.find_best_move(self.b, 1, self.is_white)
        self.b.move_by_coords(best_move)

    def find_best_move(self, b, depth=1, for_white=False):
        # Find which possible move is the best by looking at where future moves will lead you
        # This is our recursive method. It will call itself, alternately pretending to play as
        # black or white pieces, until a certain depth is reached. This way, it'll predict how
        # the game will go if a certain move is made

        # Depth check. Make sure recursion
        if depth >= 4:
            return ((0, 0, 0, 0), self.value_board(b, for_white))

        # Initialize best_move
        legal_moves = b.legal_moves
        best_move = legal_moves[random.randrange(len(legal_moves))]
        best_points = self.value_board(
            b.clone().move_by_coords(best_move), for_white)

        # Iterate through all the possible moves...
        for move in legal_moves:
            moved_b = b.clone().move_by_coords(move)
            # and recursion! Spawn a new 'bot' to predict what opponent will play.
            (opp_move, points) = self.find_best_move(
                moved_b, depth+1, not for_white)
            points *= -1

            if points > best_points:
                best_points = points
                best_move = move
        return (best_move, best_points)

    def value_board(self, b, is_value_for_white=True):
        points = b.sum_points()
        if is_value_for_white:
            return points[0] - points[1]
        return points[1] - points[0]


# This line prevents the game from being played if we ever make more files that import
# and use AI.
# Notably, when you run a python file, a couple specific variables come pre-defined (without
# you ever having to declare them yourself). Among these is the string variable __name__. If
# the file it's in is the one you specifically ran, __name__ will contain '__main__'. If it's
# just being imported from another file, it will be something different
# Therefore, we can check to see if this is the 'central' file we want to run by checking if
# variable __name__ is '__main__' or not
if __name__ == '__main__':
    from index import Board
    b = Board()
    ai = AI(b, False)

    # Game loop
    while True:
        print(b)
        # The end paramater here prevents print function from adding a newline character. Whatever
        # we print afterwards is going to start printing exactly on the same line now
        print('Your move: ', end='')
        user_move = input()
        b.move(user_move)
        ai.make_move()
