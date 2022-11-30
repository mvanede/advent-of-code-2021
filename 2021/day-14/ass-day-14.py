from utils import Parser
import datetime
from utils.lib import get_timer, panswer, pruntime, most_common, least_common
import re
_ST = get_timer()

f = open("ass-day-14-input.txt", "r")
commands = Parser.split_by(f.read(), "\n\n", conv_func=None)  # lambda x:int(x)
template = commands[0]
rules = Parser.split_by(commands[1], "\n", " -> ")

for i in range(0, 10):
    print('STARTING ITERATION {} @ {}'.format(str(i), datetime.datetime.now().time()))
    replacements = {}
    for r in rules:
        for m in re.finditer('(?=('+r[0]+'))', template):
            replacements[m.start()] = r[1]

    cntr = 0
    for start, char in sorted(replacements.items()):
        idx = (start + 1) + cntr
        template = template[:idx] + char + template[idx:]
        cntr += 1


x = template.count(most_common(template)) - template.count(least_common(template))
panswer(x)
pruntime(_ST)


