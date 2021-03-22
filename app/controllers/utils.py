# coding: utf8

from logging import getLogger

from app.ui.answer import MessageType

logger = getLogger('app.controllers.utils')


async def message_with_critical_error(bot, train):
    await bot.send_message(
        chat_id=train.chat_id,
        text=f"System error, id: {train.unique_id}"
    )


async def message_with_text(bot, answer):
    await bot.send_message(
        chat_id=answer.chat_id,
        text=answer.text,
        reply_markup=answer.keyboard
    )


def search_send_handler(message_type):
    send_handlers = {
        MessageType.TEXT: message_with_text
    }

    return send_handlers.get(message_type, MessageType.TEXT)


async def send_messages(bot, train):
    if train.has_fail:
        await message_with_critical_error(bot, train)
        return

    for answer in train.answers:
        send_handler = search_send_handler(answer.message_type)
        try:
            await send_handler(bot, answer)
            logger.debug(f'send_handler: {send_handler}, answer: {answer}')

        except RuntimeError as e:
            logger.error(f'error: {e}, train: {train}')
            await message_with_critical_error(bot, train)
            return
