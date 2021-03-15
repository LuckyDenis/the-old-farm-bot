# coding: utf-8

import os
import yaml


def get_from_environ(environ_name):
    return os.environ.get(environ_name)


class BaseFileReader:
    """
    Базовый класс для читателей конфигурационных файлов.

    Перегруженный класс с реализацией метода read можно
    передать как один из параметров в класс `ConfigReader`.
    Например:
    config_reader = ConfigReader(file_reader=YAMLFileReader)
    """

    ENV_NAME_OF_CONFIG_PATH = 'config_file'
    ENV_NAME_OF_ENVIRONMENT = 'env'
    DEFAULT_ENVIRONMENT = 'develop'
    DEFAULT_CONFIG_PATH = '/etc/app'
    DEFAULT_CONFIG_NAME = 'app.yaml'

    def __init__(self):
        self.config_path = self.search_config_path()
        self.environment = self.search_environment()

    def search_config_path(self):
        config_path = get_from_environ(
            self.ENV_NAME_OF_CONFIG_PATH
        )

        if config_path:
            return config_path
        return os.path.join(
            self.DEFAULT_CONFIG_PATH,
            self.DEFAULT_CONFIG_NAME
        )

    def search_environment(self):
        environment = get_from_environ(
            self.ENV_NAME_OF_ENVIRONMENT
        )

        if environment:
            return environment
        return self.DEFAULT_ENVIRONMENT

    def read(self):
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

    def read(self):
        """
        :return: dict
        """

        with open(self.config_path, 'r') as file:
            data = yaml.SafeLoader(file).get_data()
        return data[self.environment]


class ConfigReader:
    pass
