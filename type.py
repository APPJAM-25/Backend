from pydantic import BaseModel


class Info(BaseModel):
    age: int
    gender: str
    mbti: str
