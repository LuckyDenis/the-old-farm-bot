# coding: utf8

import pytest
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import ReplyKeyboardMarkup
from app.ui import keyboards as k7s


@pytest.mark.unit
class TestBaseKeyboard:
    def test__keyboard(self):
        with pytest.raises(NotImplementedError):
            k7s.BaseKeyboard.keyboard()


@pytest.mark.unit
class TestKeyboards:
    @pytest.mark.parametrize(
        ('keyboard', 'type_keyboard'),
        (
            (k7s.Remove.keyboard, ReplyKeyboardRemove),
            (k7s.SystemException.keyboard, ReplyKeyboardMarkup),
            (k7s.NewUser.keyboard, ReplyKeyboardMarkup)
        )
    )
    def test__keyboard(self, keyboard, type_keyboard):
        isinstance(keyboard(), type_keyboard)
