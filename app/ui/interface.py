# coding: utf8
from __future__ import annotations
from typing import TYPE_CHECKING

from logging import getLogger

import app.ui.keyboards as k7s
import app.ui.templates as t7s
from app.ui.answer import AnswerWithText
from app.ui.i18n import I18N


if TYPE_CHECKING:
    from app.typehint import TTrain
    from app.typehint import TDict
    from app.typehint import TAnswer


logger = getLogger('app.ui.interface')


i18n = I18N()


class BaseInterface:
    """
    Интерфейс для классов создающие ответ содержащий
    пользовательский интерфейс.

    """
    @classmethod
    def generate(cls, answer_info: TDict, train: TTrain):
        """
        Точка входа.

        Если случается ошибка, то сообщаем классу `BaseItinerary`,
        о том что-то пошло не так, и пусть он решает что делать с
        запросом пользователя в таком случае, так как он отвечает
        за запрос пользователя в системе.

        Устанавливаем `i18n.set_locale` здесь, для того, что бы
        изменения user.locale пользователя распространилась на
        модули `app.ui.templates` и `app.ui.keyboards`.

        :param answer_info: dict
        :param train: app.core.train
        """
        logger.debug(f'answer_info: {answer_info}, train: {train}')
        try:
            i18n.set_locale(answer_info['locale'])
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
    def _generate(cls, answer_info: TDict) -> TAnswer:
        raise NotImplementedError()


class SystemException(BaseInterface):
    @classmethod
    def _generate(cls, answer_info: TDict) -> TAnswer:
        state = {
            'unique_id': answer_info['unique_id']
        }
        answer_text = t7s.SystemException.rendering(state)
        keyboard = k7s.SystemException.keyboard()

        answer_with_text = AnswerWithText(
            chat_id=answer_info['chat_id'],
            text=answer_text,
            unique_id=answer_info['unique_id'],
            keyboard=keyboard
        )

        return answer_with_text


# ---------- cmd: start ---------- #
class NewUser(BaseInterface):
    @classmethod
    def _generate(cls, answer_info: TDict) -> TAnswer:
        state = {
            'unique_id': answer_info['unique_id']
        }
        answer_text = t7s.NewUser.rendering(state)
        keyboard = k7s.NewUser.keyboard()

        answer_with_text = AnswerWithText(
            chat_id=answer_info['chat_id'],
            text=answer_text,
            unique_id=answer_info['unique_id'],
            keyboard=keyboard
        )

        return answer_with_text
