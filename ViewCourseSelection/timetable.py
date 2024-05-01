import matplotlib.pyplot as plt
import matplotlib.patches as patches
import streamlit as st

def draw_time_table(selected_sections):
    fig, ax = plt.subplots()

    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', '#b4d092']
    days_map = {'M': 1, 'T': 2, 'W': 3, 'R': 4, 'F': 5, 'S': 6, 'U': 7}

    color = ""
    course_name = ""

    ylist = []

    for ele in selected_sections:
        if isinstance(ele, str):
            # color = colors.pop(0)
            # colors.append(color)
            color = '#b4d092'
            course_name = ele

        elif isinstance(ele, tuple):
            days, start_time, end_time, course_type = ele
            hours, minutes = map(int, end_time.split(':'))
            end_minutes = hours * 60 + minutes
            hours, minutes = map(int, start_time.split(':'))
            start_minutes = hours * 60 + minutes
            course_time = end_minutes - start_minutes
            for day in days:
                day_pos = days_map[day]
                rectangle = patches.Rectangle((day_pos - 0.5, 1440 - end_minutes), 1, course_time, linewidth=1, edgecolor='#5b9922', facecolor=color, zorder=10)
                ax.text(day_pos, 1440 - end_minutes + course_time / 2, course_name + '\n' + course_type, ha='center', va='center', fontsize=8, color='#1d1a75', zorder=15)
                ylist.append([1440 - end_minutes, end_time])
                ylist.append([1440 - start_minutes, start_time])
                ax.add_patch(rectangle)

    ylabel_list = sorted(ylist, key=lambda x: x[0])
    yticks = [item[0] for item in ylabel_list]
    yticklabels = [item[1] for item in ylabel_list]

    x_positions = [1.5, 2.5, 3.5, 4.5, 5.5, 6.5]
    for pos in x_positions:
        plt.axvline(x=pos, color='#c1c9db', linestyle='-')

    ax.set_xlim(0, 7)
    ax.set_ylim(yticks[0] - 100 if yticks[0] - 100 > 0 else 0, yticks[-1] + 100 if yticks[-1] + 100 < 1440 else 1440)
    ax.set_xticks([1, 2, 3, 4, 5, 6, 7, 8])
    ax.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', ''])  
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels)
    
    ax.set_xlabel('Day')
    ax.set_ylabel('Time')
    ax.grid(True, axis='y', zorder=0, color='#c1c9db')
    return fig


