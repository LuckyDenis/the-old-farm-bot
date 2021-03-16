# coding: utf-8

import os
import yaml
from enum import Enum
from enum import unique
from typing import AnyStr, Dict, Iterable


def convert_enum_to_string(var) -> AnyStr:
    """
    Нужен для того что бы использовать измененные
    объекты Enum, с  __getitem__.

    :param var: str, BaseVariables
    :return: str
    """
    if isinstance(var, Enum):
        return str(var)
    return var


def get_from_environ(environ_name) -> AnyStr:
    return os.environ.get(
        convert_enum_to_string(environ_name))


class BaseFileReader:
    """
    Базовый класс для читателей конфигурационных файлов.

    Позволяет через единый интерфейс, реализовывать логику
    получения необходимых конфигурационных данных из различных
    типов файлов, без внесения изменения в кодовую базу.

    Требует реализации метода `read`.
    Используется для класса `ConfigReader`.
    Например:
    `ConfigReader.FILE_READER = YAMLFileReader`
    """

    ENV_NAME_OF_CONFIG_PATH = 'CONFIG_PATH'
    ENV_NAME_OF_ENVIRONMENT = 'ENV'
    DEFAULT_ENVIRONMENT = 'develop'
    DEFAULT_CONFIG_PATH = '/etc/app'
    DEFAULT_CONFIG_NAME = 'app.yaml'

    def __init__(self):
        self.config_path = self.search_config_path()
        self.environment = self.search_environment()

    def search_config_path(self) -> AnyStr:
        config_path = get_from_environ(
            self.ENV_NAME_OF_CONFIG_PATH
        )

        if config_path:
            return config_path
        return os.path.join(
            self.DEFAULT_CONFIG_PATH,
            self.DEFAULT_CONFIG_NAME
        )

    def search_environment(self) -> AnyStr:
        environment = get_from_environ(
            self.ENV_NAME_OF_ENVIRONMENT
        )

        if environment:
            return environment
        return self.DEFAULT_ENVIRONMENT

    def read(self) -> Dict:
        """
        Требует реализации.

        Например:
        with open(self.config_path, 'r') as file:
            data = yaml.SafeLoader(file).get_data()
        return data[self.environment]

        :return: dict
        """
        raise NotImplementedError()


class YAMLFileReader(BaseFileReader):
    """
    Читатель конфигурационного файла в формате `YAML`.

    Больше информации в docstring класса `BaseFileReader`.
    """

    def read(self) -> dict:
        """
        :return: dict
        """

        with open(self.config_path, 'r') as file:
            data = yaml.SafeLoader(file).get_data()
        return data[self.environment]


class BaseVariables(Enum):
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
    VERSION = 'VERSION'


@unique
class LoggingVariables(BaseVariables):
    VERSION = 'VERSION'


class ConfigReader:
    FILE_READER: BaseFileReader = YAMLFileReader

    def __init__(self):
        if not issubclass(self.FILE_READER, BaseFileReader):
            raise TypeError(f'FILE_READER is not '
                            f'child of {type(BaseFileReader)}')

        self.data = self.FILE_READER().read()
        self._aiogram = {}
        self._logging = {}

    def merge_variables(self, var_list: Iterable, section_name: AnyStr) -> Dict:
        """
        Переменные окружения имеют более высоки приоритет,
        по этому перезаписываем переменные из файла конфигурации.

        :param var_list: dict
        :param section_name:
        :return:
        """
        env_vars = {}
        for var in var_list:
            env_vars[var] = get_from_environ(var)

        cnf_vars = self.data[section_name]
        for var, val in env_vars.items():
            if val:
                cnf_vars[var] = val
        return cnf_vars

    def aiogram(self, var: AnyStr) -> AnyStr:
        """
        Отдаем строку содержащие значение, переменной настройки,
        так как требуется немного разная настройка для методов
        `start_polling` и `start_webhook`.

        :param var: str
        :return: str
        """
        if not self._aiogram:
            self._aiogram = self.merge_variables(
                AiogramVariables,
                'aiogram'
            )

        return self._aiogram[convert_enum_to_string(var)]

    def logging(self) -> Dict:
        """
        Отдаем сразу словарь, так как интерфейс
        библиотеки `logging` позволяет настройку
        через словарь.

        :return: dict
        """
        if not self._logging:
            self._logging = self.merge_variables(
                LoggingVariables,
                'logging'
            )
        return self._logging
