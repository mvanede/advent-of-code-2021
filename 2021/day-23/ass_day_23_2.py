from utils import Parser
import copy
from pprint import pprint
from utils.lib import get_timer, panswer, pruntime
from collections import defaultdict
_ST = get_timer()

f = open("ass_day_23_test_input.txt", "r")
inputlines = Parser.split_by(f.read(), "\n","", conv_func=None)  # lambda x:int(x)


burrow_to_solve = [
    '.', '.',
    [['B', True], ['D', True], ['D', True], ['A', True]],
    '.',
    [['C', True], ['B', True], ['C', True], ['D', True]],
    '.',
    [['D', True], ['A', True], ['B', True], ['A', True]],
    '.',
    [['C', True], ['C', True], ['A', True], ['B', True]],
    '.', '.']
# ROOMS = [2, 4, 6, 8]
# ROOM_SIZE = 4

# # Example
# burrow_to_solve = [
#     '.', '.',
#     [['A', True], ['D', True], ['D', True], ['B', True]],
#     '.',
#     [['D', True], ['B', True], ['C', True], ['C', True]],
#     '.',
#     [['C', True], ['A', True], ['B', True], ['B', True]],
#     '.',
#     [['A', True], ['C', True], ['A', True], ['D', True]],
#     '.', '.']
ROOMS = [2, 4, 6, 8]
ROOM_SIZE = 4

# burrow_to_solve = [
#     '.', '.',
#     [['A', True], ['A', True], ['A', True], ['B', True]],
#     '.',
#     [['B', True], ['B', True], ['B', False], ['A', True]],
#     '.',
#     [['C', True], ['C', True], ['C', True], ['C', False]],
#     '.',
#     [['D', True], ['D', True], ['D', True], ['D', False]],
#     '.', '.']
ROOMS = [2, 4, 6, 8]
ROOM_SIZE = 4

NOT_ROOMS = list(set(range(0, len(burrow_to_solve))) - set(ROOMS))
AMPHIPOD_DESTINATIONS = {
    'A': 2,
    'B': 4,
    'C': 6,
    'D': 8
}

def move_amphipod_to(_burrow, new_idx, old_idx):
    _copy = copy.deepcopy(_burrow)
    _copy[new_idx] = _copy[old_idx]
    _copy[old_idx] = '.'
    return _copy


def get_cost(amphipod):
    if amphipod[0] == 'A':
        return 1
    elif amphipod[0] == 'B':
        return 10
    elif amphipod[0] == 'C':
        return 100
    elif amphipod[0] == 'D':
        return 1000


def get_left_right(idx, _burrow):
    return [f for f in [idx-1, idx+1] if f > 0 and f < len(_burrow)]

def get_amphipods_in_hallway(_burrow):
    _amphipods = []
    for idx in NOT_ROOMS:
        if _burrow[idx] != '.':
            _amphipods.append(idx)
    return _amphipods


def next_moves(_burrow):
    possibilities = []

    # for all rooms, can we pop any to the hallway
    for idx in ROOMS:
        if not _burrow[idx]:
            continue

        # it can go to any empty place in the hall way left or any in the hallway right but only if it hasnt been out yet?
        for roomidx in get_left_right(idx, _burrow):
            if _burrow[roomidx] == '.':
                _copy = copy.deepcopy(_burrow)
                amphipod = _copy[idx].pop()

                # Todo: also don't move out of room in case you're already in the right place when everything below is also in the right place
                if amphipod[1]:
                    amphipod[1] = False
                    _copy[roomidx] = amphipod

                    # Moving out of room = 1 step + dooropening + (ROOMSIZE-current roomlength)
                    steps = 2 + ROOM_SIZE-len(_burrow[idx])
                    possibilities.append((_copy, steps * get_cost(amphipod)))

    # For any amphipod in the  hallway
    # If we can move into a room, do so. Otherwise move 1 or 2 left or right
    for idx in get_amphipods_in_hallway(_burrow):

        moved_into_room = False
        for roomidx in [z for z in get_left_right(idx, _burrow) if z in ROOMS] :

            # if the room is empty or only contains this type, we can enter this room if it's the suitable room for this type.
            if len(_burrow[roomidx]) < ROOM_SIZE:
                amphipod = _burrow[idx]
                types = [x[0] for x in _burrow[roomidx] if x[0] != amphipod[0]]

                if not types and AMPHIPOD_DESTINATIONS[amphipod[0]] == roomidx:
                    _copy = copy.deepcopy(_burrow)
                    _copy[roomidx].append(amphipod)
                    _copy[idx] = '.'

                    # Moving out of room = dooropening + (ROOMSIZE-current roomlength)
                    steps = 1 + (ROOM_SIZE - len(_burrow[roomidx]))
                    possibilities.append((_copy, steps * get_cost(amphipod)))
                    moved_into_room = True

        if not moved_into_room:
            if idx > 0 and _burrow[idx-1] == '.':
                _copy = move_amphipod_to(_burrow, new_idx=idx-1, old_idx=idx)
                possibilities.append((_copy, get_cost(_burrow[idx])))
            elif idx > 1 and (idx-1) in ROOMS and _burrow[idx-2] == '.':
                _copy = move_amphipod_to(_burrow, new_idx=idx - 2, old_idx=idx)
                possibilities.append((_copy, 2* get_cost(_burrow[idx])))

            if idx+1 < len(_burrow) and _burrow[idx+1] == '.':
                _copy = move_amphipod_to(_burrow, new_idx=idx + 1, old_idx=idx)
                possibilities.append((_copy, get_cost(_burrow[idx])))
            elif idx+1 < len(_burrow) and (idx+1) in ROOMS and _burrow[idx+2] == '.':
                _copy = move_amphipod_to(_burrow, new_idx=idx + 2, old_idx=idx)
                possibilities.append((_copy, 2*get_cost(_burrow[idx])))
    return possibilities


def is_solved(_burrow):
    for r in ROOMS:
        if len(_burrow[r]) != ROOM_SIZE:
            return False

        types = list(set([x[0] for x in _burrow[r]]))
        if len(types) > 1:
            return False

        if AMPHIPOD_DESTINATIONS[types[0]] != r:
            return False
    return True


# for the hallway, can we push any in a room?
CACHE2 = defaultdict(set)
CACHE2['solvecount'] = 0


def solve(_burrow, cost_up_until_here, history=[]):
    if str(_burrow) in CACHE2:
        # Return cheapest from cache
        _cached = list(CACHE2[str(_burrow)])
        _cached.sort(key=lambda y: (-y[1], y[0]))
        return _cached[0:1]

    if is_solved(_burrow):
        return [(0, True)]

    # Get all options
    moves = next_moves(_burrow)

    # If out of moves
    if not moves:
        return [(0, False)]

    possible_paths = []
    CACHE2['solvecount'] += 1
    for move, cost_of_move in moves:
        # prevent endless recursion, don't go where we've already been
        if str(move) in [x for x, y in history]:
            continue

        _history = copy.deepcopy(history)
        _history.append((str(move), cost_of_move))
        _paths = solve(move, cost_up_until_here + cost_of_move, _history)

        for _cost, _will_end in _paths:
            possible_paths.append((_cost + cost_of_move, _will_end))

    CACHE2[str(_burrow)].update(set(possible_paths))

    # Only give cheapest, as min of large list is very expensive
    possible_paths.sort(key=lambda y: (-y[1], y[0]))
    return possible_paths[0:1]



solve(burrow_to_solve, 0)

# print(SOLVED.keys())
_solution = list(CACHE2[str(burrow_to_solve)])
_solution.sort(key=lambda y: (-y[1], y[0]))
print(_solution)

# moves = next_moves(burrow_to_solve)
# for m in moves:
#     print(m)

# pprint(CACHE2['solvecount'])


panswer("answer")
pruntime(_ST)
