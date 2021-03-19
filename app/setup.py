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


# ----------- ConfigReader Setup
config_reader = ConfigReader().setup()
dictConfig(config_reader.logging())

# ---------- Logging Setup
logger = getLogger(__file__)
logger.info(f'CONFIG VERSION: {config_reader.version()}')


# ---------- Aiogram Setup
parse_modes = {
    'html': ParseMode.HTML,
    'markdown': ParseMode.MARKDOWN,
    'markdown_v2': ParseMode.MARKDOWN_V2
}

aiogram_section = config_reader.aiogram()
bot = Bot(
    token=aiogram_section.API_TOKEN,
    parse_mode=parse_modes.get(aiogram_section.PARSE_MOD)
)
dp = Dispatcher(bot)


# ---------- Middleware Setup
dp.middleware.setup(UniqueIdMiddleware())


# ---------- I18N Setup
i18n_section = config_reader.i18n()
i18n = I18N(
    path=i18n_section.PATH,
    domain=i18n_section.DOMAIN,
    locales=i18n_section.LOCALES,
    default_locale=i18n_section.DEFAULT_LOCALE
)


# ---------- Function for bot
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
        skip_updates=aiogram_section.SKIP_UPDATES,
        timeout=aiogram_section.TIMEOUT,
        relax=aiogram_section.RELAX,
        fast=aiogram_section.FAST
    )


def use_webhook():
    start_webhook(
        dispatcher=dp,
        on_startup=on_startup_for_webhook,
        on_shutdown=on_shutdown_for_webhook,
        skip_updates=aiogram_section.SKIP_UPDATES,
        host=aiogram_section.WEBHOOK_HOST,
        port=aiogram_section.WEBHOOK_PORT,
        webhook_path=aiogram_section.WEBHOOK_PATH,
        check_ip=aiogram_section.CHECK_IP,
        retry_after=aiogram_section.RETRY_AFTER
    )
