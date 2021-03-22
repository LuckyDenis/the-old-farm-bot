# coding: utf8

from app.core import stations
from logging import getLogger
from app.core.depot import Train
from app.ui.i18n import I18N


logger = getLogger('app.core.dispatcher')
i18n = I18N()


class BaseItinerary:
    default_locale = i18n.ctx_locale.get()

    @classmethod
    def prepare_train(cls, user_info):
        train = Train(
            unique_id=user_info['unique_id'],
            chat_id=user_info['chat_id'],
            destination=str(cls),
            answers=list(),
            has_fail=False,
            storage={
                'user_info': {
                    'locale': user_info['locale'],
                    'chat_id': user_info['chat_id']
                }
            }
        )
        logger.debug(f'train: {train}')
        return train

    @classmethod
    async def on_itinerary(cls, user_info):
        train = cls.prepare_train(user_info)
        await cls.traveling(train)

        if train.has_fail:
            await cls.travel_is_fail(train)
        return train

    @classmethod
    async def travel_is_fail(cls, train):
        train.answers.clear()
        train.has_fail = False
        await stations.UISystemExceptionSt.stopover(train)

    @classmethod
    async def traveling(cls, train):
        for station in cls.stations():
            await station.stopover(train)
            if train.has_fail:
                return

    @classmethod
    def stations(cls):
        raise NotImplementedError()


class SystemException(BaseItinerary):
    @classmethod
    def stations(cls):
        return [
            stations.BeginSt,
            stations.NewUserSt,
            stations.UINewUserSt,
            stations.FinishSt
        ]


class CmdStart(BaseItinerary):
    @classmethod
    def stations(cls):
        return [
            stations.BeginSt,
            stations.NewUserSt,
            stations.UINewUserSt,
            stations.FinishSt
        ]
