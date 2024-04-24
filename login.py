import streamlit as st
import time
import base64

def login(placeholder):
    with placeholder.container():
        cols1, cols2, cols3 = st.columns(3)
        with cols2.container():
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.header("Login")
            username = st.text_input("username", key="username")
            password = st.text_input("password", type="password", key="userpassword")
            login_button = st.button("Login")
            if login_button:
                image = st.image("loading.gif")
                time.sleep(2) #遥遥领先同行
                if username == "admin" and password == "password":
                    st.success("Login success!")
                    st.session_state["page"] = 1
                    placeholder.empty()
                    return
                elif username == "1200000" and password == "cuhksz":
                    st.success("Login success!")
                    st.session_state["page"] = int(username)
                    placeholder.empty()
                    return
                else:
                    st.error("wrong username or password")
                    image.empty()
                    
            

def set_bg_hack(main_bg):
    main_bg_ext = "png"
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover;
         }}
         .css-1asfiv1 {{  /* Targets header within Streamlit app */
             color: black;
         }}
         .css-12b3osv {{  /* Targets input fields within Streamlit app */
             color: black;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )


def login_page():
    global username
    if "page" not in st.session_state:
        st.session_state["page"] = 0
    
    placeholder = st.empty()

    if st.session_state["page"] == 0:    
        set_bg_hack("login_background.png")
        username = login(placeholder)
        
    if st.session_state["page"] == 1:
        return "admin"
    elif st.session_state['page'] != 0:
        return "user"