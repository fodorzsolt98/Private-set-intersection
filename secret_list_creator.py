import tinyec.ec as ec
import tinyec.registry as reg
from mod_square_root import square_root
from hashlib import sha256

import math


def int_to_bytes(number):
    number_bytes_length = math.ceil((len(bin(number)) - 2)  / 8)
    return (number).to_bytes(number_bytes_length, byteorder="big")


def slots_to_tuples(slot_list, meeting_time):
    if not(meeting_time == 15 or meeting_time == 30 or meeting_time == 60):
        raise Exception("15, 30 or 60 minutes long meetings can be scheduled only.")
    converted_slot_list = []
    for slot in slot_list:
        start_time, end_time = slot.split("-")
        first_start = int(start_time.split(":")[0]) * 60 + int(start_time.split(":")[1])
        last_end = int(end_time.split(":")[0]) * 60 + int(end_time.split(":")[1])

        meeting_start = first_start

        all_slots_added = False

        while not all_slots_added:
            if meeting_start + meeting_time <= last_end:
                converted_slot_list.append((meeting_start, meeting_start + meeting_time))
                meeting_start = meeting_start + 15
                if meeting_start >= last_end:
                    all_slots_added = True

    return converted_slot_list

def at(a, b, p, x):
    assert x < p
    ysq = (x ** 3 + a * x + b) % p
    y = square_root(ysq, p)
    return y

def int_list_from_tuple_list(tuple_list):
    int_list = []
    for tuple in tuple_list:
        concatenated_int = int(str(tuple[0]) + str(tuple[1]))
        int_list.append(concatenated_int)

    return int_list

def create_points_list(slot_list, meeting_time, private_input):
    slot_tuple_list = slots_to_tuples(slot_list, meeting_time)

    integer_list = int_list_from_tuple_list(slot_tuple_list)

    points_list = []

    c = reg.get_curve("secp192r1")

    for integer in integer_list:
        hash_okay = False
        int_to_hash = integer
        while not hash_okay:
            x = int.from_bytes(sha256(int_to_bytes(int_to_hash)).digest(), "big") % c.field.p
            y = at(c.a, c.b, c.field.p, x)
            if y != -1:
                points_list.append(ec.Point(c, x, y))
                hash_okay = True
            else:
                int_to_hash = x

    multiplied_point_list = []

    for point in points_list:
        multiplied_point_list.append(private_input * point)

    return multiplied_point_list


