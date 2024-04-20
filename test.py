import requests

with open("test.wav", "rb") as f:
    result = requests.post(
        "http://localhost:8000/chat/asdf",
        files={"file": f},
        # headers={"Content-Type": "audio/wav"},
    )

    print(result.json())
