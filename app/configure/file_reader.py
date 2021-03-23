# coding: utf8
from __future__ import annotations
from typing import TYPE_CHECKING

import os
import yaml

from app.configure.utils import get_from_environ


if TYPE_CHECKING:
    from app.typehint import TDict, TOptionAnyStr, TFileReader


class BaseFileReader:
    """
    Базовый класс для читателей конфигурационных файлов.

    Позволяет через единый интерфейс, реализовывать логику
    получения необходимых данных из различных типов файлов,
    без внесения изменения в кодовую базу.

    Требует реализации метода `read`.
    Используется для класса `ConfigReader`.
    Пример:
    ConfigReader.FILE_READER = YAMLFileReader
    """

    ENV_NAME_OF_CONFIG_PATH = 'CONFIG_PATH'
    ENV_NAME_OF_ENVIRONMENT = 'ENV'
    DEFAULT_ENVIRONMENT = 'develop'
    DEFAULT_CONFIG_PATH = '/etc/app'
    DEFAULT_CONFIG_NAME = 'app.yaml'

    def __init__(self):
        self.config_path: TOptionAnyStr = None
        self.environment: TOptionAnyStr = None

    def setup(self) -> TFileReader:
        """
        Фасад для удобной настройки и чтение файла.

        Пример:
        file_reader = BaseFileReader()
        file_reader.search_config_path()
        file_reader.search_environment()
        file_reader.read()

        Пример:
        file_reader = BaseFileReader()
        file_reader.setup().read()

        :return: BaseFileReader
        """
        self.search_config_path()
        self.search_environment()
        return self

    def search_config_path(self):
        self.config_path = get_from_environ(
            self.ENV_NAME_OF_CONFIG_PATH
        )

        if not self.config_path:
            self.config_path = os.path.join(
                self.DEFAULT_CONFIG_PATH,
                self.DEFAULT_CONFIG_NAME)

    def search_environment(self):
        self.environment = get_from_environ(
            self.ENV_NAME_OF_ENVIRONMENT
        )

        if not self.environment:
            self.environment = self.DEFAULT_ENVIRONMENT

    def read(self) -> TDict:
        """
        Требует реализации.

        Пример:
        with open(self.config_path, 'r') as file:
            data = yaml.SafeLoader(file).get_data()
        return data[self.environment]

        :return: dict
        """
        raise NotImplementedError()


class YAMLFileReader(BaseFileReader):
    """
    Читатель файла в формате `YAML`.

    Больше информации в docstring класса `BaseFileReader`.
    """

    def read(self) -> TDict:
        """
        :return: dict
        """

        with open(self.config_path, 'r') as file:
            data = yaml.SafeLoader(file).get_data()
        return data[self.environment]
