# coding: utf-8

from typing import AnyStr, Dict, Type

from .file_reader import BaseFileReader
from .file_reader import YAMLFileReader
from .utils import get_from_environ


class ConfigReader:
    FILE_READER: Type[BaseFileReader] = YAMLFileReader

    def __init__(self):
        self.data: Dict = dict()
        self._aiogram: Dict = dict()
        self._logging: Dict = dict()

    def setup(self) -> 'ConfigReader':
        """
        Настройка и чтения файла конфигурации.

        Пример:
        config_reader = ConfigReader().setup()

        Пример:
        config_reader = ConfigReader()
        config_reader.setup()

        :return: ConfigReader
        """
        file_reader = self.FILE_READER()
        if not isinstance(file_reader, BaseFileReader):
            raise TypeError(f'config_reader.FILE_READER={type(file_reader)} '
                            f'не является типом {BaseFileReader}')

        self.data = file_reader.setup().read()
        self._aiogram = {}
        self._logging = {}
        return self

    def mount_section(self, section_name: AnyStr, env_merge: bool = False) -> Dict:
        """
        Подключает секцию с переменными.

        Флаг `env_merge=True` указывает на логику обработки
        значений которые будут храниться в подключенной секции.
        Так как не для всех секций необходимо слияние значений
        переменных из файла конфигурации и значения переменных
        окружения.

        Переменные окружения имеют более высоки приоритет, по этому
        перезаписывают значения переменных из файла конфигурации.

        :param section_name: str
        :param env_merge: bool, default = False

        :return: dict
        """
        section = self.data[section_name]
        if not env_merge:
            return section

        for variable in section:
            value = get_from_environ(variable)
            if value:
                section[variable] = value
        return section

    def version(self) -> AnyStr:
        """
        Версия файла конфигурации.
        1.2.3
        x.0.0 - major
        1.x.0 - minor
        1.2.x - patch

        :return: str
        """
        return self.data['VERSION']

    def aiogram(self, var: AnyStr) -> AnyStr:
        """
        Отдаем значение, а не словарь, так как
        требуется разный набор параметров для
        настройка методов `start_polling` и
        `start_webhook`.

        :param var: str
        :return: str
        """
        if not self._aiogram:
            self._aiogram = self.mount_section(
                'aiogram', env_merge=True
            )

        return self._aiogram[var]

    def logging(self) -> Dict:
        """
        Отдаем сразу словарь, так как интерфейс
        библиотеки `logging` позволяет настройку
        через словарь.
        Подробнее: `logging.config.dictConfig`.

        :return: dict
        """
        if not self._logging:
            self._logging = self.mount_section(
                'logging', env_merge=False
            )
        return self._logging
