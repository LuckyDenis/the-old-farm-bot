# coding: utf8

import pytest
from app.configer.reader import ConfigReader
from app.configer.file_reader import BaseFileReader
from app.configer.file_reader import YAMLFileReader

DATA = {
    'VERSION': '1',
    'logging': {
        'FOO': 'foo'
    },
    'aiogram': {
        'FOO': 'foo'
    },
    'fake': {
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
class TestConfigReader:
    def test__file_reader_sub_cls_base_file_reader(self):
        assert isinstance(ConfigReader.FILE_READER(), BaseFileReader)

    def test__file_reader_is_default(self):
        assert isinstance(ConfigReader.FILE_READER(), YAMLFileReader)

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
    def create_config_reader():
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
    def test__mount_section(
            self, monkeypatch, env_merge_value, variable, variable_value):

        config_reader = self.create_config_reader()
        monkeypatch.setenv('BAZ', 'baz')
        config_reader.data = {
            'fake': {
                'BAZ': 'BAZ'
            }
        }

        section_variables = config_reader.mount_section(
            'fake', env_merge=env_merge_value
        )
        assert section_variables[variable] == variable_value

    def test__create_logging(self):
        config_reader = self.create_config_reader()

        cfg_logging = config_reader.logging()
        assert isinstance(cfg_logging, dict)
        assert cfg_logging == DATA['logging']

    def test__logging_once_create(self):
        config_reader = self.create_config_reader()

        cfg_logging_a = config_reader.logging()
        cfg_logging_b = config_reader.logging()
        assert id(cfg_logging_a) == id(cfg_logging_b)

    def test__create_aiogram(self):
        config_reader = self.create_config_reader()

        cfg_aiogram = config_reader.aiogram('FOO')
        assert isinstance(cfg_aiogram, str)
        assert cfg_aiogram == DATA['aiogram']['FOO']

    def test__aiogram_once_create(self):
        config_reader = self.create_config_reader()

        _ = config_reader.aiogram('FOO')
        cfg_aiogram_a = config_reader._aiogram

        _ = config_reader.aiogram('FOO')
        cfg_aiogram_b = config_reader._aiogram

        assert id(cfg_aiogram_a) == id(cfg_aiogram_b)
