from colorama import Fore, Back, Style
# import chess
# board = chess.Board()


class Board(list):
    def __init__(self):
        self.b = [['.' for i in range(8)] for j in range(8)]
        self.legal_moves = []
        self.colnames = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        # setup = [
        #     ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
        #     ['P' for i in range(8)]
        # ]
        setup = [
            ['.' for i in range(8)],
            ['.', 'K', '.', '.', '.', '.', '.', '.']
        ]

        self.b[:2] = setup
        self.b[6:] = reversed([list(map(str.lower, row)) for row in setup])

    def form_legal_moves(self, is_white):
        b = self.b
        legal_moves = []
        direction = int(is_white) * 2 - 1

        def flatten_possibility_tree(possibility_tree):
            moves = []
            for tree in possibility_tree:
                for coord in tree:
                    if coord[0] < 0 or coord[1] < 0 or coord[0] > 7 or coord[1] > 7:
                        break
                    test_tile = b[coord[0]][coord[1]]
                    if self._is_piece(test_tile):
                        if not self._is_white(test_tile) == is_white:
                            moves.append(coord)
                        break
                    moves.append(coord)
            return moves

        def pawn_moves(row, col):
            pass

        def rook_moves(row, col):
            possibility_tree = []
            # add down, up, right, lett
            possibility_tree.append([
                (test_row, col) for test_row in range(row+1, 8)
            ])
            possibility_tree.append([
                (test_row, col) for test_row in range(row-1, -1, -1)
            ])
            possibility_tree.append([
                (row, test_col) for test_col in range(col+1, 8)
            ])
            possibility_tree.append([
                (row, test_col) for test_col in range(col-1, -1, -1)
            ])

            return flatten_possibility_tree(possibility_tree)

        def knight_moves(row, col):
            possibility_tree = [
                [(row + 2, col + 1)],
                [(row + 2, col - 1)],
                [(row - 2, col + 1)],
                [(row - 2, col - 1)],
                [(row + 1, col + 2)],
                [(row - 1, col + 2)],
                [(row + 1, col - 2)],
                [(row - 1, col - 2)]
            ]
            return flatten_possibility_tree(possibility_tree)

        def bishop_moves(row, col):
            possibility_tree = []
            # for i in range()
            pass

        def queen_moves(row, col):
            pass

        def king_moves(row, col):
            possibility_tree = []
            for d_row in range(-1, 2):
                for d_col in range(-1, 2):
                    possibility_tree.append([(row+d_row, col+d_col)])
            return flatten_possibility_tree(possibility_tree)

        moves_chooser = {
            'p': pawn_moves,
            'r': rook_moves,
            'n': knight_moves,
            'b': bishop_moves,
            'q': queen_moves,
            'k': king_moves
        }

        for row_index in range(8):
            for col_index in range(8):
                cur = b[row_index][col_index]
                if not self._is_piece(cur) or self._is_white(cur) != is_white:
                    continue
                moves = moves_chooser[cur.lower()](row_index, col_index)
                print(cur)
                print(moves)
                legal_moves += moves
        return legal_moves

    @staticmethod
    def _is_color(tile, is_white):
        return tile.islower() == is_white

    @staticmethod
    def _is_white(tile):
        return tile.islower()

    @staticmethod
    def _is_piece(tile):
        return tile is not None and tile != '.'

    def __getitem__(self, key):
        return self.b[key]

    def __setitem__(self, key, item):
        self.b[key] = item

    def __str__(self):
        ret = '     ' + ' '.join(self.colnames) + '\n'
        ret += '   __________________\n'
        for row_index, row in enumerate(self.b):
            ret += str(row_index) + '  |' + ''.join(
                [' ' + tile if (tile.isupper() or tile == '.')
                 else Fore.BLACK + Back.WHITE + ' ' + tile + Style.RESET_ALL
                 for tile in row]
            ) + '\n'
        return ret


if __name__ == '__main__':
    a = Board()
    print(a)
    a.form_legal_moves(False)
