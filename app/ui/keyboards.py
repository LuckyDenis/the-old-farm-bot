# coding: utf8

from dataclasses import dataclass

from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import ReplyKeyboardRemove

from app.ui.i18n import I18N
from app.ui.commands import Commands


i18n = I18N()
_ = i18n.gettext_lazy


@dataclass()
class BaseKeyboard:
    keyboard: (ReplyKeyboardRemove, ReplyKeyboardMarkup)


class Remove(BaseKeyboard):
    keyboard = ReplyKeyboardRemove()


class SystemException(BaseKeyboard):
    keyboard = ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=False
        ).row(
            KeyboardButton(_("{i_bug} Bug").format(
                i_bug=Commands.Bug.ui
            ))
        )


# ----------- cmd: start ---------- #
class NewUser(BaseKeyboard):
    keyboard = ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=False
        ).row(
            KeyboardButton(_("{i_accept} Accept").format(
                i_accept='/accept')),
            KeyboardButton(_("{i_not_accept} Not accept").format(
                i_not_accept='/reject'
            ))
        )
