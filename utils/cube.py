

class Cube:
    _cube = [[[]]]

    def __init__(self, cube: [[[]]]):
        self._cube = cube

    @property
    def grid(self):
        return self._grid

    @property
    def height(self):
        return len(self._grid)

    @property
    def width(self):
        return len(self._grid[0])