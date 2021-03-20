# coding: utf8

from aiogram import types as t

from app import core
from app.setup import bot
from app.setup import dp
from app.ui import Commands
from .utils import send_messages


@dp.message_handler(commands=[Commands.Start.endpoint])
async def cmd_start(message: t.Message, unique_id):
    user_info = {
        'locale': message.from_user.locale.language,
        'chat_id': message.chat.id,
        'unique_id': unique_id
    }
    answers = await core.CmdStart.into(user_info)
    await send_messages(bot, answers)
