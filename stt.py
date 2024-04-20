from openai import OpenAI
from dotenv import load_dotenv


class STT:
    def __init__(self) -> None:
        load_dotenv()
        self._client = OpenAI()

    def __call__(self, audioPath: str) -> str:
        with open(audioPath, "rb") as f:
            return self._client.audio.transcriptions.create(
                file=f,
                model="whisper-1",
            ).text


if __name__ == "__main__":
    stt = STT()
    text = stt("test.wav")
    print(text)
