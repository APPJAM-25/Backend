from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "root"})


@app.route("/chat/start")
def chatStart():
    # chat start
    return


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
