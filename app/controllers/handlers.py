# coding: utf8
from app.setup import dp
from app.setup import bot
from aiogram import types as t


@dp.message_handler(content_types=t.ContentTypes.TEXT)
async def cmd_start(message: t.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text='200, ok'
    )
