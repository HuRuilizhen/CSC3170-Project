import numpy as np
from collections import defaultdict
import requests
import json
from glob import glob
from sentence_transformers import SentenceTransformer
from numpy.linalg import norm
import streamlit as st
import ViewCourseRecommendation.audio as audio
import CommonLogic.db as db

prompt = "You are an ai study assistant in a school for providing help in course selection and study planning"


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

    root_path = "/static/embedding"
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

    student_query = "SELECT * FROM student_info"
    students = db.load_data(student_query)

    selection_query = "SELECT * FROM course_selection"
    selections = db.load_data(selection_query)

    course_query = "SELECT * FROM course_list"
    courses = db.load_data(course_query)

    for index, row in courses.iterrows():
        course_ID[row["subject"] + str(row["number"])] = row["name"]

    for index, row in students.iterrows():
        student_history[str(row["student_id"])] = []
        student_major[str(row["student_id"])] = row["school"]

    for index, row in selections.iterrows():
        student_history[str(row["student_id"])].append(
            course_ID[row["course_subject"] + str(row["course_number"])]
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

    recommend_output = recommend_output.replace(":", ",")
    texts = recommend_output.split(".\n")
    texts = [sentence.strip() for sentence in texts if sentence.strip()]
    return texts


def main(username):
    st.header("AI Courses Recommendation")
    recommend_button = st.button("Generate Courses Recommendation")
    if recommend_button:
        texts = recommend(username)

        audio_name = "recommand"
        if audio.generate_audio(texts, f"{audio_name}_audio") is True:
            audio_file = open(f"{audio_name}_audio.wav", "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/wav")
