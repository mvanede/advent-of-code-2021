from utils import Parser
from utils.lib import get_timer, panswer, pruntime
from ass_day_18 import to_tree
import ast
import itertools

_ST = get_timer()



def main():
    f = open("ass_day_18_input.txt", "r")
    commands = Parser.split_by(f.read(), "\n", conv_func=None)  # lambda x:int(x)
    numbers = [ast.literal_eval(x) for x in commands]
    all_combinations = list(itertools.combinations(numbers, 2))

    magnitudes = []
    for combination in list(all_combinations):
        tree = to_tree(None, [combination[0], combination[1]])
        changed = True
        while changed:
            tree, changed = tree.reduce()
        magnitudes.append(tree.get_magnitude())

    panswer(max(magnitudes))


main()
pruntime(_ST)
# 4747