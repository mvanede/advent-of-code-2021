import timeit

depth_of_nested_lists = lambda L: isinstance(L, list) and max(map(depth_of_nested_lists, L)) + 1


def flatten_nested_lists(L):
    for l in L:
        if isinstance(l, list):
            yield from flatten_nested_lists(l)
        else:
            yield l

max_in_list = lambda lst: max(list(flatten_nested_lists(lst)))


def int_to_bits(i, len=None):
    bits =  str(bin(i))[2:]
    return bits.rjust(len, '0') if len else bits


def get_timer():
    return timeit.default_timer()


def pruntime(start_timer):
    print('Finished in {:.5f}s'.format(timeit.default_timer() - start_timer))


def panswer(a):
    print("ANSWER: {}".format(str(a)))


def get_elements_of_length(l, lst):
    return list(filter(lambda x: len(x)==l, lst))


def most_common(lst):
    return max(set(lst), key=lst.count)


def least_common(lst):
    return min(set(lst), key=lst.count)