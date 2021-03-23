# coding: utf8

from contextvars import ContextVar
from dataclasses import dataclass

from aiogram.types import Message
from aiogram.bot.bot import Bot

from app.configure.file_reader import BaseFileReader
from app.configure.reader import ConfigReader
from app.core.stations import BaseStation
from app.core.train import Train
from app.ui.answer import AnswerWithText
from app.ui.answer import BaseAnswer
from app.ui.i18n import I18N
from app.ui.keyboards import BaseKeyboard
from typing import Type, List, Union

TDict = dict
TInt = int
TAnyStr = str
TList = list
TBool = bool

TEnumAuto = object
TOptionAnyStr = (str, None)
TDataClass = type(dataclass)
TContextVar = ContextVar

TMessage = Message
TBot = Bot

TFileReader = BaseFileReader
TConfigReader = ConfigReader


TI18N = I18N
TAnswer = BaseAnswer
TAnswerWithText = AnswerWithText
TKeyboard = BaseKeyboard.keyboard

TTrain = Train
TVisited = List[TAnyStr]
TAnswers = List[Union[BaseAnswer, AnswerWithText]]

TStation = BaseStation
TStations = List[Type[TStation]]


__all__ = [
    TTrain,
    TAnswerWithText,
    TFileReader,
    TConfigReader,
    TDict,
    TInt,
    TAnyStr,
    TOptionAnyStr,
    TBool,
    TDataClass,
    TStation,
    TStations,
    TMessage,
    TAnswers,
    TAnswer,
    TVisited,
    TEnumAuto,
    TContextVar,
    TI18N,
    TKeyboard
]
