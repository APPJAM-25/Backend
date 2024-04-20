import json
import requests
from logic import GPT


body_data = {
    "user": {
        "name": "Hong gildong",
        "age": 19,
        "gender": 'Men'
    },
    "persona": {
        "ageMin": 17,  # 나이 최소
        "ageMax": 19,  # 나이 최대
        "gender": "women",  # 성별 (men, women)
        "mbti": "ENFP",  # MBTI
        "relationship": "friend",  # 관계
        "romanticStatus": "friend",  # 연애 상태
        "polite": False  # 존댓말 여부
    }
}

response = requests.post(
    "http://localhost:3000/chat/start",
    data=json.dumps(body_data),
    timeout=15
)
chat_id = response.json()['chatId']

with open("test.wav", "rb") as f:
    result = requests.post(
        f"http://localhost:3000/chat/{chat_id}",
        files={"file": f},
        timeout=30
    )

    print(result.json())

    gpt = GPT()
    print(gpt.talk(result.json()['text']))
