import random


class AI():
    def __init__(self, board, is_white):
        self.b = board
        self.is_white = is_white

    def make_move(self):
        legal_moves = self.b.legal_moves
        move = legal_moves[random.randrange(len(legal_moves))]
        self.b.move_by_coords(move)


if __name__ == '__main__':
    from index import Board
    b = Board()
    ai = AI(b, False)

    print(b)

    b.move('e6e4')
    print(b)
    ai.make_move()
    print(b)
