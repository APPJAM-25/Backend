import os
import os.path as osp

import uuid
from fastapi import FastAPI, UploadFile

from stt import STT
from sentiment import Sentiment
from dto import ChatStartDto

from redisconn import redisConfig

app = FastAPI()
stt = STT()
sentiment = Sentiment()

rd = redisConfig()

rootPath = osp.dirname(osp.abspath(__file__))

if osp.exists(osp.join(rootPath, "tmp")) is False:
    os.mkdir(osp.join(rootPath, "tmp"))


@app.get("/")
async def root():
    return {"message": "root"}


@app.post("/chat/start")
async def chatStart(data: ChatStartDto):
    chatId = uuid.uuid4()

    return {"chatId": chatId}


@app.post("/chat/{chatId}/")
async def chat(chatId: str, file: UploadFile):
    filePath = osp.join(rootPath, "tmp", f"{chatId}.wav")
    with open(filePath, "wb") as f:
        f.write(file.file.read())

    text = stt(filePath)
    sentimentResult = sentiment(text)
    sentimentText = sentimentResult[0][0]["label"]

    rd.rpush(f"sentiment:{chatId}", sentimentText)

    return {"chatId": chatId, "text": text}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
