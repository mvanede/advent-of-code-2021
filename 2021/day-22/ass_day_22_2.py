from utils import Parser
from utils.lib import get_timer, panswer, pruntime
_ST = get_timer()


class Point():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "({}, {}, {})".format(self.x, self.y, self.z)


class Region():
    def __init__(self, corner1, corner2, state = 'on'):
        self.corner1 = corner1
        self.corner2 = corner2
        self.excluded = []
        self.state = state

    @property
    def volume(self):
        # +1, because 0,3 prresent 4 cubes (at 0, 1, 2 and 3)
        base_volume = abs(self.corner2.x-self.corner1.x + 1) * abs(self.corner2.y-self.corner1.y + 1) * abs(self.corner2.z-self.corner1.z + 1)
        for e in self.excluded:
            base_volume -= e.volume
        return base_volume

    def _compare_axis(self, line1, line2):
        if line1[0] > line2[1] or line1[1] < line2[0]:
            return None

        vals = list(line1) + list(line2)
        vals.sort()
        return vals[1], vals[2]

    def get_overlap(self, other):
        x_overlap = self._compare_axis((self.corner1.x, self.corner2.x), (other.corner1.x, other.corner2.x))
        y_overlap = self._compare_axis((self.corner1.y, self.corner2.y), (other.corner1.y, other.corner2.y))
        z_overlap = self._compare_axis((self.corner1.z, self.corner2.z), (other.corner1.z, other.corner2.z))

        if not x_overlap or not y_overlap or not z_overlap:
            return None

        return Region(Point(x_overlap[0], y_overlap[0], z_overlap[0]), Point(x_overlap[1], y_overlap[1], z_overlap[1]))

    def subtract(self, other):
        overlap = self.get_overlap(other)
        if overlap:
            # Can also overlap with existing excluded regions, so exclude the exclusion from them too :)
            for e in self.excluded:
                e.subtract(overlap)
            self.excluded.append(overlap)

        return overlap

    def __str__(self):
        return "{}, {}".format(self.corner1,  self.corner2)



"""
Proces inputfile
"""
f = open("ass_day_22_input.txt", "r")
commands = Parser.split_by(f.read(), "\n"," ", conv_func=None)  # lambda x:int(x)

instructions = []
for c in commands:
    on_off = c[0]
    coords = c[1].split(",")

    # Build Region
    _ = []
    for coord in coords:
        axis, vals = coord.split("=")
        start, end = vals.split("..")
        _.append((int(start), int(end)))

    r = Region(Point(_[0][0], _[1][0], _[2][0]), Point(_[0][1], _[1][1], _[2][1]), on_off)
    instructions.append(r)


"""
Loop over each region. If region overlaps with any of previous region, subtract
"""
processed_regions = [instructions[0]]
for instruction in instructions[1:]:
    for region in processed_regions:
        region.subtract(instruction)
    processed_regions.append(instruction)


# Count on/off states
endstate = {
    'on': 0,
    'off': 0
}
for region in processed_regions:
    endstate[region.state] += region.volume

panswer(endstate)
pruntime(_ST)

# 1263946820845866
