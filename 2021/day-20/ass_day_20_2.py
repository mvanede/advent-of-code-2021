from utils import Parser
from utils.lib import get_timer, panswer, pruntime
_ST = get_timer()

f = open("ass_day_20_test_input.txt", "r")
commands = Parser.split_by(f.read(), "\n", conv_func=None)  # lambda x:int(x)

# CODE HERE


panswer("answer")
pruntime(_ST)


