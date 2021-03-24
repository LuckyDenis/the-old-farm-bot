# coding: utf8

import pytest
from dataclasses import is_dataclass
from app.configure.reader import ConfigReader
from app.configure.reader import ConfigSections
from app.configure.file_reader import BaseFileReader
from app.configure.file_reader import YAMLFileReader

FAKE_SECTION_NAME = 'fake'

DATA = {
    'VERSION': '1',
    ConfigSections.LOGGING: {
        'FOO': 'foo'
    },
    ConfigSections.AIOGRAM: {
        'FOO': 'foo'
    },
    ConfigSections.I18N: {
        'FOO': 'foo'
    },
    FAKE_SECTION_NAME: {
        'FOO': 'foo',
        'BAZ': 'foo'
    }
}


class CustomFileReader(BaseFileReader):
    def read(self):
        return DATA


def read():
    return DATA


class CustomNotCorrect:
    pass


@pytest.mark.unit
class TestConfigSections:
    @pytest.mark.parametrize(
        'section_name',
        (
            'AIOGRAM', 'LOGGING', 'I18N', 'VERSION'
        )
    )
    def test__has_section_name(self, section_name):
        assert hasattr(ConfigSections, section_name)


@pytest.mark.unit
class TestConfigReader:
    def test__file_reader_sub_cls_base_file_reader(self):
        # bug: https://youtrack.jetbrains.com/issue/PY-43688
        assert issubclass(ConfigReader.FILE_READER, BaseFileReader)

    def test__file_reader_is_default(self):
        # bug: https://youtrack.jetbrains.com/issue/PY-43688
        assert issubclass(ConfigReader.FILE_READER, YAMLFileReader)

    def test__setup_return_self(self):
        config_reader = ConfigReader()
        assert config_reader.setup() is config_reader

    def test__setup_use_custom_file_reader(self):
        config_reader = ConfigReader()
        config_reader.FILE_READER = CustomFileReader
        config_reader.setup()

        assert config_reader.data == DATA

    def test__setup_use_is_not_correct_file_reader(self):
        config_reader = ConfigReader()
        config_reader.FILE_READER = CustomNotCorrect

        with pytest.raises(TypeError):
            config_reader.setup()

    @staticmethod
    def create_config_reader() -> ConfigReader:
        config_reader = ConfigReader()
        config_reader.data = DATA
        return config_reader

    def test__get_config_version(self):
        config_reader = self.create_config_reader()
        assert config_reader.version() == DATA['VERSION']

    @pytest.mark.parametrize(
        ('env_merge_value', 'variable', 'variable_value'),
        (
            (False, 'BAZ', 'BAZ'),
            (True, 'BAZ', 'baz')
        )
    )
    def test__read_section(
            self, monkeypatch, env_merge_value, variable, variable_value):

        config_reader = self.create_config_reader()
        monkeypatch.setenv('BAZ', 'baz')
        config_reader.data = {
            'fake': {
                'BAZ': 'BAZ'
            }
        }

        section_variables = config_reader._read_section(
            'fake', env_merge=env_merge_value
        )
        assert section_variables[variable] == variable_value

    def test__section_how_dataclass(self):
        config_reader = self.create_config_reader()
        section_cls = config_reader._section_how_dataclass(
            FAKE_SECTION_NAME, DATA[FAKE_SECTION_NAME]
        )
        assert is_dataclass(section_cls)

    def test__create_logging(self):
        config_reader = self.create_config_reader()

        logging_section = config_reader.logging()
        assert isinstance(logging_section, dict)
        assert logging_section == DATA[ConfigSections.LOGGING]

    def test__logging_once_create(self):
        config_reader = self.create_config_reader()

        logging_section_a = config_reader.logging()
        logging_section_b = config_reader.logging()
        assert id(logging_section_a) == id(logging_section_b)

    def test__create_aiogram(self):
        config_reader = self.create_config_reader()

        aiogram_section = config_reader.aiogram()
        assert is_dataclass(aiogram_section)
        assert aiogram_section.FOO == DATA[ConfigSections.AIOGRAM]['FOO']

    def test__aiogram_once_create(self):
        config_reader = self.create_config_reader()

        aiogram_section_a = config_reader.aiogram()
        aiogram_section_b = config_reader.aiogram()

        assert id(aiogram_section_a) == id(aiogram_section_b)

    def test__create_i18n(self):
        config_reader = self.create_config_reader()

        i18n_section = config_reader.i18n()
        assert is_dataclass(i18n_section)
        assert i18n_section.FOO == DATA[ConfigSections.I18N]['FOO']

    def test__i18n_once_create(self):
        config_reader = self.create_config_reader()

        i18n_section_a = config_reader.i18n()
        i18n_section_b = config_reader.i18n()

        assert id(i18n_section_a) == id(i18n_section_b)
