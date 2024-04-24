import streamlit as st
import pymysql
import pandas as pd


def get_db_connection():
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='123456',
                                     db='c3170',
                                     charset='utf8mb4',   
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection
    except pymysql.MySQLError as e:
        error_code, error_message = e.args
        st.error(f"Error connecting to the MySQL Database: {error_code}, {error_message}")
        # You might want to log the detailed error message in a log file for further investigation
        return None


def load_data(query):
    try:
        conn = get_db_connection()
        if conn is None or not hasattr(conn, 'cursor'):
            st.error("Database connection is not established correctly.")
            return pd.DataFrame()
        
        # Now that we've checked for a cursor attribute, let's use it
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()  # Fetch all the results
            columns = [col[0] for col in cursor.description]  # Get the column names
            data = pd.DataFrame(result, columns=columns)
        conn.close()
        return data
    except Exception as e:
        st.error(f"An error occurred while fetching data: {e}")
        return pd.DataFrame()

def insert_data(query):
    try:
        conn = get_db_connection()
        if conn is None or not hasattr(conn, 'cursor'):
            st.error("Database connection is not established correctly.")
            return pd.DataFrame()
        
        cursor = conn.cursor()
        cursor.execute(query)
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"An error occurred while fetching data: {e}")
        return False
