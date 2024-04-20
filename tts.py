import os.path as osp
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
rootPath = osp.dirname(osp.abspath(__file__))


class TTS:
    def __init__(self) -> None:
        load_dotenv()

        self._client = OpenAI()

    def __call__(self, chatId, gender, input):
        if gender != "man":  # 반대
            voice = "onyx"
        else:
            voice = "nova"

        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,  # 여자 nova, 남자 onyx
            input=input,
            speed=1.1,
        )

        response.stream_to_file(osp.join(rootPath, "tmp", f"{chatId}.mp3"))

        return
