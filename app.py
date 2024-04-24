import streamlit as st
import login
import config
import course_views
import db
import course_selection
import course_recommendation

def homepage(group):

    st.title("WcDonald's")
    config.set_bg("background.jpg")
    db.get_db_connection()
    
    username = str(st.session_state["page"])
    if group == 'admin':
        menu = ["Home", "View Courses", "View Course Selections"]
    else:
        menu = ["Home", "View Courses", "View Course Selections", "View Course Recommendation"]

    choice = st.sidebar.selectbox("Menu", menu)

    
    if choice == "Home":
        st.subheader("Home")
        st.write("Welcome to the Universty of WcDonald's.")

    elif choice == "View Courses":
        course_views.main(username)
    elif choice == "View Course Selections":
        course_selection.main(group,username)
    elif choice == "View Course Recommendation":
        course_recommendation.main(username)

def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["user_role"] = None

    placeholder = st.empty()

    if not st.session_state["logged_in"]:
        user_role = login.login_page()
        if user_role:
            st.session_state["logged_in"] = True
            st.session_state["user_role"] = user_role
            placeholder.empty()
            homepage(user_role)
        else:
            st.warning("Please log in to continue.")
    else:
        homepage(st.session_state["user_role"])
        
if __name__ == "__main__":
    main()

 