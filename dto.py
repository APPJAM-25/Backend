from pydantic import BaseModel
from type import *


class ChatStartDto(BaseModel):
    user: UserInfo
    persona: PersonaInfo
