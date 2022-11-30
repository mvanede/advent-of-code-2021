from utils import Parser
from utils.lib import get_timer, panswer, pruntime
import math
import ast
_ST = get_timer()


def to_tree(_root_node, data):
    left = data[0]
    right = data[1]

    _node = Node(parent=_root_node)
    _node.left = IntWrapper(left) if isinstance(left, int) else to_tree(_node, left)
    _node.right = IntWrapper(right) if isinstance(right, int) else to_tree(_node, right)
    return _node


class IntWrapper:
    def __init__(self, v):
        self.v = v

    def __str__(self):
        return str(self.v)

    def __repr__(self):
        return str(self.v)


class Node():
    def __init__(self, value=None, left=None, right=None, parent=None):
        self.left = left
        self.right = right
        self.value = value
        self.parent = parent

    def isllist(self):
        return isinstance(self.left, Node)

    def isrlist(self):
        return isinstance(self.right, Node)

    def islint(self):
        return isinstance(self.left, IntWrapper)

    def isrint(self):
        return isinstance(self.right, IntWrapper)

    """
        From your parent, go up until we've found a node with 
    """
    def find_first_left(self):
        p = self

        while p.parent and p.parent.left is p :
            p = p.parent

        if p.parent and p.parent.left:
            p = p.parent.left
            if isinstance(p, IntWrapper):
                return p

            while not isinstance(p.right, IntWrapper):
                p = p.right
            return p.right
        return None

    def find_first_right(self):
        p = self
        while p.parent and p.parent.right is p :
            p = p.parent

        if p.parent and p.parent.right:
            p = p.parent.right
            if isinstance(p, IntWrapper):
                return p

            while not isinstance(p.left, IntWrapper):
                p = p.left
            return p.left
        return None

    def _addition(self):
        if self.isllist() or self.isrlist():
            change_happened = False
            if self.isllist():
                self.left, change_happened = self.left._addition()
            elif self.isrlist() and not change_happened:
                self.right, change_happened = self.right._addition()
            return self, change_happened
        else:
            fl = self.find_first_left()
            if fl:
                fl.v += self.left.v

            fr = self.find_first_right()
            if fr:
                fr.v += self.right.v

            return IntWrapper(0), True

    def _do_explodes(self, _depth=0):
        changed_happened = False

        if _depth == 4:
            print("explode=" + str(self))
            return self._addition()

        if self.isllist() and not changed_happened:
            self.left, changed_happened = self.left._do_explodes(_depth + 1)

        if self.isrlist() and not changed_happened:
            self.right, changed_happened = self.right._do_explodes(_depth + 1)

        return self, changed_happened

    def _do_splits(self, _depth=0):
        changed_happened = False

        if self.isllist() and not changed_happened:
            self.left, changed_happened = self.left._do_splits(_depth + 1)

        if self.islint() and self.left.v >= 10 and not changed_happened:
            print("split="+str(self.left.v))
            self.left = Node(left=IntWrapper(math.floor(self.left.v/2)), right=IntWrapper(math.ceil(self.left.v/2)), parent=self)
            changed_happened = True

        if self.isrlist() and not changed_happened:
            self.right, changed_happened = self.right._do_splits(_depth + 1)

        if self.isrint() and self.right.v >= 10 and not changed_happened:
            print("split=" + str(self.right.v))
            self.right = Node(left=IntWrapper(math.floor(self.right.v / 2)),
                              right=IntWrapper(math.ceil(self.right.v / 2)), parent=self)
            changed_happened = True

        return self, changed_happened

    def reduce(self, _depth=0):
        _s, changed_happened = self._do_explodes(_depth)

        if changed_happened:
            return _s, changed_happened
        return self._do_splits()

    def to_list(self):
        l = self.left.to_list() if self.isllist() else self.left.v
        r = self.right.to_list() if self.isrlist() else self.right.v
        return [l, r]

    def get_magnitude(self):
        lft = self.left.v if isinstance(self.left, IntWrapper) else self.left.get_magnitude()
        rght = self.right.v if isinstance(self.right, IntWrapper) else self.right.get_magnitude()
        return 3*lft + 2*rght

    def __str__(self):
        return str([self.left, self.right])

    def __repr__(self):
        return str([self.left, self.right])


def main():
    f = open("ass_day_18_input.txt", "r")
    commands = Parser.split_by(f.read(), "\n", conv_func=None)  # lambda x:int(x)
    numbers = [ast.literal_eval(x) for x in commands]

    # Sum up all
    current = to_tree(None, numbers[0])
    for next_to_add in numbers[1:]:
        tree = to_tree(None, [current.to_list(), next_to_add])

        changed = True
        while changed:
            tree, changed = tree.reduce()
        current = tree

    panswer(current.get_magnitude())


main()
pruntime(_ST)
# 3486
