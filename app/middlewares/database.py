# coding: utf8
from aiogram.dispatcher.middlewares import BaseMiddleware

__all__ = ["DBMiddleware"]


class DBMiddleware(BaseMiddleware):
    def __init__(self, connect=None):
        self.connect = connect

        super(DBMiddleware, self).__init__()

    async def on_process_message(self, _, data: dict):
        data['db'] = await self.connect.get()
