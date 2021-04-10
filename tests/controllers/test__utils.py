# coding: utf8

import pytest
from app.controllers import sender
from app.core.train import Train
from app.ui.answer import AnswerWithText
from app.ui.keyboards import BaseKeyboard
from app.ui.answer import MessageType


class FakeBot:
    def __init__(self):
        self.send_msgs_done = []
        self.chat_ids = []

    async def send_message(self, chat_id=None, **kwargs):
        self.chat_ids.append(chat_id or kwargs.get('chat_id'))
        self.send_msgs_done.append(True)


@pytest.fixture()
def bot():
    return FakeBot()


CHAT_ID = 123456789
UNIQUE_ID = f'{CHAT_ID}-2'


@pytest.fixture()
def answer():
    answer = AnswerWithText(
        chat_id=CHAT_ID,
        unique_id=UNIQUE_ID,
        keyboard=BaseKeyboard.keyboard,
        text='foo1'
    )
    return answer


@pytest.fixture()
def train():
    train = Train(
        unique_id=UNIQUE_ID,
        chat_id=CHAT_ID,
        destination='test',
        storage={'FOO': 'foo'}
    )
    return train


@pytest.mark.unit
class TestUnit:
    async def test__message_with_critical_error(self, train, bot):
        await sender.message_with_critical_error(
            bot, train
        )
        assert filter(
            lambda chat_id: chat_id == CHAT_ID,
            bot.chat_ids)
        assert all(bot.send_msgs_done)
        assert len(bot.send_msgs_done) == 1
        assert len(bot.chat_ids) == 1

    async def test__message_with_text(self, bot, answer):
        await sender.message_with_text(bot, answer)

        assert len(bot.chat_ids) == 1
        assert bot.chat_ids[-1] == answer.chat_id

    @pytest.mark.parametrize(
        ('message_type', 'handler'),
        (
            (MessageType.TEXT, sender.message_with_text),
        )
    )
    def test__search_send_handler(self, message_type, handler):
        assert sender.search_send_handler(message_type) is handler

    async def test__send_messages_correct(
            self, monkeypatch, bot, train, answer):
        is_call_func = [False]

        async def message_with_text(*args, **kwargs):
            is_call_func[0] = True
            b = args[0] or kwargs['bot']
            a = args[1] or kwargs['answer']
            await b.send_message(
                chat_id=a.chat_id
            )
        monkeypatch.setattr(
            sender, 'message_with_text',
            message_with_text
        )

        train.answers += [answer, answer]
        await sender.send_messages(bot, train)

        assert len(bot.chat_ids) == 2

    async def test__send_messages_train_has_fail(
            self, monkeypatch, bot, train):
        is_call_func = [False]

        async def message_with_critical_error(*_, **__):
            is_call_func[0] = True

        monkeypatch.setattr(
            sender, 'message_with_critical_error',
            message_with_critical_error
        )

        train.has_fail = True
        await sender.send_messages(bot, train)

        assert is_call_func[0] is True

    async def test__send_messages_fail(
            self, monkeypatch, bot, train, answer):
        is_call_func = [False]

        async def message_with_critical_error(*_, **__):
            is_call_func[0] = True

        monkeypatch.setattr(
            sender, 'message_with_critical_error',
            message_with_critical_error
        )

        async def message_with_text(*_, **__):
            raise TypeError()

        monkeypatch.setattr(
            sender, 'message_with_text',
            message_with_text
        )

        train.answers += [answer, answer]
        await sender.send_messages(bot, train)

        assert is_call_func[0] is True
