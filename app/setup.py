# coding: utf8

from app.ui.i18n import I18N
from app.database.connecter import DBConnect
from app.configure.reader import ConfigReader
from app.middlewares.unique_id import UniqueIdMiddleware
from app.middlewares.database import DBMiddleware
from aiogram import Dispatcher
from aiogram import Bot
from aiogram.utils.executor import start_webhook
from aiogram.utils.executor import start_polling
from aiogram.types import ParseMode

from logging.config import dictConfig
from logging import getLogger
from logging import addLevelName


addLevelName(60, 'STARTUP')
# ----------- ConfigReader Setup
config_reader = ConfigReader().setup()

# ---------- Logging Setup
dictConfig(config_reader.logging())

logger = getLogger('app')
logger.log(60, f'Версия конфигурации: {config_reader.version()}')


# ---------- Aiogram Setup
parse_modes = {
    'html': ParseMode.HTML,
    'markdown': ParseMode.MARKDOWN,
    'markdown_v2': ParseMode.MARKDOWN_V2
}

bot_section = config_reader.bot()
bot = Bot(
    token=bot_section.APP_BOT_API_TOKEN,
    parse_mode=parse_modes.get(bot_section.APP_BOT_PARSE_MOD)
)
dp = Dispatcher(bot)


# ---------- Aiogram Setup
db_section = config_reader.database()
db_connect = DBConnect().setup(
    drive=db_section.APP_DB_DRIVER,
    port=db_section.APP_DB_PORT,
    host=db_section.APP_DB_HOST,
    username=db_section.APP_DB_USERNAME,
    password=db_section.APP_DB_PASSWORD,
    dbname=db_section.APP_DB_NAME,
    min_pool=db_section.APP_DB_MIN_POOL,
    max_pool=db_section.APP_DB_MAX_POOL,
    isolation_level=db_section.APP_DB_ISOLATION_LEVEL
)


# ---------- I18N Setup
i18n_section = config_reader.i18n()
i18n = I18N().setup(
    path=i18n_section.APP_LC_PATH,
    domain=i18n_section.APP_LC_DOMAIN,
    default_locale=i18n_section.APP_LC_DEFAULT_LOCALE
)


# ---------- Middleware Setup
dp.middleware.setup(UniqueIdMiddleware())
dp.middleware.setup(DBMiddleware(db_connect))


# ---------- Function for bot
async def on_startup_for_webhook(*_, webhook_url):
    await db_connect.test()
    await bot.set_webhook(webhook_url)


async def on_shutdown_for_webhook(*_):
    await db_connect.shutdown()
    await bot.delete_webhook()


async def on_startup_for_polling(*_):
    await db_connect.test()


async def on_shutdown_for_polling(*_):
    await db_connect.shutdown()


def use_polling():
    start_polling(
        dispatcher=dp,
        on_startup=on_startup_for_polling,
        on_shutdown=on_shutdown_for_polling,
        skip_updates=bot_section.APP_BOT_SKIP_UPDATES,
        timeout=bot_section.APP_BOT_TIMEOUT,
        relax=bot_section.APP_BOT_RELAX,
        fast=bot_section.APP_BOT_FAST
    )


def use_webhook():
    start_webhook(
        dispatcher=dp,
        on_startup=on_startup_for_webhook,
        on_shutdown=on_shutdown_for_webhook,
        skip_updates=bot_section.APP_BOT_SKIP_UPDATES,
        host=bot_section.APP_BOT_WEBHOOK_HOST,
        port=bot_section.APP_BOT_WEBHOOK_PORT,
        webhook_path=bot_section.APP_BOT_WEBHOOK_PATH,
        check_ip=bot_section.APP_BOT_CHECK_IP,
        retry_after=bot_section.APP_BOT_RETRY_AFTER
    )
