import requests

with open("test.wav", "rb") as f:
    result = requests.post(
        "http://localhost:3000/chat/asdf",
        files={"file": f},
    )

    print(result.json())
