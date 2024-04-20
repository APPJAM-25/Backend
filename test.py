import requests
from logic import GPT

with open("test.wav", "rb") as f:
    result = requests.post(
        "http://localhost:3000/chat/asdf",
        files={"file": f},
    )

    print(result.json())

    gpt = GPT()
    print(gpt.talk(result.json()['text']))
