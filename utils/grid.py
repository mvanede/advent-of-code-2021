from collections import Counter
import math
import copy


class NoMostCommonException(Exception):
    pass


class NoLeastCommonException(Exception):
    pass


class Grid:
    _grid = [[]]

    def __init__(self, *args, **kwargs):
        if isinstance(args[0], list):
            self._grid = copy.deepcopy(args[0])
        elif isinstance(args[0], int) and isinstance(args[1], int):
            self._default_value = kwargs['default_value'] if 'default_value' in kwargs else 0
            super().__init__([([self._default_value] * args[0]) for i in range(args[1])])

    @classmethod
    def init_with(cls, width, height, default_value=None):
        return cls([[default_value] * width for i in range(height)])

    @property
    def grid(self):
        return self._grid

    @property
    def height(self):
        return len(self._grid)

    @property
    def width(self):
        return len(self._grid[0])

    @property
    def rows(self):
        return self._grid

    @property
    def cols(self):
        return [list(col) for col in (list(zip(*self._grid)))]

    @property
    def cells(self):
        retval = {}
        for row_idx in range(0, self.height):
            for col_idx in range(0, self.width):
                retval[(col_idx, row_idx)] = self.get(col_idx, row_idx)
        return retval

    def cells_where(self, where_func):
        retval = {}
        for row_idx in range(0, self.height):
            for col_idx in range(0, self.width):
                if where_func(self.get(col_idx, row_idx)):
                    retval[(col_idx, row_idx)] = self.get(col_idx, row_idx)
        return retval

    """
    GET methods
    """

    def get(self, col_idx: int, row_idx: int):
        return self._grid[row_idx][col_idx]

    def get_row(self, row_idx: int):
        return self._grid[row_idx]

    def get_rows(self, start_idx: int, end_idx: int):
        return self._grid[start_idx:end_idx]

    def get_col(self, col_idx: int):
        return [row[col_idx] for row in self._grid]

    def get_cols(self, start_idx: int, end_idx: int):
        return [row[start_idx:end_idx] for row in self._grid]

    def get_copy(self):
        return Grid(copy.deepcopy(self._grid))

    """
    MOST AND LEAST COMMON methods
    """

    def get_most_common_in_row(self, row_idx: int):
        data = Counter(self._grid[row_idx]).most_common(2)
        if data[0][1] == data[1][1]:
            raise NoMostCommonException
        return data[0]

    def get_least_common_in_row(self, row_idx: int):
        data = Counter(self._grid[row_idx]).most_common()
        data.reverse()

        if data[0][1] == data[1][1]:
            raise NoLeastCommonException
        return data[0]

    def get_most_common_in_col(self, col_idx: int):
        data = Counter(self.get_col(col_idx)).most_common(2)
        if data[0][1] == data[1][1]:
            raise NoMostCommonException
        return data[0]

    def get_least_common_in_col(self, col_idx: int):
        data = Counter(self.get_col(col_idx)).most_common()
        data.reverse()

        if data[0][1] == data[1][1]:
            raise NoLeastCommonException
        return data[0]

    def get_most_common(self):
        data = Counter(self.flatten()).most_common(2)
        if data[0][1] == data[1][1]:
            raise NoMostCommonException
        return data[0]

    def get_least_common(self):
        data = Counter(self.flatten()).most_common()
        data.reverse()

        if data[0][1] == data[1][1]:
            raise NoLeastCommonException
        return data[0]

    def rotate_cw(self):
        self._grid = [list(row) for row in zip(*reversed(self._grid))]
        return self

    def rotate_ccw(self):
        ccw = [list(r[::-1]) for r in list(zip(*reversed(self._grid)))[::-1]]
        self._grid = ccw
        return self

    def flip_horizontal(self):
        self._grid = self._grid[::-1]
        return self

    def flip_vertical(self):
        return self.flip_horizontal().rotate_cw().rotate_cw()

    """
    SUM AND PRODUCT methods
    """

    def get_row_sum(self, row_idx):
        return sum([int(i) for i in self.get_row(row_idx)])

    def get_col_sum(self, col_idx):
        return sum([int(i) for i in self.get_col(col_idx)])

    def get_sum(self):
        return sum([int(i) for i in self.flatten()])

    def get_sum_if(self, if_func):
        return sum(x if if_func(x) else 0 for x in self.flatten())

    def get_row_prod(self, row_idx):
        return math.prod([int(i) for i in self.get_row(row_idx)])

    def get_col_prod(self, col_idx):
        return math.prod([int(i) for i in self.get_col(col_idx)])

    def get_prod(self):
        return math.prod(self.flatten())

    def add_at(self, col_idx: int, row_idx: int, val):
        self._grid[row_idx][col_idx] += val
        return self

    def substract_at(self, col_idx: int, row_idx: int, val):
        self._grid[row_idx][col_idx] -= val
        return self

    def add_all(self, add_val, conv_func=None):
        for col, row in self.cells.keys():
            v = self.get(col, row) + add_val
            if conv_func:
                v = conv_func(v)
            self.set(col, row, v)

    """
    REPLACE and SET methods
    """

    def set(self, col_idx: int, row_idx: int, new_val):
        self._grid[row_idx][col_idx] = new_val
        return self

    def replace_in_row(self, row_idx: int, old_val, new_val):
        self._grid[row_idx] = [new_val if i == old_val else i for i in self._grid[row_idx]]
        return self

    def set_in_row(self, row_idx: int, new_val):
        self._grid[row_idx] = [new_val for i in self._grid[row_idx]]
        return self

    def replace_in_col(self, col_idx: int, old_val, new_val):
        for row in self._grid:
            if row[col_idx] == old_val:
                row[col_idx] = new_val
        return self

    def set_in_col(self, col_idx: int, new_val):
        for row in self._grid:
            row[col_idx] = new_val
        return self

    def replace_all(self, old_val, new_val):
        for i in range(0, self.height):
            self.replace_in_row(i, old_val, new_val)
        return self

    def remove_row(self, row_id):
        del self._grid[row_id]

    def remove_col(self, col_id):
        for row in self.rows:
            del row[col_id]

    """
    FINDING AND ADJACENT
    """

    def get_adjacent(self, col_idx: int, row_idx: int, include_diagonal=True, include_self=False):
        ret = {}
        for pos_row in range(max(row_idx - 1, 0), min(row_idx + 2, self.height)):
            for pos_col in range(max(col_idx - 1, 0), min(col_idx + 2, self.width)):
                if not include_self and (pos_row == row_idx and pos_col == col_idx):
                    continue
                if not include_diagonal and not (pos_row == row_idx or pos_col == col_idx):
                    continue
                ret[(pos_col, pos_row)] = self.get(pos_col, pos_row)
        return ret

    def get_adjacent_bottom_right(self, col_idx: int, row_idx: int, include_diagonal=True):
        ret = {}
        for pos_row in range(max(row_idx, 0), min(row_idx + 2, self.height)):
            for pos_col in range(max(col_idx, 0), min(col_idx + 2, self.width)):
                if pos_row == row_idx and pos_col == col_idx:
                    continue
                if not include_diagonal and not (pos_row == row_idx or pos_col == col_idx):
                    continue
                ret[(pos_col, pos_row)] = self.get(pos_col, pos_row)
        return ret

    def find_all(self, val):
        return [(idx_col, idx_row) for idx_row, row in enumerate(self._grid) for idx_col, y in enumerate(row) if
                val == y]

    def get_uniq_values(self):
        return list(set(self.flatten()))

    def count_if(self, if_func):
        return sum(1 if if_func(x) else 0 for x in self.flatten())

    def get_value_mapping_dict(self):
        ret = {}
        for v in self.get_uniq_values():
            ret[v] = self.find_all(v)
        return ret

    def get_value_mapping(self):
        ret = []
        for v in self.get_uniq_values():
            ret.append((v, self.find_all(v)))
        return ret

    """
    MERGE
    """

    """
    ETC
    """

    def print(self, sep='\n'):
        print(*self._grid, sep=sep)
        print("")

    def pprint(self, sep='', end=''):
        for row in self.rows:
            for col in row:
                print(sep.join(str(col)), end=end)
            print("")
        print("")

    def flatten(self):
        return [el for row in self._grid for el in row]

    def __str__(self):
        return str(self.flatten())
