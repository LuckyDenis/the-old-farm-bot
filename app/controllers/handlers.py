# coding: utf8

from aiogram import types as t
from app.ui.commands import Commands
from app.controllers.utils import send_messages
from app.core import dispatcher as d
from app.setup import dp, bot


@dp.message_handler(commands=[Commands.Start.endpoint])
async def cmd_start(message: t.Message, unique_id):
    user_info = {
        'locale': message.from_user.locale.language,
        'chat_id': message.chat.id,
        'unique_id': unique_id
    }
    train = await d.CmdStart.on_itinerary(user_info)

    await send_messages(bot, train)
