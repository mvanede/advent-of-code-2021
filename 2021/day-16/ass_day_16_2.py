from utils.lib import get_timer, panswer, pruntime

import math
_ST = get_timer()
f = open("ass-day-16-input.txt", "r")


def hex_to_bitstr(hexstr):
    return ''.join([bin(int(c, 16))[2:].rjust(4,'0')  for c in hexstr])


def read_next_literal(bitstr):
    packet_version = bitstr[0:3]
    packet_type_id = bitstr[3:6]
    rest_of_string = bitstr[6:]

    # LITERAL
    val = []
    _reached_last_part = False
    while not _reached_last_part:
        val.append(rest_of_string[1:5])

        # Indicates last part of this packet
        if rest_of_string[0] == '0':
            _reached_last_part = True
        rest_of_string = rest_of_string[5:]

    return {
        'packet_version': int(packet_version, 2),
        'packet_type_id': int(packet_type_id, 2),
        'val': int(''.join(val), 2)
    }, rest_of_string


def read_next(bitstr, stop_at_one = False):
    packets = []

    while len(bitstr) and int(bitstr, 2) > 0 and not (stop_at_one and len(packets) == 1):
        packet_version = bitstr[0:3]
        packet_type_id = bitstr[3:6]

        # LITERAL
        if int(packet_type_id, 2) == 4:
            literal, rest_of_string = read_next_literal(bitstr)
            packets.append(literal)
        # OPERATOR
        else:
            rest_of_string = bitstr[6:]  # remove packet version and type
            length_type_id = rest_of_string[0]
            rest_of_string = rest_of_string[1:]

            if length_type_id == '0':
                # If the length type ID is 0, then the  next 15 bits are a number that represents the  total length
                total_length = int(rest_of_string[0:15], 2)
                rest_of_string = rest_of_string[15:]

                v, r = read_next(rest_of_string[:total_length])
                rest_of_string = rest_of_string[total_length:]

                packets.append({
                    'packet_version': int(packet_version, 2),
                    'packet_type_id': int(packet_type_id, 2),
                    'val': v
                })
            else:
                # If the length type ID is 1, then the next 11 bits are a number that represents the number of sub-packets immediately contained by this packet.
                total_nr_subpackets = int(rest_of_string[0:11], 2)
                rest_of_string = rest_of_string[11:]
                subpackets = []

                for i in range(total_nr_subpackets):
                    v, rest_of_string = read_next(rest_of_string, True)
                    subpackets.append(v[0])

                packets.append({
                    'packet_version': int(packet_version, 2),
                    'packet_type_id': int(packet_type_id, 2),
                    'val': subpackets
                })

        bitstr = rest_of_string

    return packets, bitstr


def get_value(_packet):
    if _packet['packet_type_id'] == 4:
        return _packet['val']

    elif _packet['packet_type_id'] == 0:
        return sum([get_value(p) for p in _packet['val']])

    elif _packet['packet_type_id'] == 1:
        return math.prod([get_value(p) for p in _packet['val']])

    elif _packet['packet_type_id'] == 2:
        return min([get_value(p) for p in _packet['val']])

    elif _packet['packet_type_id'] == 3:
        return max([get_value(p) for p in _packet['val']])

    elif _packet['packet_type_id'] == 3:
        return max([get_value(p) for p in _packet['val']])

    elif _packet['packet_type_id'] == 5:
        sub_vals = [get_value(p) for p in _packet['val']]
        return 1 if sub_vals[0] > sub_vals[1] else 0

    elif _packet['packet_type_id'] == 6:
        sub_vals = [get_value(p) for p in _packet['val']]
        return 1 if sub_vals[0] < sub_vals[1] else 0

    elif _packet['packet_type_id'] == 7:
        sub_vals = [get_value(p) for p in _packet['val']]
        return 1 if sub_vals[0] == sub_vals[1] else 0


def sum_value(_packets):
    s = 0
    for p in _packets:
        s += get_value(p)
    return s


# READ AND PROCESS
x = hex_to_bitstr(f.read())
packets, remaining = read_next(x)

panswer(sum_value(packets))
pruntime(_ST)


# 246225449979