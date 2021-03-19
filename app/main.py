# coding: utf-8
from app.setup import use_polling
from app.setup import use_webhook
from app.setup import aiogram_section  # config_reader.aiogram()


def main():
    if aiogram_section.USE_POLLING:
        use_polling()
    else:
        use_webhook()


if __name__ == '__main__':
    main()
