from secret_list_creator import create_points_list, compute_common_point_list, tuple_to_slot
import random

Alice_prefered_times = ["13:30-14:45", "09:30-10:00", "12:15-13:00"]

Bob_prefered_times = ["14:30-14:45", "08:30-09:00", "12:00-12:15", "15:00-16:30"]

Alice_private_input = random.randint(1, 100)
Bob_private_input = random.randint(1, 100)

Alice_points, Alice_tuples = create_points_list(Alice_prefered_times, 15, Alice_private_input)
Bob_points, Bob_tuples = create_points_list(Bob_prefered_times, 15, Bob_private_input)

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

print(Alice_good_slots)
print(Bob_good_slots)
