# coding: utf8
from __future__ import annotations
from typing import TYPE_CHECKING

from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import ReplyKeyboardRemove

from app.ui.i18n import I18N
from app.ui.commands import Commands


if TYPE_CHECKING:
    from app.typehint import TKeyboard


i18n = I18N()
_ = i18n.gettext_lazy


class BaseKeyboard:
    @classmethod
    def keyboard(cls) -> TKeyboard:
        raise NotImplementedError()


class Remove(BaseKeyboard):
    @classmethod
    def keyboard(cls) -> TKeyboard:
        return ReplyKeyboardRemove()


class SystemException(BaseKeyboard):
    @classmethod
    def keyboard(cls) -> TKeyboard:
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=False
        ).row(
            KeyboardButton(_("{i_bug} Bug").format(
                i_bug=Commands.Bug.ui
            ))
        )


# ----------- cmd: start ---------- #
class NewUser(BaseKeyboard):
    @classmethod
    def keyboard(cls) -> TKeyboard:
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=False
        ).row(
            KeyboardButton(_("{i_accept} Accept").format(
                i_accept='/accept')),
            KeyboardButton(_("{i_not_accept} Not accept").format(
                i_not_accept='/reject'
            ))
        )
