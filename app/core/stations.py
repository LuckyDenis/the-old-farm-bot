# coding: utf8

from logging import getLogger
from app.core.depot import Train
from app.ui import interface as ui

logger = getLogger('app.core.station')


class BaseStation:
    @classmethod
    async def to_move(cls, train: Train):
        try:
            await cls._to_move(train)
        except RuntimeError as e:
            logger.error(cls.__class__, e)

    @classmethod
    async def _to_move(cls, train: Train):
        raise NotImplementedError()


class BeginSt(BaseStation):
    @classmethod
    async def _to_move(cls, train):
        pass


class FinishSt(BaseStation):
    @classmethod
    async def _to_move(cls, train):
        pass


class NewUserSt(BaseStation):
    @classmethod
    async def _to_move(cls, train):
        pass


class UINewUserSt(BaseStation):
    @classmethod
    async def _to_move(cls, train):
        answer_info = {
            'unique_id': train.unique_id,
            'locale': train.storage['user_info']['locale'],
            'chat_id': train.storage['user_info']['chat_id']
        }
        ui.NewUser.rendering(answer_info, train)
