import streamlit as st
import LoginSystem.login as login
import CommonLogic.config as config
import ViewCourse.course_views as course_views
import CommonLogic.db as db
import ViewCourseSelection.course_selection as course_selection
import ViewCourseRecommendation.course_recommendation as course_recommendation


def homepage(group):

    st.title("WcDonald's")
    config.set_bg("static/images/background.jpg")
    db.get_db_connection()

    username = str(st.session_state["page"])
    if group == "admin":
        menu = ["Home", "View Courses", "View Course Selections"]
    else:
        menu = [
            "Home",
            "View Courses",
            "View Course Selections",
            "View Course Recommendation",
        ]

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        welcome_text = "Welcome to the Universty of WcDonald's."
        st.write(welcome_text)
        audio_file = open("static/sounds/welcome.wav", "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/wav")
    elif choice == "View Courses":
        course_views.main(username)
    elif choice == "View Course Selections":
        course_selection.main(group, username)
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
