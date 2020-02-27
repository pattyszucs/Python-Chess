from colorama import Fore, Back, Style
# import chess
# board = chess.Board()


class Board(list):
    def __init__(self):
        self.b = [['.' for i in range(8)] for j in range(8)]
        self.legal_moves = []
        self.colnames = 'abcdefgh'
        self.is_white_turn = True

        setup = [
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
            ['P' for i in range(8)]
        ]
        self.b[:2] = setup
        self.b[6:] = reversed([list(map(str.lower, row)) for row in setup])
        self.legal_moves = self.form_legal_moves()

        # self.b = [
        #     ['.', '.', '.', '.', '.', '.', '.', '.'],
        #     ['.', '.', '.', '.', '.', '.', '.', '.'],
        #     ['.', '.', 'P', '.', '.', '.', '.', '.'],
        #     ['.', '.', '.', '.', '.', '.', '.', '.'],
        #     ['.', '.', '.', '.', '.', '.', '.', '.'],
        #     ['.', '.', '.', '.', '.', '.', '.', '.'],
        #     ['.', '.', '.', '.', '.', '.', '.', '.'],
        #     ['.', '.', '.', '.', '.', '.', '.', '.']
        # ]

    def form_legal_moves(self):
        is_white = self.is_white_turn
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
            moves = []
            try:
                forward = b[row-direction][col]
                if not self._is_piece(forward):
                    moves.append((row-direction, col))
                    if ((row == 1 and not is_white) or (row == 6 and is_white)) and not self._is_piece(b[row-(direction*2)][col]):
                        moves.append((row-(direction*2), col))
            except:
                pass

            left_attack = b[row-direction][col-1]
            if self._is_piece(left_attack) and self._is_white(left_attack) != is_white:
                moves.append((row-direction, col-1))
            try:
                right_attack = b[row-direction][col+1]
                if self._is_piece(right_attack) and self._is_white(right_attack) != is_white:
                    moves.append((row-direction, col+1))
            except:
                pass

            # clear out-of-bounds
            moves = [move for move in moves if (
                move[0] > 0 and move[0] <= 7 and move[1] > 0 and move[1] <= 7)]

            return moves

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
            possibility_tree.append([
                (row+dif, col+dif) for dif in range(1, 8-row)
            ])
            possibility_tree.append([
                (row+dif, col-dif) for dif in range(1, 8-row)
            ])
            possibility_tree.append([
                (row-dif, col+dif) for dif in range(1, row)
            ])
            possibility_tree.append([
                (row-dif, col-dif) for dif in range(1, row)
            ])
            return flatten_possibility_tree(possibility_tree)

        def queen_moves(row, col):
            return rook_moves(row, col) + bishop_moves(row, col)

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
                # print(cur)
                # print(moves)
                legal_moves += [(row_index, col_index, move[0], move[1])
                                for move in moves]
        return legal_moves

    @staticmethod
    def _is_white(tile):
        return tile.islower()

    @staticmethod
    def _is_piece(tile):
        return tile is not None and tile != '.'

    def move(self, move):
        # move should be formatted as 'a2a4'
        from_coord = (int(move[1]), self.colnames.index(move[0].lower()))
        to_coord = (int(move[3]), self.colnames.index(move[2].lower()))
        return self.move_by_coords((from_coord[0], from_coord[1], to_coord[0], to_coord[1]))

    def move_by_coords(self, coord):
        self.b[coord[2]][coord[3]] = self.b[coord[0]][coord[1]]
        self.b[coord[0]][coord[1]] = '.'
        self.is_white_turn = not self.is_white_turn
        self.legal_moves = self.form_legal_moves()
        points = self.sum_points()
        if points[0] >= 100:
            print('WHITE HAS WON THE GAME!')
        if points[1] >= 100:
            print('BLACK HAS WON THE GAME!')

    def sum_points(self):
        point_chooser = {
            'p': 1,
            'r': 5,
            'n': 3,
            'b': 3,
            'q': 9,
            'k': 100
        }
        points = [139, 139]  # total points available

        b = self.b
        for row in b:
            for tile in row:
                if not self._is_piece(tile):
                    continue
                value = point_chooser[tile.lower()]
                if self._is_white(tile):
                    points[1] -= value
                else:
                    points[0] -= value
        return points

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
    print(a.move('e6e0'))
    print(a.move('e1e3'))
    print(a.legal_moves)
    print(a.sum_points())
    print(a)
