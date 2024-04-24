import csv
import numpy as np
from collections import defaultdict
import requests
import json
from glob import glob
from sentence_transformers import SentenceTransformer
from numpy.linalg import norm
import streamlit as st

prompt = "You are an ai study assistant in a school for providing help in course selection and study planning"
course_csv_path = "csv/course_list.csv"
selection_csv_path = "csv/course_selection.csv"
student_csv_path = "csv/student_info.csv"


def get_gpt_response(history, major):
    url = "https://oa.api2d.net/v1/chat/completions"

    messages = [{"role": "system", "content": prompt}]
    user_input = f"Hi! I am a student majored in {major}. I have taken the courses of {history}. Please recommend me five courses to take next!"
    messages.append({"role": "user", "content": user_input})

    payload = json.dumps(
        {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "safe_mode": False,
        }
    )
    headers = {
        "Authorization": "Bearer fk216155-ybzDrTKBFD4QDsLvTt07er4yNISFMdm3",
        "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response = json.loads(response.text)
    return response["choices"][0]["message"]["content"]


def find_closest_course(title):
    embeddings = defaultdict()

    root_path = "embedding"
    files = glob(root_path + "/*.npy")

    for file in files:
        uid = file.split("/")[-1].split("\\")[-1].split(".")[0]
        embeddings[uid] = np.load(file)

    model = SentenceTransformer("bert-base-nli-mean-tokens")
    sentence_embeddings = model.encode(title)
    max_similarity = 0
    result = None
    for key, embedding in embeddings.items():
        similarity = np.dot(embedding, sentence_embeddings) / (
            norm(embedding) * norm(sentence_embeddings)
        )
        if similarity > max_similarity:
            max_similarity = similarity
            result = key
    return result


def recommend(username):
    course_ID = defaultdict()
    student_history = defaultdict(list)
    student_major = defaultdict()

    with open(student_csv_path, "r", encoding="utf-8") as csvfile:
        students = list(csv.DictReader(csvfile))

    with open(selection_csv_path, "r", encoding="utf-8") as csvfile:
        selections = list(csv.DictReader(csvfile))

    with open(course_csv_path, "r", encoding="utf-8") as csvfile:
        courses = list(csv.DictReader(csvfile))

    for course in courses:
        course_ID[course["Subject"] + course["Number"]] = course["Name"]

    for student in students:
        student_history[student["student_id"]] = []
        student_major[student["student_id"]] = student["school"]

    for selection in selections:
        student_history[selection["student_id"]].append(
            course_ID[selection["course_subject"] + selection["course_number"]]
        )

    history = student_history[username]
    major = student_major[username]
    response_text = get_gpt_response(history, major)
    recommeded_courses = []

    for i in range(1, 6):
        recommeded_courses.append(response_text.split(f"\n\n{i}. ")[1].split(":")[0])

    recommendation_results = []

    for recommeded_course in recommeded_courses:
        recommendation_results.append(find_closest_course(recommeded_course))

    recommend_output = "Hello! Here are your recommended courses based on your selection history and major.\n"

    for i, line in enumerate(recommendation_results):
        recommend_output += (
            "\n"
            + line
            + ": "
            + response_text.split(f"\n\n{i + 1}. ")[1].split(":")[1].split("\n")[0]
            + "\n"
        )

    st.text_area("Recommended Courses", recommend_output, height=500)


def main(username):
    st.header("AI Courses Recommendation")
    recommend_button = st.button("Generate Courses Recommendation")
    if recommend_button:
        recommend(username)
