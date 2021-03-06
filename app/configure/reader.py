# coding: utf-8
from __future__ import annotations
from dataclasses import dataclass, make_dataclass
from typing import TYPE_CHECKING
from logging import getLogger


from app.configure.file_reader import BaseFileReader
from app.configure.file_reader import YAMLFileReader
from app.configure.utils import get_from_environ


if TYPE_CHECKING:
    from app.typehint import TAnyStr
    from app.typehint import TFileReader
    from app.typehint import TDict
    from app.typehint import TConfigReader
    from app.typehint import TBool
    from app.typehint import TDataClass


logger = getLogger('app.configure.reader')


@dataclass
class ConfigSections:
    BOT: TAnyStr = 'bot'
    LOGGING: TAnyStr = 'logging'
    I18N: TAnyStr = 'i18n'
    DATABASE: TAnyStr = 'database'
    NEW_GAMER: TAnyStr = 'new_gamer'
    VERSION: TAnyStr = 'VERSION'


class ConfigReader:
    FILE_READER: TFileReader = YAMLFileReader

    def __init__(self):
        self.data: TDict = dict()
        self._logging: TDict = dict()
        self._i18n: TDataClass = None
        self._bot: TDataClass = None
        self._database: TDataClass = None
        self._new_gamer: TDataClass = None

    def setup(self) -> TConfigReader:
        """
        Настройка и чтения файла конфигурации.

        Пример:
        config_reader = ConfigReader().setup()

        Пример:
        config_reader = ConfigReader()
        config_reader.setup()

        :return: ConfigReader
        """
        file_reader = self.FILE_READER
        # bug: https://youtrack.jetbrains.com/issue/PY-43688
        if not issubclass(file_reader, BaseFileReader):  # noqa
            raise TypeError(f'config_reader.FILE_READER={type(file_reader)} '
                            f'не является типом {BaseFileReader}')

        self.data = file_reader().setup().read()
        logger.debug(self.data)
        return self

    def _read_section(self, section_name: TAnyStr, env_merge: TBool = False):
        """
        Читает секцию с переменными.

        Так как не для всех секций необходимо слияние значений
        переменных из файла и значения переменных окружения, то
        используем флаг `env_merge`. Он указывает на логику обработки
        значений которые будут храниться в прочитанной секции.

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

    def version(self) -> TAnyStr:
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
    def _section_how_dataclass(cls_name: TAnyStr, fields) -> TDataClass:
        cls = make_dataclass(cls_name, fields=fields, eq=False)
        return cls(**fields)

    def bot(self) -> TDataClass:
        """
        Отдаем `dataclass`, а не словарь, так как
        получившийся код будет чище, в разделе
        настройки модуля `app.setup`.

        :return: dataclass
        """
        if not self._bot:
            section = self._read_section(
                ConfigSections.BOT, env_merge=True
            )
            self._bot = self._section_how_dataclass(
                ConfigSections.BOT, section)

        return self._bot

    def logging(self) -> TDict:
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

    def i18n(self) -> TDataClass:
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

    def database(self) -> TDataClass:
        """
        Отдаем `dataclass`, а не словарь, так как
        получившийся код будет чище, в разделе
        настройки модуля `app.setup`.

        :return: dataclass
        """
        if not self._database:
            section = self._read_section(
                ConfigSections.DATABASE, env_merge=True
            )
            self._database = self._section_how_dataclass(
                ConfigSections.DATABASE, section)

        return self._database

    def new_gamer(self) -> TDataClass:
        """
        Отдаем `dataclass`, а не словарь, так как
        получившийся код будет чище, в разделе
        настройки модуля `app.setup`.

        :return: dataclass
        """
        if not self._new_gamer:
            section = self._read_section(
                ConfigSections.NEW_GAMER, env_merge=True
            )
            self._new_gamer = self._section_how_dataclass(
                ConfigSections.NEW_GAMER, section)

        return self._new_gamer
