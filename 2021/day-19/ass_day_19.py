from utils import Parser
from enum import Enum, unique
from utils.lib import get_timer, panswer, pruntime
_ST = get_timer()


"""
READ INPUT
"""


def read_input(filename):
    f = open(filename, "r")
    lines = Parser.split_by(f.read(), "\n\n", "\n", conv_func=None)  # lambda x:int(x)

    unplaced_scanners = []
    for line in lines:
        scanner = []
        for coord in line[1:]:
            scanner.append([int(x) for x in coord.split(",")])
        unplaced_scanners.append(scanner)
    return unplaced_scanners


@unique
class Facing(Enum):
    FRONT = 1
    BACK = 2
    LEFT = 3
    RIGHT = 4
    UP = 5
    DOWN = 6

@unique
class Rotation(Enum):
    NONE  = 1
    QRTCW = 2
    QRTCCW = 3
    HALF = 4


def apply_facing(position, facing):
    x = position[0]
    y = position[1]
    z = position[2]
    if facing == Facing.FRONT:
        return position
    elif facing == Facing.BACK:
        return [-x, y, -z]
    elif facing == Facing.LEFT:
        return [-z, y, x]
    elif facing == Facing.RIGHT:
        return [z, y, -x]
    elif facing == Facing.UP:
        return [x, z, -y]
    elif facing == Facing.DOWN:
        return [x, -z, y]


def apply_rotation(position, rotation):
    x = position[0]
    y = position[1]
    z = position[2]

    if rotation == Rotation.NONE:
        return position
    elif rotation == Rotation.QRTCW:
        return [y, -x, z]
    elif rotation == Rotation.QRTCCW:
        return [-y, x, z]
    elif rotation == Rotation.HALF:
        return [-x, -y, z]


def get_orientation(_position, f , r):
    return apply_rotation(apply_facing(_position.copy(), f), r)


def calc_offset(_b1, _b2):
    return [_b1[0]-_b2[0], _b1[1]-_b2[1], _b1[2]-_b2[2]]


def add_offset(position, offset):
    return [position[0]+offset[0], position[1]+offset[1], position[2]+offset[2]]


def get_matches(base_scanner, scanner2, f, r, offset):
    matches = []
    for idx, beacon2 in enumerate(scanner2):
        transformed_beacon = add_offset(get_orientation(beacon2, f, r), offset)
        if transformed_beacon in base_scanner:
            matches.append((transformed_beacon, beacon2))

        # If we're not gonna make 12 anymore, let's go home
        if len(matches) + (len(scanner2)-idx) < 12:
            return []
        # if we already made it to 12, also go home
        elif len(matches) == 12:
            return matches

    return matches



been_there = []
def should_place_next_scanner(_main_scanner, _unplaced_scanner):
    # For all orientations
    for beacon1 in _unplaced_scanner:
        # Loop over all beacons in placed scanner,
        for beacon2 in _main_scanner:
            for f in Facing:
                for r in Rotation:
                    # How much would match if beacon1==beacon2, given this facing+rotation?
                    beacon_1u = get_orientation(beacon1, f, r)
                    offset = calc_offset(beacon2, beacon_1u)

                    matches = get_matches(_main_scanner, _unplaced_scanner, f, r, offset)
                    if len(matches) >= 12:
                        return matches, f, r, offset
    return None, None, None, None


def main():
    unplaced_scanners = read_input("ass_day_19_input.txt")
    main_scanner = unplaced_scanners.pop(0)

    order = [[-397,770,-682], [-563,-459,-728], [-7,43,-97], [-585,-677,-842], [548,-495,250], [-359,585,-724], [-655,538,409], [-621,648,-820], [549,651,656], [-725,571,493], [487,589,-526], [398,-470,-523], [-831,499,-428], [-496,-614,723], [489,854,-602], [582,-598,-217], [484,-744,850], [-353,-781,-678], [634,726,880], [-552,649,769], [576,-382,-424], [-650,-668,475], [516,646,373], [601,-381,-817], [-917,452,-578], [506,-840,-500], [409,349,-680]]
    sorted_unplaced = []
    for o in order:
        for u in unplaced_scanners:
            if u[0] == o:
                sorted_unplaced.append(u)
    unplaced_scanners = sorted_unplaced

    while unplaced_scanners:
        print("STILL {} unplaced".format(str(len(unplaced_scanners))))
        unplaced_scanner = unplaced_scanners.pop(0)
        matches, f, r, offset = should_place_next_scanner(main_scanner, unplaced_scanner)
        if matches:
            print("PLACE SCANNER: " + str(unplaced_scanner[0]))

            # Add them to the main scanner
            for beacon1 in unplaced_scanner:
                relative_beacon1 = add_offset(get_orientation(beacon1, f, r), offset)
                main_scanner.append(relative_beacon1)

            # Horrible, but quick for now:  make the mainscanner contain only unique values
            main_scanner = [list(y) for y in set(tuple(x) for x in main_scanner)]
        else:
            print("PUT BACK: " + str(unplaced_scanner[0]))
            unplaced_scanners.append(unplaced_scanner)

    main_scanner = list(set(tuple(x) for x in main_scanner))
    panswer(len(main_scanner))


main()
pruntime(_ST)
# 362