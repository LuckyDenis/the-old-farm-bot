# coding: utf8
from typing import List

from app.ui.answer import MessageType


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


async def send_messages(bot, answers: List):
    for answer in answers:
        send_handler = search_send_handler(answer.message_type)
        try:
            await send_handler(bot, answer)
        except RuntimeError:
            await bot.send_message(
                chat_id=answer.chat_id,
                text=f"System error, id: {answer.unique_id}"
            )
