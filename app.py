import json
import math
import os
import os.path as osp

import random
import uuid
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse

from logic import GPT
from stt import STT
from tts import TTS
from sentiment import Sentiment
from dto import ChatStartDto

from redisconn import Redis

app = FastAPI()
stt = STT()
tts = TTS()
sentiment = Sentiment()

rd = Redis()
gptObjects = {}

rootPath = osp.dirname(osp.abspath(__file__))

if osp.exists(osp.join(rootPath, "tmp")) is False:
    os.mkdir(osp.join(rootPath, "tmp"))


@app.get("/")
async def root():
    return {"message": "root"}


@app.get("/chat/data/{chatId}")
def get_data(chatId: str):
    gpt = gptObjects[chatId]
    persona_data = gpt.get_persona_data().__dict__

    age = int(persona_data['ageMin'])
    gender = persona_data['gender'].lower()
    number = random.randint(1, 5)

    if age >= 15:
        age = 10
    elif age >= 20 and age < 30:
        age = 20
    elif age >= 30 and age < 40:
        age = 30
    elif age >= 40:
        age = 40

    return [persona_data ,f"{age}{gender}{number}.jpg"]

@app.post("/chat/start")
async def chatStart(data: ChatStartDto):
    chatId = str(uuid.uuid4())

    gptObjects[chatId] = GPT(chatId, data)
    gpt = gptObjects[chatId]

    gpt.create_persona()

    return {"chatId": chatId}


@app.post("/chat/{chatId}/")
async def chat(chatId: str, file: UploadFile):
    """채팅을 비동기 처리"""
    filePath = osp.join(rootPath, "tmp", f"{chatId}.wav")
    with open(filePath, "wb") as f:
        f.write(file.file.read())

    text = stt(filePath)
    sentimentResult = await sentiment(text)
    sentimentText = sentimentResult[0][0]["label"]

    rd().rpush(f"sentiment:{chatId}", sentimentText)

    gpt = gptObjects[chatId]
    answer = gpt.talk(text)
    gender = gpt.data.gender

    tts(chatId, gender, answer)

    return FileResponse(osp.join(rootPath, "tmp", f"{chatId}.mp3"))


@app.post("/chat/end/{chatId}")
def chatEnd(chatId: str):
    """
    채팅을 끝내고 통계를 반환
    """
    gpt = gptObjects[chatId]
    result = gpt.get_analyze()
    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3000)
