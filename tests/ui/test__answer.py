# coding: utf8

import pytest
from app.ui.answer import MessageType
from app.ui.answer import AnswerWithText
from app.ui.keyboards import BaseKeyboard


# user_id, chat_id = 2^64
# https://core.telegram.org/bots/api
CHAT_ID = 18446744073709551616
UNIQUE_ID = '18446744073709551616 - 2'
TEXT = 'text'


@pytest.mark.unit
class TestAnswerWithText:
    def test__fields(self):
        answer_with_text = AnswerWithText(
            chat_id=CHAT_ID,
            unique_id=UNIQUE_ID,
            keyboard=BaseKeyboard.keyboard,
            text=TEXT
        )
        assert answer_with_text.message_type == MessageType.TEXT


@pytest.mark.unit
class TestMessageType:
    @pytest.mark.parametrize(
        'attr',
        (
            'TEXT',
        )
    )
    def test__has_attr(self, attr):
        assert hasattr(MessageType, attr)
