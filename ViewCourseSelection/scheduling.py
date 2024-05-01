from collections import defaultdict
import itertools
import random

'''
Function: check_arrangement()
This function takes a list of sections and return true if the arrangement is valid, false otherwise.
Input: a 2d-list. Each row represents a section. Columns: day, start time, end time.
'''
def time_to_min(time):
    h, m = map(int, time.split(':'))
    return h * 60 + m

def check_arrangement(section_times):
    week = {'M': [], 'T': [], 'W': [], 'R': [], 'F': [], 'S': [], 'U': []}
    for days, start, end in section_times:
        start_minutes = time_to_min(start)
        end_minutes = time_to_min(end)
        for day in days:
            week[day].append((start_minutes, end_minutes))
    
    for day, times in week.items():
        times.sort()
        last_end_time = 0
        for start, end in times:
            if start < last_end_time:
                return False
            last_end_time = end
    
    return True

'''
Here is an example of how to use the function
'''
# schedule = [
#     ['MW', '13:30', '15:00'],
#     ['T', '14:00', '15:30'],
#     ['W', '16:00', '13:45'],
#     ['F', '11:00', '12:00']
# ]
# print(check_arrangement(schedule))


'''
Function: best_arrange()
This function takes a list of sections and returns the best arrangement of sections that have the latest start time 
and the fewest number of sections that start at the ealiest time.
Input: a 2d-list. Each row represents a section. Columns: course, section, day, start time, end time.
'''

def get_combinations(sections):
    courses = defaultdict(lambda: defaultdict(list))
    for course_id, type_id, day, start, end in sections:
        courses[course_id][type_id].append((day, start, end, type_id))
    
    for course_id in courses:
        for type_id in courses[course_id]:
            courses[course_id][type_id].sort(key = lambda x: time_to_min(x[1]))

    all_combinations = []
    for course_id in courses:
        type_combinations = list(itertools.product(*[courses[course_id][type_id] for type_id in courses[course_id]]))
        all_combinations.append([(course_id, *combo) for combo in type_combinations])
    
    combinations = []
    for combination in itertools.product(*all_combinations):
        flattened_combination = [item for sublist in combination for item in sublist]
        # print(flattened_combination)
        check_list = []
        for item in flattened_combination:
            if isinstance(item, tuple):
                check_list.append([item[0], item[1], item[2]])
        if check_arrangement(check_list):
            combinations.append(flattened_combination)

    return combinations

def find_best(combinations):
    best_combinations = []
    latest_earliest_time = -1
    min_earliest_count = float('inf')
    
    for combo in combinations:
        start_times = [time_to_min(session[1]) for session in combo if isinstance(session, tuple)]
        if not start_times:
            continue
        earliest_time = min(start_times)
        earliest_count = start_times.count(earliest_time)
        
        if earliest_time > latest_earliest_time:
            latest_earliest_time = earliest_time
            min_earliest_count = earliest_count
            best_combinations = [combo]
        elif earliest_time == latest_earliest_time:
            if earliest_count < min_earliest_count:
                min_earliest_count = earliest_count
                best_combinations = [combo]
            elif earliest_count == min_earliest_count:
                best_combinations.append(combo)

    if len(best_combinations) == 0:
        return None
    return random.choice(best_combinations)

'''
Here is an example of how to use the function
'''
# sections = [
#     ['Math101', 'LEC', 'MW', '08:00', '09:30'],
#     ['Math101', 'LEC', 'T', '15:00', '16:30'],
#     ['Math101', 'TUT', 'MW', '13:00', '14:30'],
#     ['Math101', 'TUT', 'T', '09:00', '10:30'],
#     ['Math101', 'LAB', 'F', '14:00', '15:30'],
#     ['CS101', 'LEC', 'MW', '13:00', '14:30'],
#     ['CS101', 'LEC', 'T', '09:00', '10:30'],
#     ['CS101', 'TUT', 'F', '12:00', '13:30'],
#     ['CS101', 'TUT', 'MW', '10:00', '11:30'],
# ]
# selected_sections = find_best(get_combinations(sections))
# print(selected_sections)