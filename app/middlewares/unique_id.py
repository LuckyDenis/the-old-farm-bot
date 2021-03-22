# coding: utf8

from aiogram import types as t
from aiogram.dispatcher.middlewares import BaseMiddleware


__all__ = ["UniqueIdMiddleware"]


class UniqueIdMiddleware(BaseMiddleware):
    def __init__(self):
        super(UniqueIdMiddleware, self).__init__()

    async def on_process_message(self, message: t.Message, data):
        data['unique_id'] = self.make(message)

    @staticmethod
    def make(message: t.Message):
        return f'{message.chat.id}-{message.message_id}'
