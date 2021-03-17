# coding: utf-8

from typing import AnyStr, Dict, Iterable

from .file_reader import BaseFileReader
from .file_reader import YAMLFileReader
from .utils import get_from_environ
from .variables import AiogramVariables
from .variables import ConfigVariables


class ConfigReader:
    FILE_READER = YAMLFileReader

    def __init__(self):
        self.data: Dict = dict()
        self._aiogram: Dict = dict()
        self._logging: Dict = dict()

    def setup(self) -> 'ConfigReader':
        file_reader = self.FILE_READER
        if not issubclass(file_reader, BaseFileReader):
            raise TypeError(f'config_reader.FILE_READER is not '
                            f'child of {type(BaseFileReader)}')

        self.data = self.FILE_READER().setup().read()
        self._aiogram = {}
        self._logging = {}
        return self

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

        cnf_vars = self.data[str(section_name)]
        for var, val in env_vars.items():
            if val:
                cnf_vars[var] = val
        return cnf_vars

    def version(self):
        return self.data[str(ConfigVariables.VERSION)]

    def aiogram(self, var) -> AnyStr:
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
                str(ConfigVariables.AIOGRAM)
            )

        return self._aiogram[str(var)]

    def logging(self) -> Dict:
        """
        Отдаем сразу словарь, так как интерфейс
        библиотеки `logging` позволяет настройку
        через словарь.

        :return: dict
        """
        if not self._logging:
            self._logging = self.merge_variables(
                dict(),
                str(ConfigVariables.LOGGING)
            )
        return self._logging
