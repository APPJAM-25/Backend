import asyncio
import os
from openai import OpenAI
from dotenv import load_dotenv

from sentiment import Sentiment


class GPT:
    """GPT 모시깽"""

    def __init__(self) -> None:
        load_dotenv()

        self.client = OpenAI()
        self.client.api_key = os.getenv("OPENAI_API_KEY")
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-3.5-turbo"
        self.tool = self.generate_tool()
        self.message_list = []

    def get_message_list(self) -> list:
        """대화내역 리턴"""
        return self.message_list

    def talk(self, propmt) -> str:
        """GPT와 채팅"""
        self.message_list.append({"role": "user", "content": propmt})

        completion_is_awkward = self.client.chat.completions.create(
            model=self.model,
            messages=self.message_list,
            tools=self.tool,
            tool_choice="auto",
        )

        completion_answer = self.client.chat.completions.create(
            model=self.model, messages=self.message_list
        )

        is_awkward = completion_is_awkward.choices[0].message.content is None
        answer = completion_answer.choices[0].message.content

        # GPT가 해당 문장이 어색하다고 판단했다면
        if is_awkward:
            pass

        self.message_list.append({"role": "system", "content": answer})
        return answer

    def generate_tool(self):
        """GPT가 문장이 문맥과 어색한지 판단하기 위한 기능을 하도록 만드는 함수를 제작"""
        tool = [
            {
                "type": "function",
                "function": {
                    "name": "is_not_awkward",
                    "description": "Check whether the entered string is consistent with the previous sentence",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "sentence": {
                                "type": "string",
                                "description": "Send sentences to check for awkwardness",
                            },
                        },
                        "required": ["sentence"],
                    },
                },
            }
        ]

        return tool
