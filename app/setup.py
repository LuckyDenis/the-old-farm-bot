# coding: utf8

from aiogram import Dispatcher
from aiogram import Bot
from aiogram.utils.executor import start_webhook
from aiogram.utils.executor import start_polling
from aiogram.types import ParseMode
from app.configer import ConfigReader
from app.configer import AiogramVariables
from app.configer import LoggingVariables
from logging.config import dictConfig
from logging import getLogger


reader = ConfigReader()
dictConfig(reader.logging())

logger = getLogger(__file__)
AIOGRAM_CONFIG_VERSION = reader.aiogram(AiogramVariables.VERSION)
LOGGING_CONFIG_VERSION = reader.aiogram(LoggingVariables.VERSION)
logger.info(f'CONFIG VERSION: ('
            f'aiogram: {AIOGRAM_CONFIG_VERSION}, '
            f'logging: {LOGGING_CONFIG_VERSION})')

parse_modes = {
    'html': ParseMode.HTML,
    'markdown': ParseMode.MARKDOWN,
    'markdown_v2': ParseMode.MARKDOWN_V2
}

bot = Bot(
    token=reader.aiogram(AiogramVariables.API_TOKEN),
    parse_mode=parse_modes.get(reader.aiogram(AiogramVariables.PARSE_MOD))
)
dp = Dispatcher(bot)


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
        skip_updates=reader.aiogram(AiogramVariables.SKIP_UPDATES),
        timeout=reader.aiogram(AiogramVariables.TIMEOUT),
        relax=reader.aiogram(AiogramVariables.RELAX),
        fast=reader.aiogram(AiogramVariables.FAST)
    )


def use_webhook():
    start_webhook(
        dispatcher=dp,
        on_startup=on_startup_for_webhook,
        on_shutdown=on_shutdown_for_webhook,
        skip_updates=reader.aiogram(AiogramVariables.SKIP_UPDATES),
        host=reader.aiogram(AiogramVariables.WEBHOOK_HOST),
        port=reader.aiogram(AiogramVariables.WEBHOOK_PORT),
        webhook_path=reader.aiogram(AiogramVariables.WEBHOOK_PATH),
        check_ip=reader.aiogram(AiogramVariables.CHECK_IP),
        retry_after=reader.aiogram(AiogramVariables.RETRY_AFTER)
    )
