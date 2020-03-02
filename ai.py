import random
from time import sleep
from pdb import set_trace as tr


class AI():
    def __init__(self, board, is_white):
        self.b = board
        self.is_white = is_white

    def make_move(self):
        (best_move, best_points) = self.find_best_move(self.b, 1, self.is_white)
        print('MAX POINTS:', best_points)
        self.b.move_by_coords(best_move)

    def find_best_move(self, b, depth=1, for_white=False):
        if depth >= 4:
            return ((0, 0, 0, 0), self.value_board(b, for_white))

        legal_moves = b.legal_moves
        # init best_move
        best_move = legal_moves[random.randrange(len(legal_moves))]
        best_points = self.value_board(
            b.clone().move_by_coords(best_move), for_white)

        for move in legal_moves:
            moved_b = b.clone().move_by_coords(move)
            (opp_move, points) = self.find_best_move(
                moved_b, depth+1, not for_white)
            points *= -1
            # print(moved_b)
            # print(points, best_points)
            # input()

            if points > best_points:
                best_points = points
                best_move = move
        # print('RETURNING:', best_points)
        return (best_move, best_points)

    def value_board(self, b, is_value_for_white=True):
        points = b.sum_points()
        if is_value_for_white:
            return points[0] - points[1]
        return points[1] - points[0]


if __name__ == '__main__':
    from index import Board
    b = Board()
    ai = AI(b, False)

    while True:
        print(b)
        print('Your move: ', end='')
        user_move = input()
        b.move(user_move)
        # print(b)
        ai.make_move()
