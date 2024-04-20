import os
from openai import OpenAI
from dotenv import load_dotenv

from type import PersonaInfo
from redisconn import Redis


class GPT:
    """GPT 모시깽"""

    def __init__(self, chatId, data) -> None:
        load_dotenv()

        self.chatId = chatId
        self.data = data
        self.client = OpenAI()
        self.client.api_key = os.getenv("OPENAI_API_KEY")
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-3.5-turbo"
        self.tool = self.generate_tool()
        self.message_list = []
        self.rd = Redis()

    def get_persona_data(self):
        """ 유저 데이터 리턴 """
        return self.data.persona

    def create_persona(self) -> None:
        """페르소나 생성"""
        prompt = f"""
        You are {self.data.persona.gender} with an age between {self.data.persona.ageMin} and {self.data.persona.ageMax} years.
        you live in a region of Korea and has an MBTI of {self.data.persona.mbti}.
        The relationship is currently in a {self.data.persona.relationship} state and you are currently in {self.data.persona.romanticStatus}.
        you use {'polite language to me' if self.data.persona.polite else 'informal language to me'}.
        The area you live in, education level, and occupation must be set, and the your characteristics, name, personality, behavior patterns, and interests must be set in detail and have a conversation with me.
        그리고 넌 한국어로 대답해야 해.
        """
        self.message_list.append({"role": "system", "content": prompt})

    def get_message_list(self) -> list:
        """대화내역 리턴"""
        return self.message_list

    def talk(self, prompt) -> str:
        """GPT와 채팅"""
        self.message_list.append({"role": "user", "content": prompt})

        self.client.chat.completions.create(
            model=self.model,
            messages=self.message_list,
            tools=self.tool,
            tool_choice="auto",
        )

        # GPT가 해당 문장이 어색하다고 판단했다면
        # if completion_is_awkward.choices[0].message.content is None:
        #     pass

        completion_answer = self.client.chat.completions.create(
            model=self.model, messages=self.message_list, temperature=0.5
        )

        answer = completion_answer.choices[0].message.content

        self.message_list.append({"role": "assistant", "content": answer})
        # print(self.message_list)
        return answer

    def generate_tool(self):
        """GPT가 문장이 문맥과 어색한지 판단하기 위한 기능을 하도록 만드는 함수를 제작"""
        tool = [
            {
                "type": "function",
                "function": {
                    "name": "is_not_awkward",
                    "description": "Verify that the string you entered matches the previous sentence.",
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

    def get_analyze(self):
        """ 통계 내기 """
        # messages = [
        #     {"role": "system", "content": """
        #         You are women with an age between 17 and 19 years.
        #         you live in a region of Korea and has an MBTI of ENFP.
        #         The relationship is currently in a Friend state and you are currently in Lover.
        #         you use informal language to me.
        #         The area you live in, education level, and occupation must be set, and the your characteristics, name, personality, behavior patterns, and interests must be set in detail and have a conversation with me.
        #         그리고 넌 한국어로 대답해야 해.
        #     """},
        #     {"role": "user", "content": "안녕?"},
        #     {"role": "assistant", "content": "안녕"},
        #     {"role": "user", "content": "오늘 점심은 뭐 먹었어?"},
        #     {"role": "assistant", "content": "나는 오늘 삼겹살 먹었어. 너는?"},
        #     {"role": "user", "content": "맛있었겠네"},
        # ]

        request_messages = []

        for i in self.message_list:
            role = i.get("role")
            type = ""
            
            if role == "system":
                continue
            elif role =='user':
                type = "자신 : "
            elif role == 'assistant':
                type = "상대 : "

            request_messages.append(type + i.get("content") + "\n")

        request_messages.append("\n\n Analyze the above conversations and give a score on whether the context of the conversation was natural, whether you empathized well with what the other person said, whether you used a variety of vocabulary, whether the conversation continued, and whether the conversation was interesting. Please display it in the form of “title”: “score” with additional explanation. The title of each item should be 'Naturalness', 'Empathy', 'Variety of vocabulary', 'Continuation', 'Interestingness' and expressed as a score out of 100. 100 is the high score and 1 is the low score. Diverse vocabulary should be reduced by using abbreviations, slang, and new words. Please analyze it in more detailed numbers.")
        
        result = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role" : "user", "content" : str(request_messages)}],
            temperature=0.3
        )

        return result.choices[0].message.content