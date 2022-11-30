from utils.lib import get_timer, panswer, pruntime
_ST = get_timer()


def calculate_path(start, velocity, target_area):
    positions = []
    position = start

    positions.append(start.copy())

    while position[0] < target_area[1][0] and position[1] < target_area[1][1]:
        position[0] += velocity[0]
        position[1] -= velocity[1]

        if velocity[0] != 0:
            velocity[0] -= 1 if velocity[0] > 0 else -1

        velocity[1] -= 1

        positions.append(position.copy())
    return positions


def in_area(position, area):
    return area[0][0] <= position[0] <= area[1][0] and area[0][1] <= position[1] <= area[1][1]


def max_height(path):
    return max([h*-1 for w,h in path])


def main():
    #test_target_area: x=20..30, y=-10..-5
    target_area = ((79, 117),(137, 176))

    max_height_found = 0
    for col in range (0, target_area[1][0]):
        for row in range(0, 1000):
            p = calculate_path([0, 0], [col, row], target_area)
            if in_area(p[-1], target_area):
                mh = max_height(p)
                max_height_found = mh if mh > max_height_found else max_height_found
    panswer(max_height_found)


main()
pruntime(_ST)
#15400
