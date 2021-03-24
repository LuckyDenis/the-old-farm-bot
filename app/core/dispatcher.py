# coding: utf8
from __future__ import annotations
from typing import TYPE_CHECKING

from app.core import stations
from logging import getLogger
from app.core.train import Train
from app.ui.i18n import I18N

if TYPE_CHECKING:
    from app.typehint import TDict
    from app.typehint import TTrain
    from app.typehint import TStations
    from app.typehint import TAnyStr


logger = getLogger('app.core.dispatcher')
i18n = I18N()


class BaseItinerary:
    """
    Интерфейс для класса пути.

    Так как при обработке команд от пользователя,
    операции над данными могут часто повторяться,
    что бы не копировать эту логику, выделим её в
    небольшие классы, которые делают что-то одно,
    и будем обходить используя общий интерфейс.
    Принцип паттерна `Цепочка обязанностей`.
    """

    _default_locale: TAnyStr = i18n.ctx_locale.get()

    @classmethod
    def _prepare_train(cls, user_info: TDict) -> TTrain:
        """
        Создание контейнера для данных.

        Устанавливаем `locale` - пользователя или
        по умолчанию в системе.

        :param user_info: dict
        :return: app.core.train
        """
        user_info['locale'] = user_info.get(
            'locale', cls._default_locale)

        train = Train(
            unique_id=user_info['unique_id'],
            chat_id=user_info['chat_id'],
            destination=str(cls),
            storage={
                'user_info': user_info
            }
        )

        logger.debug(f'train: {train}')
        return train

    @classmethod
    async def on_itinerary(cls, user_info: TDict) -> TTrain:
        """
        Точка входа.

        :param user_info: dict
        :return: app.core.train
        """
        train = cls._prepare_train(user_info)

        await cls._traveling(train)
        if train.has_fail:
            await cls._travel_is_fail(train)
        return train

    @classmethod
    async def _travel_is_fail(cls, train: TTrain):
        train.answers.clear()
        train.has_fail = False
        await stations.UISystemExceptionSt.stopover(train)

    @classmethod
    async def _traveling(cls, train: TTrain):
        """
        Тут только логика обхода.

        Если в ходе обхода случилась ошибка,
        то останавливаем обход, и пускай её
        обрабатывают выше.

        :param train: app.core.train
        """
        for station in cls._stations():
            await station.stopover(train)
            if train.has_fail:
                return

    @classmethod
    def _stations(cls) -> TStations:
        raise NotImplementedError()


class SystemException(BaseItinerary):
    @classmethod
    def _stations(cls) -> TStations:
        return [
            stations.BeginSt,
            stations.NewUserSt,
            stations.UINewUserSt,
            stations.FinishSt
        ]


class CmdStart(BaseItinerary):
    @classmethod
    def _stations(cls) -> TStations:
        return [
            stations.BeginSt,
            stations.NewUserSt,
            stations.UINewUserSt,
            stations.FinishSt
        ]
