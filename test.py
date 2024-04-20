import requests

with open("1.m4a", "rb") as f:
    requests.post("http://localhost:8000/chat/asdf", files={"file": f})
