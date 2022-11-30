from utils import Parser
from collections import defaultdict
import itertools as it
from utils.lib import get_timer, panswer, pruntime
_ST = get_timer()

"""
The codeblock of 18 lines (where w is the input digit), can be 
simplified to this. div_z, add_x and add_y are the three variables
that can differ per block and appear in that order in the code
"""
def codeblock (w, prev_z, block_args):
    div_z, add_x, add_y = block_args
    z = prev_z // div_z
    if (prev_z % 26) + add_x == w:
        return z
    else:
        return (z*26) + w + add_y


# Can we reverse this?
def reverse_codeblock (w, next_z, block_args):
    div_z, add_x, add_y = block_args
    x = next_z - w - add_y

    if 0 <= w - add_x < 26:
       return w - add_x + (next_z * div_z)
    elif x % 26 == 0:
        return x // 26 * div_z

    return None


def solve(commands):
    # Start at the back, where z=0. Reverse the inputs
    div_zs = [x[2] for x in commands[4::18]]
    add_xs = [x[2] for x in commands[5::18]]
    add_ys = [x[2] for x in commands[15::18]]
    codeblock_arguments = list(zip(div_zs, add_xs, add_ys))

    last_zs = [0]
    result = defaultdict(list)
    digits = list(range(1, 10))[::-1]

    while codeblock_arguments:
        args = codeblock_arguments.pop()
        prevz_list = []

        for w, z in it.product(digits, last_zs):
            prev_z = reverse_codeblock(w, z, args)
            if prev_z is None:
                continue

            # Todo: could also use a set
            if not prev_z in prevz_list:
                prevz_list.append(prev_z)

            if z in result:
                for tail in result.get(z, []):
                    result[prev_z].append([w] + tail)
            else:
                result[prev_z] = [[w]]

        last_zs = prevz_list
    return result


def main():
    f = open("ass_day_24_input.txt", "r")
    commands = Parser.split_by(f.read(), "\n", " ",
                               conv_func=lambda x: int(x) if x not in ['inp', 'add', 'mul', 'div', 'mod', 'eql', 'w',
                                                                       'x', 'y', 'z'] else x)  # lambda x:int(x)

    result = solve(commands)
    valid_results = [int(''.join(map(str, x))) for x in result[0] if len(x) == 14]
    panswer(max(valid_results))
    panswer(min(valid_results))


main()
pruntime(_ST)
# Part1: 98998519596997
# Part2: 31521119151421
