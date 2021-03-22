# coding: utf8

from logging import getLogger
from app.ui import interface as ui

logger = getLogger('app.core.station')


class BaseStation:
    @classmethod
    async def stopover(cls, train):
        try:
            await cls._stopover(train)
        except (KeyError, ValueError) as e:
            logger.error(f'error: {e}, cls: {cls}, train: {train}')

    @classmethod
    async def _stopover(cls, train):
        raise NotImplementedError()


class BeginSt(BaseStation):
    @classmethod
    async def _stopover(cls, train):
        pass


class FinishSt(BaseStation):
    @classmethod
    async def _stopover(cls, train):
        pass


class NewUserSt(BaseStation):
    @classmethod
    async def _stopover(cls, train):
        pass


class UISystemExceptionSt(BaseStation):
    @classmethod
    async def _stopover(cls, train):
        answer_info = {
            'unique_id': train.unique_id,
            'locale': train.storage['user_info']['locale'],
            'chat_id': train.storage['user_info']['chat_id']
        }
        ui.SystemException.generate(answer_info, train)


class UINewUserSt(BaseStation):
    @classmethod
    async def _stopover(cls, train):
        answer_info = {
            'unique_id': train.unique_id,
            'locale': train.storage['user_info']['locale'],
            'chat_id': train.storage['user_info']['chat_id']
        }
        ui.NewUser.generate(answer_info, train)
