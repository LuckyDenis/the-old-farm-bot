# coding: utf8

from aiogram import Dispatcher
from aiogram import Bot
from aiogram.utils.executor import start_webhook
from aiogram.utils.executor import start_polling
from aiogram.types import ParseMode
from app.ui import I18N
from app.configer import ConfigReader
from app.middlewares import UniqueIdMiddleware
from logging.config import dictConfig
from logging import getLogger


# ----------- ConfigReader Setup
config_reader = ConfigReader().setup()
dictConfig(config_reader.logging())

# ---------- Logging Setup
logger = getLogger('app')
logger.info(f'CONFIG VERSION: {config_reader.version()}')


# ---------- Aiogram Setup
parse_modes = {
    'html': ParseMode.HTML,
    'markdown': ParseMode.MARKDOWN,
    'markdown_v2': ParseMode.MARKDOWN_V2
}

aiogram_section = config_reader.aiogram()
bot = Bot(
    token=aiogram_section.APP_AG_API_TOKEN,
    parse_mode=parse_modes.get(aiogram_section.APP_AG_PARSE_MOD)
)
dp = Dispatcher(bot)


# ---------- Middleware Setup
dp.middleware.setup(UniqueIdMiddleware())


# ---------- I18N Setup
i18n_section = config_reader.i18n()
i18n = I18N().setup(
    path=i18n_section.APP_LC_PATH,
    domain=i18n_section.APP_LC_DOMAIN,
    default_locale=i18n_section.APP_LC_DEFAULT_LOCALE
)


# ---------- Function for bot
async def on_startup_for_webhook(*_, webhook_url):
    i18n.reload()
    await bot.set_webhook(webhook_url)


async def on_shutdown_for_webhook(*_):
    await bot.delete_webhook()


async def on_startup_for_polling(*_):
    i18n.reload()


async def on_shutdown_for_polling(*_):
    pass


def use_polling():
    start_polling(
        dispatcher=dp,
        on_startup=on_startup_for_polling,
        on_shutdown=on_shutdown_for_polling,
        skip_updates=aiogram_section.APP_AG_SKIP_UPDATES,
        timeout=aiogram_section.APP_AG_TIMEOUT,
        relax=aiogram_section.APP_AG_RELAX,
        fast=aiogram_section.APP_AG_FAST
    )


def use_webhook():
    start_webhook(
        dispatcher=dp,
        on_startup=on_startup_for_webhook,
        on_shutdown=on_shutdown_for_webhook,
        skip_updates=aiogram_section.APP_AG_SKIP_UPDATES,
        host=aiogram_section.APP_AG_WEBHOOK_HOST,
        port=aiogram_section.APP_AG_WEBHOOK_PORT,
        webhook_path=aiogram_section.APP_AG_WEBHOOK_PATH,
        check_ip=aiogram_section.APP_AG_CHECK_IP,
        retry_after=aiogram_section.APP_AG_RETRY_AFTER
    )
