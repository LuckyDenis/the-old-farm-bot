# coding: utf8

from dataclasses import dataclass
from enum import Enum, auto, unique
from typing import Union, AnyStr

from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import ReplyKeyboardRemove


@unique
class MessageType(Enum):
    TEXT = auto()


@dataclass()
class BaseAnswer:
    chat_id: int
    message_type: MessageType
    unique_id: AnyStr
    keyboard: Union[ReplyKeyboardRemove, ReplyKeyboardMarkup]


@dataclass()
class AnswerWithText(BaseAnswer):
    text: MessageType.TEXT
