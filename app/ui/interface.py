# coding: utf8

from logging import getLogger

import app.ui.keyboards as k7s
import app.ui.templates as t7s
from app.ui.answer import AnswerWithText
from app.ui.answer import MessageType

logger = getLogger('app.ui.interface')


class BaseInterface:
    @classmethod
    def generate(cls, answer_info, train):
        logger.debug(f'answer_info: {answer_info}, train: {train}')
        try:
            train.answers.append(
                cls._generate(answer_info)
            )
        except (ValueError, TypeError,
                OSError, KeyError,
                FileNotFoundError) as e:
            train.has_fail = True
            logger.error(
                f'error: {e}, answer_info: {answer_info}, train: {train}')

    @classmethod
    def _generate(cls, answer_info):
        raise NotImplementedError()


class SystemException(BaseInterface):
    @classmethod
    def _generate(cls, answer_info):
        state = {
            'unique_id': answer_info['unique_id'],
            'locale': answer_info['locale']
        }
        answer_text = t7s.SystemException.rendering(state)

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
    def _generate(cls, answer_info):
        state = {
            'unique_id': answer_info['unique_id'],
            'locale': answer_info['locale']
        }
        answer_text = t7s.NewUser.rendering(state)

        answer_with_text = AnswerWithText(
            chat_id=answer_info['chat_id'],
            message_type=MessageType.TEXT,
            text=answer_text,
            unique_id=answer_info['unique_id'],
            keyboard=k7s.NewUser.keyboard
        )

        return answer_with_text
