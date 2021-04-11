# coding: utf8
from __future__ import annotations
from typing import TYPE_CHECKING

from app.ui.commands import Commands
from app.controllers.sender import send_messages
from app.core import dispatcher as d
from app.setup import dp, bot


if TYPE_CHECKING:
    from app.typehint import Train
    from app.typehint import TMessage
    from app.typehint import TAnyStr


# ---------- cmd: start --------- #
@dp.message_handler(commands=[Commands.Start.endpoint])
async def cmd_start(message: TMessage, unique_id: TAnyStr):
    user_info = {
        'locale': message.from_user.locale.language,
        'chat_id': message.chat.id,
        'unique_id': unique_id
    }
    train: Train = await d.CmdStart.on_itinerary(user_info)

    await send_messages(bot, train)
