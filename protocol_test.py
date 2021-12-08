from secret_list_creator import create_points_list, compute_common_point_list, tuple_to_slot, point_list_to_dictionary
import random

Alice_prefered_times = ["2021-12-10:13:30-13:45", "2021-12-10:13:45-14:00", "2021-12-10:09:30-09:45", "2021-12-10:09:45-10:00"
                        , "2021-12-10:12:15-12:30", "2021-12-10:12:30-12:45", "2021-12-10:12:45-13:00"]

Bob_prefered_times = ["2021-12-10:14:30-14:45", "2021-12-10:08:30-08:45", "2021-12-10:08:45-09:00", "2021-12-10:12:00-12:15"
                        , "2021-12-10:15:15-15:30", "2021-12-10:15:30-15:45", "2021-12-10:15:45-16:00"
                        , "2021-12-10:16:0-16:15","2021-12-10:16:15-16:30"]

Alice_private_input = random.randint(1, 100)
Bob_private_input = random.randint(1, 100)

Alice_points, Alice_tuples = create_points_list(Alice_prefered_times, Alice_private_input)
Bob_points, Bob_tuples = create_points_list(Bob_prefered_times, Bob_private_input)

Alice_common_point_list = compute_common_point_list(Bob_points, Alice_private_input)
Bob_common_point_list = compute_common_point_list(Alice_points, Bob_private_input)

dicti = point_list_to_dictionary(Alice_common_point_list)

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

print(Alice_good_slots)
print(Bob_good_slots)
