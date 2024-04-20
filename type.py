from pydantic import BaseModel


class UserInfo(BaseModel):
    name: str
    age: int
    gender: str  # (man, woman)


class PersonaInfo(BaseModel):
    name: str | None
    ageMin: int  # 나이 최소
    ageMax: int  # 나이 최대
    gender: str  # 성별 (man, woman)
    mbti: str  # MBTI
    relationship: str  # 관계
    romanticStatus: str  # 연애 상태
    polite: bool  # 존댓말 여부
