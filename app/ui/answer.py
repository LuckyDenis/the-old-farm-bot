# coding: utf8

from dataclasses import dataclass
from enum import Enum, auto, unique
from app.ui.keyboards import BaseKeyboard


@unique
class MessageType(Enum):
    TEXT = auto()


@dataclass()
class BaseAnswer:
    chat_id: int
    message_type: MessageType
    unique_id: str
    keyboard: BaseKeyboard


@dataclass()
class AnswerWithText(BaseAnswer):
    text: MessageType.TEXT
