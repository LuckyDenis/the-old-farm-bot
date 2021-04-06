# coding: utf8
from __future__ import annotations
from typing import TYPE_CHECKING

from logging import getLogger
from app.ui import interface as ui

if TYPE_CHECKING:
    from app.typehint import TTrain


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
    async def stopover(cls, train: TTrain):
        """
        Точка входа.

        Если при обработке запроса
        что-то где-то сломается, то сообщаем модулю
        выше, и уже выше стоящий модуль решает,
        как разобраться с возникшей ситуацией.
        У выше стоящих модулей, больше возможностей
        более чисто разрешить возникшую ситуацию.

        :param train: app.core.train
        """
        train.visited.append(cls.__name__)
        try:
            cls._check_fields(train)
            await cls._stopover(train)
        except (KeyError, ValueError) as e:
            train.has_fail = True
            logger.error(f'error: {e}, cls: {cls.__name__}, train: {train}')

    @classmethod
    def _check_fields(cls, train: TTrain):
        # TODO: Реализовать, на подобии cls._stopover()
        pass

    @classmethod
    async def _stopover(cls, train: TTrain):
        raise NotImplementedError()


class BeginSt(BaseStation):
    @classmethod
    async def _stopover(cls, train: TTrain):
        # TODO: Реализовать
        pass


class FinishSt(BaseStation):
    @classmethod
    async def _stopover(cls, train: TTrain):
        # TODO: Реализовать
        pass


class NewUserSt(BaseStation):
    @classmethod
    async def _stopover(cls, train: TTrain):
        # TODO: Реализовать
        pass


class UISystemExceptionSt(BaseStation):
    @classmethod
    async def _stopover(cls, train: TTrain):
        answer_info = {
            'unique_id': train.unique_id,
            'locale': train.storage['user_info']['locale'],
            'chat_id': train.storage['user_info']['chat_id']
        }
        ui.SystemException.generate(answer_info, train)


class UINewUserSt(BaseStation):
    @classmethod
    async def _stopover(cls, train: TTrain):
        answer_info = {
            'unique_id': train.unique_id,
            'locale': train.storage['user_info']['locale'],
            'chat_id': train.storage['user_info']['chat_id']
        }
        ui.NewUser.generate(answer_info, train)
