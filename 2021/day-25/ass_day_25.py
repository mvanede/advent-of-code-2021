from utils import Parser, Grid
from utils.lib import get_timer, panswer, pruntime
_ST = get_timer()

f = open("ass_day_25_input.txt", "r")
commands = Parser.split_by(f.read(), "\n","", conv_func=None)  # lambda x:int(x)
seafloor = Grid(commands)

# CODE HERE
settled = False
counter = 0
while not settled:
    og = seafloor.get_copy()
    next_seafloor = seafloor.get_copy()
    herd1 = seafloor.cells_where(lambda x: x == '>')
    for col1, row1 in herd1.keys():
        rcol = (col1+1) % seafloor.width
        if seafloor.get(rcol, row1) == '.':
            next_seafloor.set(rcol, row1, '>')
            next_seafloor.set(col1, row1, '.')

    herd2 = seafloor.cells_where(lambda x: x == 'v')
    seafloor = next_seafloor.get_copy()
    for col2, row2 in herd2.keys():
        brow = (row2+1) % seafloor.height
        if seafloor.get(col2, brow) == '.':
            next_seafloor.set(col2, brow, 'v')
            next_seafloor.set(col2, row2, '.')

    seafloor = next_seafloor.get_copy()
    counter += 1
    settled = str(og) == str(seafloor)

panswer(counter)
pruntime(_ST)


