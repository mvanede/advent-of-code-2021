from utils import Parser
from math import floor
import itertools
from utils.lib import get_timer, panswer, pruntime, int_to_bits
_ST = get_timer()

f = open("ass_day_24_input.txt", "r")
commands = Parser.split_by(f.read(), "\n", " ", conv_func=lambda x: int(x) if x not in ['inp', 'add', 'mul', 'div', 'mod', 'eql', 'w', 'x', 'y', 'z' ] else x)  # lambda x:int(x)


"""
Straightforward implementation of validation program
"""
def validate_nomad(INPUT, program):
    state = {
        'w': 0,
        'x': 0,
        'y': 0,
        'z': 0,
    }

    for command, variable, *value in program:
        if value:
            value = value[0] if isinstance(value[0], int) else state[value[0]]

        if command == 'inp':
            state[variable] = INPUT.pop(0)
        elif command == 'add':
            state[variable] = state[variable] + value
        elif command == 'mul':
            state[variable] = state[variable]*value
        elif command == 'div':
            state[variable] = floor(state[variable]/value)
        elif command == 'mod':
            state[variable] = floor(state[variable]%value)
        elif command == 'eql':
            state[variable] = 1 if state[variable] == value else 0
        else:
            print("Unknown command: " + command)
    return state


def is_valid(input):
    output = validate_nomad([int(x) for x in input], commands)
    return not output['z']


print(is_valid('98998519596997'))
pruntime(_ST)



