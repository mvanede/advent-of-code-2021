from utils import Parser, Grid, ExpandingGrid
from utils.lib import get_timer, panswer, pruntime
from math import inf
import heapdict
_ST = get_timer()


def dijkstra(_grid, src, dest):
    prev = {}
    path_costs = {src: 0}

    cell_list = heapdict.heapdict()
    for cell in _grid.cells:
        cell_list[cell] = inf

    cell_list[src] = 0
    while cell_list:
        u, c = cell_list.popitem()

        for v in _grid.get_adjacent(u[0], u[1], False):
            cost_of_path = path_costs[u] + _grid.get(u[0], u[1])

            if cost_of_path < path_costs.get(v, inf):
                path_costs[v] = cost_of_path
                cell_list[v] = cost_of_path
                prev[v] = u

    path = [dest]
    cur = dest

    while prev.get(cur, None):
        path.append(prev[cur])
        cur = prev[cur]

    return list(reversed(path))


def main():
    f = open("ass-day-15-input.txt", "r")
    commands = Parser.split_by(f.read(), "\n", "", conv_func=lambda x: int(x))
    grid = Grid(commands)

    # Multiply the grid x5
    new_grid = grid.get_copy()
    multigrid = ExpandingGrid(1, 1, None)
    new_grid = grid
    for row in range(0, 5):
        # Set first in row
        if row == 0:
            multigrid.set(0, 0, grid)
        else:
            new_grid = multigrid.get(0, row - 1).get_copy()
            new_grid.add_all(1, lambda x: 1 if x % 10 == 0 else x % 10)
            multigrid.set(0, row, new_grid)

        for col in range(1, 5):
            new_grid = multigrid.get(col - 1, row).get_copy()
            new_grid.add_all(1, lambda x: 1 if x % 10 == 0 else x % 10)
            multigrid.set(col, row, new_grid)

    # Smash it
    height = grid.height
    width = grid.width
    large_grid = ExpandingGrid(1, 1, None)
    for row_cnt, row in enumerate(multigrid.rows):
        for col_cnt, _grid in enumerate(row):
            for _col, _row in _grid.cells.keys():
                large_grid.set(_col + (col_cnt * width), _row + (row_cnt * height), _grid.get(_col, _row))

    # Start the engines
    _sum = 0
    path = dijkstra(large_grid, (0, 0), (large_grid.width-1, large_grid.height-1))
    for col, row in path[1:]:
        _sum += large_grid.get(col, row)

    panswer(_sum)


main()
pruntime(_ST)

# 2952
