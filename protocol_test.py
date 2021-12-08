from secret_list_creator import create_points_list, compute_common_point_list, tuple_to_slot, point_list_to_dictionary
import random

def test_protocol(Alice_preferred_times, Bob_preferred_times):
    Alice_private_input = random.randint(1, 100)
    Bob_private_input = random.randint(1, 100)

    Alice_points, Alice_tuples = create_points_list(Alice_preferred_times, Alice_private_input)
    Bob_points, Bob_tuples = create_points_list(Bob_preferred_times, Bob_private_input)

    Alice_common_point_list = compute_common_point_list(Bob_points, Alice_private_input)
    Bob_common_point_list = compute_common_point_list(Alice_points, Bob_private_input)

    Alice_index_list = []
    Bob_index_list = []

    for i in range(0, len(Alice_common_point_list)):
        for j in range(0, len(Bob_common_point_list)):
            if Alice_common_point_list[i] == Bob_common_point_list[j]:
                Alice_index_list.append(j)
                Bob_index_list.append(i)

    Alice_good_slots = []
    Bob_good_slots = []

    for index in Alice_index_list:
        Alice_good_slots.append(tuple_to_slot(Alice_tuples[index]))

    for index in Bob_index_list:
        Bob_good_slots.append(tuple_to_slot(Bob_tuples[index]))

    if Alice_good_slots == Bob_good_slots:
        print("Meeting scheduling was succesful. Possible time slots:")
        print(Alice_good_slots)
    else:
        print("Some problem emerged during meeting scheduling.")

Alice_preferred_times = ["2021-12-10:13:30-13:45", "2021-12-10:13:45-14:00", "2021-12-10:09:30-09:45", "2021-12-10:09:45-10:00"
                        , "2021-12-10:12:15-12:30", "2021-12-10:12:30-12:45", "2021-12-10:12:45-13:00"]

Bob_preferred_times = ["2021-12-10:14:30-14:45", "2021-12-10:08:30-08:45", "2021-12-10:08:45-09:00", "2021-12-10:12:00-12:15"
                        , "2021-12-10:15:15-15:30", "2021-12-10:15:30-15:45", "2021-12-10:15:45-16:00"
                        , "2021-12-10:16:0-16:15","2021-12-10:16:15-16:30"]

print("Test with no common time slots, with 15 minutes meeting:")
test_protocol(Alice_preferred_times, Bob_preferred_times)

Alice_preferred_times = ["2021-12-10:13:30-13:45", "2021-12-10:13:45-14:00", "2021-12-10:09:30-09:45", "2021-12-10:09:45-10:00"
                        , "2021-12-10:12:15-12:30", "2021-12-10:12:30-12:45", "2021-12-10:12:45-13:00"]

Bob_preferred_times = ["2021-12-10:14:30-14:45", "2021-12-10:08:30-08:45", "2021-12-10:08:45-09:00", "2021-12-10:12:00-12:15"
                        , "2021-12-10:12:15-12:30" , "2021-12-10:15:15-15:30", "2021-12-10:15:30-15:45", "2021-12-10:15:45-16:00"
                        , "2021-12-10:16:0-16:15","2021-12-10:16:15-16:30"]

print("\nTest with common time slots, with 15 minutes meeting:")
test_protocol(Alice_preferred_times, Bob_preferred_times)

Alice_preferred_times = ["2021-12-10:13:30-14:00", "2021-12-10:13:45-14:15", "2021-12-10:09:30-10:00", "2021-12-10:09:45-10:15"
                        , "2021-12-10:10:00-10:30", "2021-12-10:10:15-10:45", "2021-12-10:10:30-11:00"
                        , "2021-12-10:12:15-12:45", "2021-12-10:12:30-13:00", "2021-12-10:13:15-13:45"]

Bob_preferred_times = ["2021-12-10:14:30-15:00", "2021-12-10:08:30-09:00", "2021-12-10:08:45-09:15", "2021-12-10:12:00-12:30"
                        , "2021-12-10:15:15-15:45", "2021-12-10:15:30-16:00", "2021-12-10:15:45-16:15"
                        , "2021-12-10:16:00-16:45","2021-12-10:16:15-16:45"]

print("\nTest with no common time slots, with 30 minutes meeting:")
test_protocol(Alice_preferred_times, Bob_preferred_times)

Alice_preferred_times = ["2021-12-10:13:30-14:00", "2021-12-10:13:45-14:15", "2021-12-10:08:30-09:00", "2021-12-10:08:45-09:15"
                        , "2021-12-10:09:30-10:00", "2021-12-10:09:45-10:15", "2021-12-10:10:00-10:30", "2021-12-10:10:15-10:45"
                        , "2021-12-10:10:30-11:00", "2021-12-10:12:00-12:30", "2021-12-10:12:15-12:45", "2021-12-10:12:30-13:00",
                         "2021-12-10:13:15-13:45"]

Bob_preferred_times = ["2021-12-10:14:30-15:00", "2021-12-10:08:30-09:00", "2021-12-10:08:45-09:15", "2021-12-10:12:00-12:30"
                        , "2021-12-10:15:15-15:45", "2021-12-10:15:30-16:00", "2021-12-10:15:45-16:15"
                        , "2021-12-10:16:00-16:45","2021-12-10:16:15-16:45"]

print("\nTest with common time slots, with 30 minutes meeting:")
test_protocol(Alice_preferred_times, Bob_preferred_times)

Alice_preferred_times = ["2021-12-10:13:30-14:15", "2021-12-10:13:45-14:30", "2021-12-10:08:30-09:15", "2021-12-10:08:45-09:30"
                        , "2021-12-10:09:30-10:15", "2021-12-10:09:45-10:30", "2021-12-10:10:00-10:45", "2021-12-10:10:15-11:00"
                        , "2021-12-10:10:30-11:15", "2021-12-10:12:00-12:45", "2021-12-10:12:15-13:00", "2021-12-10:12:30-13:15",
                         "2021-12-10:13:15-14:00"]

Bob_preferred_times = ["2021-12-10:14:30-15:15", "2021-12-10:08:15-09:00", "2021-12-10:13:00-13:45"
                        , "2021-12-10:15:30-16:15", "2021-12-10:15:45-16:30", "2021-12-10:16:00-16:45","2021-12-10:16:15-17:00"]

print("\nTest with no common time slots, with 45 minutes meeting:")
test_protocol(Alice_preferred_times, Bob_preferred_times)

Alice_preferred_times = ["2021-12-10:13:30-14:15", "2021-12-10:13:45-14:30", "2021-12-10:08:30-09:15", "2021-12-10:08:45-09:30"
                        , "2021-12-10:09:30-10:15", "2021-12-10:09:45-10:30", "2021-12-10:10:00-10:45", "2021-12-10:10:15-11:00"
                        , "2021-12-10:10:30-11:15", "2021-12-10:12:00-12:45", "2021-12-10:12:15-13:00", "2021-12-10:12:30-13:15",
                         "2021-12-10:13:15-14:00"]

Bob_preferred_times = ["2021-12-10:14:30-15:15", "2021-12-10:08:15-09:00", "2021-12-10:13:00-13:45", "2021-12-10:13:15-14:00"
                        ,"2021-12-10:13:30-14:15", "2021-12-10:15:30-16:15", "2021-12-10:15:45-16:30", "2021-12-10:16:00-16:45",
                        "2021-12-10:16:15-17:00"]

print("\nTest with common time slots, with 45 minutes meeting:")
test_protocol(Alice_preferred_times, Bob_preferred_times)