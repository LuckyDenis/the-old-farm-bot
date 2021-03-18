# coding: utf8
from app.setup import dp
from app.setup import bot
from aiogram import types as t
from app.ui import Commands


@dp.message_handler(commands=[Commands.Start.endpoint])
async def cmd_start(message: t.Message, unique_id):
    await bot.send_message(
        chat_id=message.chat.id,
        text=f'200, ok; unique_id: {unique_id}'
    )
