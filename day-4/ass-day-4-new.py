from utils.grid import Grid
from typing import List

f = open("ass-day-4-input.txt", "r")
lines = f.read().split("\n\n")
numbers = lines[0].split(',')

boards = []
for l in lines[1:]:
    b = [sl.split() for sl in l.split("\n") ]
    boards.append(Grid(b))


def has_bingo(board):
    for row in board.rows + board.cols:
        uniq = list(set(row))
        if uniq[0] == '-' and len(uniq) == 1:
            return True


def play(_numbers, _boards:List[Grid]):
    for n in _numbers:
        for _board in _boards:
            _board.replace_all(n, '-')

            if has_bingo(_board):
                _board.replace_all('-', 0)
                return _board.get_sum() * int(n)


print (play(numbers, boards))