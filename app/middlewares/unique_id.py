# coding: utf8
from __future__ import annotations
from typing import TYPE_CHECKING
from aiogram.dispatcher.middlewares import BaseMiddleware

if TYPE_CHECKING:
    from app.typehint import TMessage
    from app.typehint import TDict
    from app.typehint import TAnyStr

__all__ = ["UniqueIdMiddleware"]


class UniqueIdMiddleware(BaseMiddleware):
    def __init__(self):
        super(UniqueIdMiddleware, self).__init__()

    async def on_process_message(self, message: TMessage, data: TDict):
        data['unique_id'] = self._make(message)

    @staticmethod
    def _make(message: TMessage) -> TAnyStr:
        return f'{message.chat.id}-{message.message_id}'
