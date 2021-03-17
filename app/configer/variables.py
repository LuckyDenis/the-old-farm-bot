# coding: utf8
"""
Реализованно для удобства работы с большим количеством
переменных. Используется `Enum`, так как он позволяет
итерироваться по классу как по словарю.
"""

from enum import Enum
from enum import unique


class BaseVariables(Enum):
    """
    Так как нам нужно особое поведение для класса
    """

    def __str__(self):
        """
        Перегружаем метод `__str__`, что бы получать
        за место `<BaseVariables.Foo: Foo>` значение
        в формате `str(Foo)`.
        :return: str
        """
        return str(self._value_)


@unique
class AiogramVariables(BaseVariables):
    """
    Переменные секции `ConfigVariables.AIOGRAM`.
    """
    API_TOKEN = 'API_TOKEN'
    WEBHOOK_HOST = 'WEBHOOK_HOST'
    WEBHOOK_PORT = 'WEBHOOK_PORT'
    WEBHOOK_PATH = 'WEBHOOK_PATH'
    USE_POLLING = 'USE_POLLING'
    PARSE_MOD = 'PARSE_MOD'
    SKIP_UPDATES = 'SKIP_UPDATES'
    CHECK_IP = 'CHECK_IP'
    RETRY_AFTER = 'RETRY_AFTER'
    TIMEOUT = 'TIMEOUT'
    RELAX = 'RELAX'
    FAST = 'FAST'


@unique
class ConfigVariables(BaseVariables):
    """
    Секции в файле конфигурации.
    """
    VERSION = 'VERSION'
    LOGGING = 'logging'
    AIOGRAM = 'aiogram'
