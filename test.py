import json
import requests

import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100  # Sample rate
seconds = 5  # Duration of recording


body_data = {
    "user": {"name": "수민", "age": 25, "gender": "man"},
    "persona": {
        "ageMin": 20,  # 나이 최소
        "ageMax": 30,  # 나이 최대
        "gender": "man",  # 성별 (man, woman)
        "mbti": "ISTP",  # MBTI
        "relationship": "친구",  # 관계
        "romanticStatus": "썸",  # 연애 상태
        "polite": False,  # 존댓말 여부
    },
}

response = requests.post(
    "http://localhost/chat/start", data=json.dumps(body_data), timeout=15
)
chat_id = response.json()["chatId"]

# response = requests.get(f"http://localhost:3000/chat/data/{chat_id}", timeout=15)
# print(response.json())
# response = requests.post(f"http://localhost:3000/chat/{chat_id}", timeout=30)


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
            f"http://localhost/chat/{chat_id}", files={"file": f}, timeout=30
        )

        with open("output.mp3", "wb") as f:
            f.write(result.content)

result = requests.post(
    "http://localhost/chat/end/12313", data=json.dumps(body_data), timeout=30
)
print(result.json())
