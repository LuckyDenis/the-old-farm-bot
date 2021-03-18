# coding: utf8

from aiogram import Dispatcher
from aiogram import Bot
from aiogram.utils.executor import start_webhook
from aiogram.utils.executor import start_polling
from aiogram.types import ParseMode
from app.configer import ConfigReader
from app.ui import I18N
from app.middlewares import UniqueIdMiddleware
from logging.config import dictConfig
from logging import getLogger


reader = ConfigReader().setup()
dictConfig(reader.logging())

logger = getLogger(__file__)
logger.info(f'CONFIG VERSION: {reader.version()}')

parse_modes = {
    'html': ParseMode.HTML,
    'markdown': ParseMode.MARKDOWN,
    'markdown_v2': ParseMode.MARKDOWN_V2
}

i18n = I18N()
bot = Bot(
    token=reader.aiogram('API_TOKEN'),
    parse_mode=parse_modes.get(reader.aiogram('PARSE_MOD'))
)
dp = Dispatcher(bot)
dp.middleware.setup(UniqueIdMiddleware())


async def on_startup_for_webhook(*_, webhook_url):
    await bot.set_webhook(webhook_url)


async def on_shutdown_for_webhook(*_):
    await bot.delete_webhook()


async def on_startup_for_polling(*_):
    pass


async def on_shutdown_for_polling(*_):
    pass


def use_polling():
    start_polling(
        dispatcher=dp,
        on_startup=on_startup_for_polling,
        on_shutdown=on_shutdown_for_polling,
        skip_updates=reader.aiogram('SKIP_UPDATES'),
        timeout=reader.aiogram('TIMEOUT'),
        relax=reader.aiogram('RELAX'),
        fast=reader.aiogram('FAST')
    )


def use_webhook():
    start_webhook(
        dispatcher=dp,
        on_startup=on_startup_for_webhook,
        on_shutdown=on_shutdown_for_webhook,
        skip_updates=reader.aiogram('SKIP_UPDATES'),
        host=reader.aiogram('WEBHOOK_HOST'),
        port=reader.aiogram('WEBHOOK_PORT'),
        webhook_path=reader.aiogram('WEBHOOK_PATH'),
        check_ip=reader.aiogram('CHECK_IP'),
        retry_after=reader.aiogram('RETRY_AFTER')
    )
