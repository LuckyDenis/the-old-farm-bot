# coding: utf8

from contextvars import ContextVar
from dataclasses import dataclass
from typing import Type, List, Union

from aiogram.bot.bot import Bot
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import ReplyKeyboardMarkup

from app.configure.file_reader import BaseFileReader
from app.configure.reader import ConfigReader
from app.core.stations import BaseStation
from app.core.train import Train
from app.ui.answer import AnswerWithText
from app.ui.answer import BaseAnswer
from app.ui.i18n import I18N
from app.database.connecter import DBConnect


TDict = dict
TInt = int
TAnyStr = str
TList = list
TBool = bool

TEnumAuto = object
TDataClass = type(dataclass)
TContextVar = ContextVar

TMessage = Message
TBot = Bot
TKeyboard = (ReplyKeyboardMarkup, ReplyKeyboardRemove)

TFileReader = BaseFileReader
TConfigReader = ConfigReader


TI18N = I18N
TAnswer = BaseAnswer
TAnswerWithText = AnswerWithText

TTrain = Train
TVisited = List[TAnyStr]
TAnswers = List[Union[BaseAnswer, AnswerWithText]]

TStation = BaseStation
TStations = List[Type[TStation]]


TDBConnect = DBConnect


__all__ = [
    'TTrain',
    'TAnswerWithText',
    'TFileReader',
    'TConfigReader',
    'TDict',
    'TInt',
    'TAnyStr',
    'TBool',
    'TDataClass',
    'TDBConnect',
    'TStation',
    'TStations',
    'TMessage',
    'TAnswers',
    'TAnswer',
    'TVisited',
    'TEnumAuto',
    'TContextVar',
    'TI18N',
    'TKeyboard'
]
