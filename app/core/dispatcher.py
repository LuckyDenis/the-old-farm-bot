# coding: utf8

from app.core import stations
from logging import getLogger
from typing import Dict
from app.core.depot import Train
from app.ui.i18n import I18N


logger = getLogger('app.core.dispatcher')
i18n = I18N()


class BaseItinerary:
    default_locale = i18n.ctx_locale.get()
    stations = list()

    @classmethod
    def prepare_train(cls, user_info: Dict):
        train = Train(
            unique_id=user_info['unique_id'],
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
        return train

    @classmethod
    async def into(cls, user_info):
        train = cls.prepare_train(user_info)
        logger.error(train)
        return await cls._into(train)

    @classmethod
    async def _into(cls, train):
        raise NotImplementedError()


class CmdStart(BaseItinerary):
    stations = [
        stations.BeginSt,
        stations.NewUserSt,
        stations.UINewUserSt,
        stations.FinishSt
    ]

    @classmethod
    async def _into(cls, train):
        for station in cls.stations:
            await station.to_move(train)
            if train.has_fail:
                break

        if train.has_fail:
            train.answers.clear()
            train.has_fail = False
            logger.error('error')
        return train.answers
