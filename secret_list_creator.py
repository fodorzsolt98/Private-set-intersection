import tinyec.ec as ec
import tinyec.registry as reg
from mod_square_root import square_root
from hashlib import sha256

import math


def int_to_bytes(number):
    number_bytes_length = math.ceil((len(bin(number)) - 2) / 8)
    return (number).to_bytes(number_bytes_length, byteorder="big")


def point_list_to_dictionary(points_list):
    point_dict = {}
    for i in range(0, len(points_list)):
        point_dict[i] = {"x" : points_list[i].x, "y" : points_list[i].y}
    return point_dict

def point_list_from_dictionary(point_dictionary):
    c = reg.get_curve("secp192r1")
    points_list = []
    for index in point_dictionary:
        points_list.append(ec.Point(c, point_dictionary[index]["x"], point_dictionary[index]["y"]))

    return points_list


def slots_to_tuples(slot_list):
    converted_slot_list = []
    for slot in slot_list:
        date, daytime = slot.split(":", 1)
        start_time, end_time = daytime.split("-")
        start_integer = int(start_time.split(":")[0]) * 60 + int(start_time.split(":")[1])
        end_integer = int(end_time.split(":")[0]) * 60 + int(end_time.split(":")[1])

        year, month, day = date.split("-")

        converted_slot_list.append((int(year + month + day + str(start_integer))
                                    , int(year + month + day + str(end_integer))))

    return converted_slot_list

def tuple_to_slot(slot_tuple):
    start_full = str(slot_tuple[0])
    end_full = str(slot_tuple[1])
    start_year = start_full[0:4]
    end_year = end_full[0:4]
    start_month = start_full[4:6]
    end_month = end_full[4:6]
    start_day = start_full[6:8]
    end_day = end_full[6:8]
    start_time_integer = int(start_full[8:])
    end_time_integer = int(end_full[8:])
    start_hours = start_time_integer // 60
    start_minutes = start_time_integer % 60
    end_hours = end_time_integer // 60
    end_minutes = end_time_integer % 60
    return start_year + "-" + start_month + "-" + start_day + ":" +str(start_hours) + ":" + str(start_minutes) + "-"\
           + str(end_hours) + ":" + str(end_minutes)

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

def create_points_list(slot_list, private_input):
    slot_tuple_list = slots_to_tuples(slot_list)

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

    return multiplied_point_list, slot_tuple_list

def compute_common_point_list(other_party_point_list, private_value):
    common_point_list = []
    for point in other_party_point_list:
        common_point_list.append(point * private_value)

    return common_point_list

def compute_index_lists_for_free_slots(party1_points_list, party2_points_list):
    party1_index_list = []
    party2_index_list = []

    for i in range(0, len(party1_points_list)):
        for j in range(0, len(party2_points_list)):
            if party1_points_list[i] == party2_points_list[j]:
                party1_index_list.append(j)
                party2_index_list.append(i)

    return party1_index_list, party2_index_list