from utils import Parser
from utils.lib import get_timer, panswer, pruntime, flatten_nested_lists
_ST = get_timer()

"""
Proces inputfile
"""
f = open("ass_day_22_test_input.txt", "r")
commands = Parser.split_by(f.read(), "\n"," ", conv_func=None)  # lambda x:int(x)

instructions = []
for c in commands:
    on_off = c[0]
    coords = c[1].split(",")
    _ = []
    for coord in coords:
        axis, vals = coord.split("=")
        start, end = vals.split("..")
        _.append((int(start), int(end)))
    instructions.append((on_off, _))

"""
Proces instruction
"""
width = height = depth = 100
cube = [[['off'] * (width + 1) for i in range(height + 1)] for d in range(depth +1)]
x_offset = int(width/2)
y_offset = int(height/2)
z_offset = int(depth/2)

for i in instructions:
    state = i[0]
    _x = i[1][0]
    _y = i[1][1]
    _z = i[1][2]

    if (_x[0]+x_offset < 0 or _x[1]+x_offset > 99) and (_y[0]+y_offset < 0 or _y[1]+y_offset > 99) and (_z[0]+z_offset < 0 or _z[1]+z_offset > 99):
        continue

    for x in range(_x[0], _x[1]+1):
        for y in range(_y[0], _y[1] + 1):
            for z in range(_z[0], _z[1] + 1):
                    cube[ x + x_offset][ y + y_offset][z + z_offset] = state


flatten = flatten_nested_lists(cube)
panswer(len([x for x in flatten if x == 'on']))
pruntime(_ST)

# 553201
