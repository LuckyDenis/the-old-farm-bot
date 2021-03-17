# coding: utf8

import os
from typing import Dict, NoReturn

import yaml

from .utils import get_from_environ


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
        self.config_path = None
        self.environment = None

    def setup(self) -> 'BaseFileReader':
        """
        Фасад для удобной настройки и прочтения файла
        с конфигурацией для читателя.

        За место:
        file_reader = BaseFileReader()
        file_reader.search_config_path()
        file_reader.search_environment()
        file_reader.read()

        Писать так:
        file_reader = BaseFileReader()
        file_reader.setup().read()
        :return:
        """
        self.search_config_path()
        self.search_environment()
        return self

    def search_config_path(self) -> NoReturn:
        self.config_path = get_from_environ(
            self.ENV_NAME_OF_CONFIG_PATH
        )

        if not self.config_path:
            self.config_path = os.path.join(
                self.DEFAULT_CONFIG_PATH,
                self.DEFAULT_CONFIG_NAME)

    def search_environment(self) -> NoReturn:
        self.environment = get_from_environ(
            self.ENV_NAME_OF_ENVIRONMENT
        )

        if not self.environment:
            self.environment = self.DEFAULT_ENVIRONMENT

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
