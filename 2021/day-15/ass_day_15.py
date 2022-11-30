from utils import Parser, Grid
from utils.lib import get_timer, panswer, pruntime
_ST = get_timer()
import heapdict
from math import inf


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

    _sum = 0
    path = dijkstra(grid, (0,0), (grid.width-1, grid.height-1))
    for col, row in path[1:]:
        _sum += grid.get(col, row)

    panswer(_sum)

main()
pruntime(_ST)
# 696