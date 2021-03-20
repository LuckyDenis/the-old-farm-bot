# coding: utf8

from logging import getLogger
from typing import AnyStr

from app.ui import keyboards as k7s
from app.ui import templates as t7s
from app.ui.answer import AnswerWithText
from app.ui.answer import MessageType

logger = getLogger('app.ui.interface')


class BaseInterface:
    @classmethod
    def rendering(cls, answer_info, train):
        try:
            train.answers.append(
                cls._rendering(answer_info)
            )
        except (
                ValueError, TypeError,
                OSError, KeyError,
                FileNotFoundError) as e:
            logger.error(e)
            train.has_fail = True

    @classmethod
    def _rendering(cls, answer_info):
        raise NotImplementedError()


class SystemException(BaseInterface):
    @classmethod
    def _rendering(cls, answer_info):
        state = {
            'unique_id': answer_info['unique_id'],
            'locale': answer_info['locale']
        }
        answer_text: AnyStr = t7s.SystemException.rendering(state)

        answer_with_text = AnswerWithText(
            chat_id=answer_info['chat_id'],
            message_type=MessageType.TEXT,
            text=answer_text,
            unique_id=answer_info['unique_id'],
            keyboard=k7s.SystemException.keyboard
        )

        return answer_with_text


# ---------- cmd: start ---------- #
class NewUser(BaseInterface):
    @classmethod
    def _rendering(cls, answer_info):
        state = {
            'unique_id': answer_info['unique_id'],
            'locale': answer_info['locale']
        }
        answer_text: AnyStr = t7s.NewUser.rendering(state)

        answer_with_text = AnswerWithText(
            chat_id=answer_info['chat_id'],
            message_type=MessageType.TEXT,
            text=answer_text,
            unique_id=answer_info['unique_id'],
            keyboard=k7s.NewUser.keyboard
        )

        return answer_with_text
