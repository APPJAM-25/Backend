from pydantic import BaseModel


class Image(BaseModel):
    age: int
    gender: str
    mbti: str
