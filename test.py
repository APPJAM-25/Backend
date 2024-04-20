import json
import requests

import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100  # Sample rate
seconds = 3  # Duration of recording


body_data = {
    "user": {"name": "Hong gildong", "age": 19, "gender": "Men"},
    "persona": {
        "ageMin": 17,  # 나이 최소
        "ageMax": 19,  # 나이 최대
        "gender": "woman",  # 성별 (man, woman)
        "mbti": "ENFP",  # MBTI
        "relationship": "friend",  # 관계
        "romanticStatus": "friend",  # 연애 상태
        "polite": False,  # 존댓말 여부
    },
}

response = requests.post(
    "http://localhost:3000/chat/start", data=json.dumps(body_data), timeout=15
)
chat_id = response.json()["chatId"]

while 1:
    print("recoding...")
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()
    write("output.wav", fs, recording)
    print("recoding end")

    if (input("send? (y/n): ") or "n") == "n":
        continue

    with open("output.wav", "rb") as f:
        result = requests.post(
            f"http://localhost:3000/chat/{chat_id}", files={"file": f}, timeout=30
        )

        with open("output.mp3", "wb") as f:
            f.write(result.content)

result = requests.post("http://localhost:3000/chat/end/12313", timeout=30)
print(result.json())
