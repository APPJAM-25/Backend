import os
import os.path as osp

import uuid
from dto import ChatStartDto
from flask import Flask, request, jsonify

app = Flask(__name__)
rootPath = osp.dirname(osp.abspath(__file__))


@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "root"})


@app.route("/chat/start", methods=["POST"])
def chatStart():
    data = request.get_json()
    data = ChatStartDto(data)
    chatId = uuid.uuid4()

    return jsonify({"chatId": chatId})


@app.route("/chat/<string:chatId>", methods=["POST"])
def chat():
    chatId = uuid.UUID(request.headers.get("chatId"))
    osp.join(rootPath, f"{chatId}.m4a")
    # osp.join(rootPath, "chat", f"{chatId}.m4a")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
