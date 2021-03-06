# coding: utf8
from __future__ import annotations
from typing import TYPE_CHECKING
from logging import getLogger

from app.ui.answer import MessageType

if TYPE_CHECKING:
    from app.typehint import TTrain
    from app.typehint import TAnswerWithText
    from app.typehint import TEnumAuto
    from app.typehint import TBot


logger = getLogger('app.controllers.utils')


async def message_with_critical_error(bot: TBot, train: TTrain):
    """
    Если модуль `app.core.dispatcher` не смог справиться
    с ошибкой, или при отправке сообщения случилась ошибка,
    то значит, что-то случилось из ряда не предусмотренного.
    По этому надо отдать пользователю хоть какой-то ответ.
    Так как не известна причина сбоя, то ответ деградирует,
    до простого текстового сообщения с уникальным номером.

    :param bot: aiogram.types.bot
    :param train: app.core.train
    """
    await bot.send_message(
        chat_id=train.chat_id,
        text=f"System error, id: {train.unique_id}"
    )


async def message_with_text(bot: TBot, answer: TAnswerWithText):
    """
    Сообщение, которое содержит, только текст.

    :param bot: aiogram.types.bot
    :param answer: app.ui.answer
    """
    await bot.send_message(
        chat_id=answer.chat_id,
        text=answer.text,
        reply_markup=answer.keyboard
    )


def search_send_handler(message_type: TEnumAuto):
    """
    Для разных типов сообщений требуется разный набор
    параметров. Для этого используем разные обработчик,
    и применим паттерн `Стратегия`, для выбора подходящего
    обработчик, и определим логику в обработчике, тогда
    детали реализации становятся менее связанные.

    :param message_type: app.ui.answer
    """
    send_handlers = {
        MessageType.TEXT: message_with_text
    }

    return send_handlers.get(message_type, MessageType.TEXT)


async def send_messages(bot: TBot, train: TTrain):
    """
    Точка отправки ответов.

    Чтобы не копировать логику отправки в модуле
    `app.controllers.handlers` для каждой точки входа,
    выделим общий интерфейс, и будем уже в одном месте
    решать, каким образом отправлять сообщение.

    :param bot: aiogram.types.bot
    :param train: app.core.train
    """
    if train.has_fail:
        await message_with_critical_error(bot, train)
        return

    for answer in train.answers:
        send_handler = search_send_handler(answer.message_type)
        try:
            await send_handler(bot, answer)
            logger.debug(f'send_handler: {send_handler}, answer: {answer}')

        except TypeError as e:
            logger.error(f'error: {e}, train: {train}')
            await message_with_critical_error(bot, train)
            return
