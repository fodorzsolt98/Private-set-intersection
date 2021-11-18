def slots_to_integers(slot_list, meeting_time):
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