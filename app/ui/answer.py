# coding: utf8
from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass, field
from enum import Enum, unique, auto


if TYPE_CHECKING:
    from app.typehint import TEnumAuto
    from app.typehint import TInt
    from app.typehint import TAnyStr
    from app.typehint import TKeyboard


@unique
class MessageType(Enum):
    TEXT: TEnumAuto = auto()


@dataclass
class BaseAnswer:
    chat_id: TInt
    unique_id: TAnyStr
    keyboard: TKeyboard
    message_type: TEnumAuto = field(init=False)


@dataclass
class AnswerWithText(BaseAnswer):
    text: TAnyStr

    def __post_init__(self):
        self.message_type: TEnumAuto = MessageType.TEXT
