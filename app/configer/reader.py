# coding: utf-8

from dataclasses import dataclass, make_dataclass
from typing import AnyStr, Dict, Type

from .file_reader import BaseFileReader
from .file_reader import YAMLFileReader
from .utils import get_from_environ


@dataclass
class ConfigSections:
    AIOGRAM: AnyStr = 'aiogram'
    LOGGING: AnyStr = 'logging'
    I18N: AnyStr = 'i18n'
    VERSION = 'VERSION'


class ConfigReader:
    FILE_READER: Type[BaseFileReader] = YAMLFileReader

    def __init__(self):
        self.data: Dict = dict()
        self._aiogram: Dict = dict()
        self._logging: Dict = dict()
        self._i18n: Dict = dict()

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
        return self

    def _read_section(self, section_name: AnyStr, env_merge: bool = False) -> Dict:
        """
        Читает секцию с переменными.

        Флаг `env_merge=True` указывает на логику обработки
        значений которые будут храниться в прочитанной секции.
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
        return self.data[ConfigSections.VERSION]

    @staticmethod
    def _section_how_dataclass(cls_name: AnyStr, fields: Dict) -> dataclass:
        cls = make_dataclass(cls_name, fields=fields, eq=False)
        return cls(**fields)

    def aiogram(self) -> dataclass:
        """
        Отдаем `dataclass`, а не словарь, так как
        получившийся код будет чище, в разделе
        настройки модуля `app.setup`.

        :return: dataclass
        """
        if not self._aiogram:
            section = self._read_section(
                ConfigSections.AIOGRAM, env_merge=True
            )
            self._aiogram = self._section_how_dataclass(
                ConfigSections.AIOGRAM, section)

        return self._aiogram

    def logging(self) -> Dict:
        """
        Отдаем сразу словарь, так как интерфейс
        библиотеки `logging` позволяет настройку
        через словарь.
        Подробнее: `logging.config.dictConfig`.

        :return: dict
        """
        if not self._logging:
            self._logging = self._read_section(
                ConfigSections.LOGGING, env_merge=False
            )
        return self._logging

    def i18n(self) -> dataclass:
        """
        Отдаем `dataclass`, а не словарь, так как
        получившийся код будет чище, в разделе настройки
        модуля `app.setup`.

        :return: dataclass
        """
        if not self._i18n:
            section = self._read_section(
                ConfigSections.I18N, env_merge=True
            )
            self._i18n = self._section_how_dataclass(
                ConfigSections.I18N, section)

        return self._i18n
