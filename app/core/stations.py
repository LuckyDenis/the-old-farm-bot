# coding: utf8

from logging import getLogger
from app.ui import interface as ui

logger = getLogger('app.core.station')


class BaseStation:
    """
    Интерфейс для классов необходимых классу `BaseItinerary`.

    Позволяют сделать какие-то небольшие наборы операций
    надо пользовательским запросом. Что дает возможность
    переиспользовать себя. Можно собирать в грозди.
    Подход паттерна `Цепочка обязанностей`.
    """

    @classmethod
    async def stopover(cls, train):
        """
        Точка входа, если при обработке запроса
        что-то где-то сломается, то сообщаем модулю
        выше, и уже выше стоящий модуль решает,
        как разобраться с возникшей ситуацией.
        У выше стоящих модулей, больше возможностей
        более чисто разрешить возникшую ситуацию.

        :param train: app.core.train
        """
        train.visited.append(cls)
        try:
            await cls._stopover(train)
        except (KeyError, ValueError) as e:
            train.has_fail = True
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
