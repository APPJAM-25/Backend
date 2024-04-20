from pydantic import BaseModel
from type import *


class ChatStartDto(BaseModel):
    a: Info
    b: Info
