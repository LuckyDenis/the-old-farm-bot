# coding: utf8


import pytest
from app.middlewares.unique_id import UniqueIdMiddleware
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types.message import Message, Chat


MESSAGE_ID = 123456789
CHAT_ID = 424242
DATA_UNIQUE_ID_KEY = 'unique_id'

message = Message()
message.message_id = MESSAGE_ID
message.chat = Chat
message.chat.id = CHAT_ID

TEMPLATE_UNIQUE_ID = f'{message.chat.id}-{message.message_id}'


@pytest.mark.unit
class TestUniqueId:
    def test__unique_id_cls_is_sub_base_middleware(self):
        mid_unique_id = UniqueIdMiddleware()
        assert isinstance(mid_unique_id, BaseMiddleware)

    def test__make_unique_id(self):
        mid_unique_id = UniqueIdMiddleware()
        unique_id = mid_unique_id.make(message)
        assert unique_id == TEMPLATE_UNIQUE_ID

    async def test__on_process_message(self):
        mid_unique_id = UniqueIdMiddleware()
        data = dict()
        await mid_unique_id.on_process_message(
            message, data
        )
        assert data[DATA_UNIQUE_ID_KEY] == TEMPLATE_UNIQUE_ID
