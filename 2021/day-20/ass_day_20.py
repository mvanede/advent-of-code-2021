from utils import Parser, ExpandingGrid
from utils.lib import get_timer, panswer, pruntime
_ST = get_timer()

f = open("ass_day_20_input.txt", "r")
commands = Parser.split_by(f.read(), "\n\n", conv_func=None)  # lambda x:int(x)
enhancement_algorithm = commands[0]
input_image = ExpandingGrid(Parser.split_by(commands[1:], "\n", "")[0], '.')


def get_pixel_for(_col, _row, _image):
    x = ['0' if v == '.' else '1' for v in _image.get_adjacent(_col,_row, True, True).values()]
    idx = int(''.join(x), 2)
    return enhancement_algorithm[idx]


for i in range (0, 2):
    # Extend the image on all sides with 2 (enough, since we use a window of 3x3
    input_image.set(-2, -2, input_image.default_value)
    input_image.set(input_image.width+1, input_image.height+1, input_image.default_value)

    new_image = input_image.get_copy()
    for col in range(1, input_image.width-1):
        for row in range (1, input_image.height-1):
            new_image.set(col, row, get_pixel_for(col, row, input_image))
    input_image = new_image.get_copy()

    # Set the surroundings
    idx = int(('0' if input_image.default_value=='.' else '1')*9, 2)
    surroundings_value = enhancement_algorithm[idx]

    input_image.set_in_row(0, surroundings_value)
    input_image.set_in_row(input_image.height-1, surroundings_value)
    input_image.set_in_col(0, surroundings_value)
    input_image.set_in_col(input_image.width - 1, surroundings_value)

    input_image.set_default_value(surroundings_value)


# input_image.pprint()
panswer(input_image.count_if(lambda x: x == '#'))
pruntime(_ST)

# 5301
# 19492