import random


class AI():
    def __init__(self, board, is_white):
        self.b = board
        self.is_white = is_white

    def make_move(self):
        legal_moves = self.b.legal_moves
        best_move = legal_moves[random.randrange(len(legal_moves))]
        best_points = 0
        # find move that maximizes points
        for move in legal_moves:
            moved_b = self.b.clone()
            moved_b.move_by_coords(move)

            points = moved_b.sum_points()
            self_points = points[0]
            if not self.is_white:
                self_points = points[1]

            if self_points > best_points:
                best_points = self_points
                best_move = move

        self.b.move_by_coords(best_move)


if __name__ == '__main__':
    from index import Board
    b = Board()
    ai = AI(b, False)

    while True:
        print(b)
        print('Your move: ', end='')
        user_move = input()
        b.move(user_move)
        print(b)
        ai.make_move()
