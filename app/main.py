# coding: utf-8
from app.setup import use_polling
from app.setup import use_webhook
from app.setup import bot_section  # config_reader.aiogram()


def main():
    if bot_section.APP_BOT_USE_POLLING:
        use_polling()
    else:
        use_webhook()


if __name__ == '__main__':
    main()
