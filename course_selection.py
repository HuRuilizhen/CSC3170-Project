
import streamlit as st
import db
import utils
import timetable
import course_manager

def main(group,username):
    if group == "admin":
        admin()
    else:
        user(username)
def admin():
    st.subheader("Student List")
    query = "SELECT * FROM student_info"
    data = db.load_data(query)
    if not data.empty:
        st.dataframe(data)
    else:
        st.write("No data found in the student list.")


def user(username):
    st.subheader("Course Selections")
    query = "SELECT * FROM course_selection"
    data = db.load_data(query)
    if not data.empty:
        # TODO
        #-----------------------------------------
        # admin
        if st.session_state["page"] == 1:
            search_student_query = st.text_input("Search student:", "")
            # search student's selections
            if search_student_query:
                filtered_data = data[data['student_id'] == int(search_student_query)]
                gpa, emoji = utils.cal_gpa(search_student_query, 1)
                st.write(f"student {search_student_query}'s GPA is")
                st.subheader(f"{format(gpa, '.3f')} {emoji}")
            else:
                filtered_data = data
            # show the selection table
            st.dataframe(filtered_data)

            # data analysis graph
            st.subheader("Course Selection Distribution")
            query = "SELECT DISTINCT subject FROM course_list"
            data = db.load_data(query)
            subjects_list = data['subject'].to_list()
            selected_subject = st.selectbox('Filter by subject:', subjects_list)
            if selected_subject:
                distribution_button = st.button("Generate Distribution")
                if distribution_button:
                    query = f"SELECT course_number, year, term, COUNT(*) AS selection_number FROM course_selection WHERE course_subject = \'{selected_subject}\' GROUP BY course_number, year, term" 
                    data = db.load_data(query)
                    if not data.empty:
                        st.bar_chart(data, x='course_number', y='selection_number', color='year')
                    else:
                        st.write("There are no courses selected for this subject")
                
        # student
        else:
            
            gpa, emoji = utils.cal_gpa(username, 1)
            filtered_data = data[data['student_id'] == int(username)]
            st.header("Your GPA is")
            st.title(f"{format(gpa, '.3f')} {emoji}")
            st.dataframe(filtered_data)

            timetable_button = st.button("generate time table")
            if timetable_button:
                query = f"""SELECT DISTINCT CONCAT(cl.subject, cl.number) AS course_key, cl.type_code, cl.days_of_week, cl.start_time, cl.end_time 
                                FROM course_section AS cl INNER JOIN (
                                    SELECT course_subject, course_number 
                                    FROM course_selection 
                                    WHERE student_id = \'{username}\') 
                                AS cs ON cs.course_subject = cl.subject AND cs.course_number = cl.number 
                                WHERE start_time != \'ARRANGED\'
                                """
                data = db.load_data(query)

                sections = []
                for index, row in data.iterrows():
                    course_key = row['course_key']
                    type_code = row['type_code']
                    days_of_week = row['days_of_week']
                    start_time = utils.convert_time_to_24hr_format(row['start_time'])
                    end_time = utils.convert_time_to_24hr_format(row['end_time'])
                    
                    sections.append([course_key, type_code, days_of_week, start_time, end_time])

                selected_sections = course_manager.find_best(course_manager.get_combinations(sections))
                if selected_sections is None:
                    st.write("Course time conflict, unable to generate")
                else:
                    fig = timetable.draw_time_table(selected_sections)
                    st.write("Only show courses with confirmed course times")
                    st.pyplot(fig)
                
        #-----------------------------------------
    else:
        st.write("No data found in the course selections.")


  
   