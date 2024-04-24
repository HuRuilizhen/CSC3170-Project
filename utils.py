import db
def convert_time_to_24hr_format(time_str):
    time, period = time_str.split()
    hour, minute = map(int, time.split(':'))
    if period.upper() == 'PM' and hour != 12:
        hour += 12
    if period.upper() == 'AM' and hour == 12:
        hour = 0
    return f"{hour:02d}:{minute:02d}"

def cal_gpa(student_id, mul = 0.7):
    query = f"SELECT * FROM course_selection where student_id = {student_id}"
    data = db.load_data(query)
    grade_lst = data['grade'].to_list()
    # What is A+?
    gpa_map = {'A+': 4.3, 'A': 4, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7, 'C': 2, 'D': 1, 'F': 0}
    total_credit = 0
    score = 0
    for grade in grade_lst:
        if gpa_map.get(grade) != None:
            total_credit += 3
            score += 3 * gpa_map[grade]
    gpa = score / total_credit * mul
    if gpa > 3.5:
        emoji = "😝"
    elif gpa > 3.0:
        emoji = "🥰"
    elif gpa > 2.5:
        emoji = "🥺"
    elif gpa > 1.5:
        emoji = "😡"
    else:
        emoji = "🤡"
    return gpa, emoji
