import os
import os.path as osp

import uuid
from dto import ChatStartDto
from fastapi import FastAPI, UploadFile

app = FastAPI()
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
    filePath = osp.join(rootPath, "tmp", f"{chatId}.m4a")
    with open(filePath, "wb") as f:
        f.write(file.file.read())

    return {"chatId": chatId}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
