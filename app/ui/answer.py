# coding: utf8

from dataclasses import dataclass, field
from enum import Enum, unique, auto
from app.ui.keyboards import BaseKeyboard


@unique
class MessageType(Enum):
    TEXT = auto()


@dataclass
class BaseAnswer:
    chat_id: int
    unique_id: str
    keyboard: BaseKeyboard
    message_type: auto() = field(init=False)


@dataclass
class AnswerWithText(BaseAnswer):
    text: str

    def __post_init__(self):
        self.message_type = MessageType.TEXT
