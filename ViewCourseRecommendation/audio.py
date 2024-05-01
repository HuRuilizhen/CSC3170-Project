import requests
import soundfile
import numpy as np
import json


def generate_audio(texts, file_name):
    MY_URL = "http://10.26.1.178:11451/predict"

    # texts = [
    #     "Hello! Here are your recommended courses based on your selection history and major.",
    #     "CHLH260,  This course will provide you with a strong foundation in ethical principles and legal considerations related to the field of medicine.",
    #     "BSE601,  Deepen your understanding of the human body's structure and function through this foundational course in anatomy and physiology.",
    #     "BSE703,  Further explore the study of drugs and their effects on the body, an essential concept for any student pursuing a career in medicine.",
    #     "EPOL597,  Improve your ability to effectively communicate with patients and colleagues while honing your clinical skills in a practical setting.",
    #     "PATH494,  Dive into the study of the functional changes that accompany disease processes, enhancing your understanding of the mechanisms underlying various medical conditions."
    # ]

    # can't handle ':' situation
    full_audio = np.array([])

    for text in texts:
        data = {"text": text}

        r = requests.post(url=MY_URL, json={"data": data})
        response = json.loads(r.content)
        audio = np.array(response)

        silent_audio = np.zeros(16000)
        full_audio = np.concatenate((full_audio, audio, silent_audio))

    soundfile.write(f"./{file_name}.wav", full_audio, 16000)

    return True
