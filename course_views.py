import streamlit as st
import chatbot
import db

def handle_courses_view():
    st.subheader("Course List")
    # Add the details for the courses view here, possibly using sql_generator.py for SQL logic

def handle_course_selections(username):
    st.subheader("Course Selections")
    # Add the logic for viewing course selections

def main(username):
    st.subheader("Course List")

    # Assuming 'subject' is a column in your 'course_list' table.
    # First, get the list of unique subjects for the filter
    selected_query = st.selectbox('query mode', ['AI generate', 'Conditional filtering'])
    if selected_query == 'AI generate':
        st.title("UWD Database AI Query Assistant")

        # Selection between LLMs
        llm_choice = st.radio("Select the Language Model to Generate SQL", ('Dashscope LLM', 'GPT 3.5'))

        # Area for user input
        user_input = st.text_area("Enter your query:")
        assistant_output = ""
        if st.button("Get AI Generated SQL") and user_input != "":
            chatbot.messages.append({"role": "user", "content": user_input})
    
            # Conditional call based on LLM selection
            if llm_choice == 'Dashscope LLM':
                # Call the get_response function to get a response from dashscope
                response = chatbot.get_dashscope_response(chatbot.messages)
                assistant_output = response["output"]["choices"][0]["message"]["content"]
            else:
                # Call the get_response function to get a response from GPT 3.5
                assistant_output = chatbot.get_gpt_response(chatbot.messages)
            
            # Display the AI generated SQL to the user
            #st.text_area("AI Generated SQL", assistant_output, height=300)
            print(assistant_output)
        

        if assistant_output != "":
            add_index = 3
            start_index = assistant_output.find("```sql")
            if start_index != -1:
                add_index = 6
            else:
                start_index = assistant_output.find("```")
            end_index = assistant_output.rfind("```")
            if start_index != -1 and end_index != -1:
                assistant_output = assistant_output[start_index+add_index:end_index]
            query = assistant_output
            print(query)
            sub_query = query[0:query.find("FROM")]


            data = db.load_data(query)
            if not data.empty:
                st.dataframe(data)
            else:
                st.write("No data for this condition")

    elif selected_query == 'Conditional filtering':
        subjects_query = "SELECT DISTINCT subject FROM course_list"
        subjects_data = db.load_data(subjects_query)
        subjects_list = subjects_data['subject'].tolist() if not subjects_data.empty else []
        # Create a selectbox widget for subjects
        selected_subject = st.selectbox('Filter by subject:', ['All'] + subjects_list)
        # Modify the query based on the selected subject
        
        if selected_subject != 'All':
            query = f"""
                        SELECT cl.*, cs.CRN, cs.section, cs.status_code, cs.part_of_term, cs.section_title, cs.section_credit_hours,
                            cs.section_status, cs.enrollment_status, cs.type, cs.type_code, cs.start_time, cs.end_time, cs.days_of_week,
                            cs.room, cs.building, cs.instructors
                        FROM course_list AS cl
                        INNER JOIN course_section AS cs 
                        ON cl.subject = cs.subject
                            AND cl.number = cs.number
                            AND cl.year_term = cs.year_term
                            WHERE cl.subject = \'{selected_subject}\'
                        """
        else:
            query = """
                    SELECT cl.*, cs.CRN, cs.section, cs.status_code, cs.part_of_term, cs.section_title, cs.section_credit_hours,
                        cs.section_status, cs.enrollment_status, cs.type, cs.type_code, cs.start_time, cs.end_time, cs.days_of_week,
                        cs.room, cs.building, cs.instructors
                    FROM course_list AS cl
                    INNER JOIN course_section AS cs 
                    ON cl.subject = cs.subject
                        AND cl.number = cs.number
                        AND cl.year_term = cs.year_term;
                    """

        # Fetch and display the data based on the query
        data = db.load_data(query)
        if not data.empty:

            # List of all possible columns fetched dynamically from the dataframe
            all_columns = data.columns.tolist()
        
            default_columns = ['year_term', 'subject', 'name', 'instructors', 'description']

            # Filter out any default columns not present in the actual data to avoid errors
            valid_defaults = [col for col in default_columns if col in all_columns]

            # Let users choose which columns to display, with some defaults pre-selected
            selected_columns = st.multiselect('Select columns to display:', all_columns, default=valid_defaults)
            search_query = st.text_input("Search by course name:", "")

            # Filter data based on search query if provided
            if search_query:
                filtered_data = data[data['name'].str.contains(search_query, case=False, na=False)]
            else:
                filtered_data = data

            if selected_columns and not filtered_data.empty:
                st.dataframe(filtered_data[selected_columns])
            elif not selected_columns:
                st.write("Please select at least one column to display.")
            else:
                st.write(f"No courses found with the name '{search_query}'.")
        else:
            st.write(f"No data found for subject: {selected_subject}")
    else:
        st.write("something wrong")
    

    # OCTE
    st.subheader("Course OCTE")
    query = "SELECT DISTINCT subject FROM course_list"
    data = db.load_data(query)
    subjects_list = data['subject'].to_list()
    selected_subject = st.selectbox('subject (octe):', subjects_list)
    if selected_subject:
        query = f"SELECT DISTINCT number FROM course_list WHERE subject = \'{selected_subject}\'"
        filtered_data = db.load_data(query)
        if not filtered_data.empty:
            numbers_list = filtered_data['number'].to_list()
            selected_number = st.selectbox('number (octe):', numbers_list)
            if selected_number:
                octe_button = st.button("generate OCTE")
                if octe_button:
                    query = f"SELECT octe, COUNT(*) AS number FROM course_selection WHERE course_subject = \'{selected_subject}\' AND course_number = {selected_number} GROUP BY octe ORDER BY octe"
                    filtered_data = db.load_data(query)
                    if not filtered_data.empty:
                        mean = 0
                        mean_num = 0
                        for index, row in filtered_data.iterrows():
                            octe_value = row['octe']
                            number_value = row['number']
                            mean += octe_value * number_value
                            mean_num += number_value
                        mean /= mean_num
                        st.write(f"Mean: {format(mean, '.3f')}")
                        st.bar_chart(filtered_data, x='octe', y='number')
                    else:
                        st.write("No octe for this course")

    # TEST ONLY
    if st.session_state["page"] != 1:
        st.subheader("Add Course")
        # Get the subject list
        query = "SELECT DISTINCT subject FROM course_list"
        data = db.load_data(query)
        subjects_list = data['subject'].to_list()
        selected_subject = st.selectbox('subject (add):', subjects_list)
        # Subject confirmed
        if selected_subject:
            # Get the list of course numbers corresponding to the subject
            query = f"SELECT DISTINCT number FROM course_list WHERE subject = \'{selected_subject}\'"
            filtered_data = db.load_data(query)
            if not filtered_data.empty:
                numbers_list = filtered_data['number'].to_list()
                selected_number = st.selectbox('number (add):', numbers_list)
                # Course number confirmed
                if selected_number:
                    submit_button = st.button("submit")
                    # Submit!
                    if submit_button:
                        # Confirm whether the course has been selected
                        query = f"SELECT course_key FROM course_selection WHERE student_id = {username}"
                        filtered_data = db.load_data(query)
                        course_key_set = set(filtered_data["course_key"].to_list())
                        # the course hasn't been selected
                        if f"(\'{selected_subject}\', {selected_number})" not in course_key_set:
                            # Insert sql query
                            query = f"INSERT INTO course_selection VALUES (NULL, {username}, \'{selected_subject}\', {selected_number}, 2024, \'Spring\', \'Unknown\', -1, \'(\\\'{selected_subject}\\\', {selected_number})\')"
                            res = db.insert_data(query)
                            if res == True:
                                st.success("submit success")
                            else:
                                st.error("submit error")
                        else:
                            st.error("You have selected this course")
            else:
                st.error("Oops, something went wrong")

        else:
            st.write(f"No data found for subject: {selected_subject}")
    


    