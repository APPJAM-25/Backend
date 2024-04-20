import os
import os.path as osp

import uuid
from fastapi import FastAPI, UploadFile

from logic import GPT
from stt import STT
from dto import ChatStartDto

app = FastAPI()
stt = STT()
gpt = GPT()

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
    """ 채팅을 비동기 처리 """
    filePath = osp.join(rootPath, "tmp", f"{chatId}.wav")
    with open(filePath, "wb") as f:
        f.write(file.file.read())

    text = stt(filePath)
    gpt.talk(text)

    return {"chatId": chatId, "text": text}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
