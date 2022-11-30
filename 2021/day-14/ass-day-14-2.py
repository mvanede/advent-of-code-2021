from utils import Parser
from utils.lib import get_timer, panswer, pruntime
from collections import defaultdict
_ST = get_timer()

f = open("ass-day-14-input.txt", "r")
commands = Parser.split_by(f.read(), "\n\n", conv_func=None)  # lambda x:int(x)
template = commands[0]

# PARSE RULES INTO DICT
rules = Parser.split_by(commands[1], "\n", " -> ")
ruleset = {}
for r in rules:
    ruleset[r[0]] = r[1]


# to split string in sets of two characters
def to_charsets(_string):
    _sets = defaultdict(int)
    for i in range(0, len(_string) - 1):
        _sets[_string[i:i+2]] += 1
    return _sets


# Allright, let's start
def main():
    charsets = to_charsets(template)
    for i in range(0, 40):
        _new_charsets = defaultdict(int)

        for charset, cnt1 in charsets.items():
            if charset in ruleset:
                new_string = charset[0] + ruleset[charset] + charset[1:]
                # Split new string into sets of 2, and add to new charsets times the original set occures
                for x, cnt2 in to_charsets(new_string).items():
                    _new_charsets[x] += cnt1 * cnt2
        charsets = _new_charsets

    # Count characters
    character_count = defaultdict(int)
    for s, cnt in charsets.items():
        character_count[s[0]] += cnt
    character_count[template[-1]] += 1

    panswer(max(character_count.values()) - min(character_count.values()))


main()
pruntime(_ST)
