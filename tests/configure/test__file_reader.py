# coding: utf-8

import os
import pytest
from app.configure import reader
from app.configure.file_reader import BaseFileReader
from app.configure.file_reader import YAMLFileReader

ENV_NAME_OF_CONFIG_PATH = 'CONFIG_PATH'
ENV_NAME_OF_ENVIRONMENT = 'ENV'
DEFAULT_ENVIRONMENT = 'develop'
DEFAULT_CONFIG_PATH = '/etc/app'
DEFAULT_CONFIG_NAME = 'app.yaml'
environs = {}


def get_etc_dir():
    module_dir = os.path.dirname(__file__)
    test_dir = os.path.dirname(module_dir)
    root_dir = os.path.dirname(test_dir)
    prefix = os.path.join(root_dir, 'etc')
    return os.path.join(prefix, 'app')


def fake_get_from_environ(environ_name):
    return environs.get(environ_name)


@pytest.mark.unit
class TestBaseFileReader:
    @pytest.mark.parametrize(
        'variable_name, variable_value',
        (
            ('ENV_NAME_OF_CONFIG_PATH', ENV_NAME_OF_CONFIG_PATH),
            ('ENV_NAME_OF_ENVIRONMENT', ENV_NAME_OF_ENVIRONMENT),
            ('DEFAULT_ENVIRONMENT', DEFAULT_ENVIRONMENT),
            ('DEFAULT_CONFIG_PATH', DEFAULT_CONFIG_PATH),
            ('DEFAULT_CONFIG_NAME', DEFAULT_CONFIG_NAME)
        )
    )
    def test__default_variables(self, variable_name, variable_value):
        assert hasattr(BaseFileReader, variable_name)
        assert getattr(BaseFileReader, variable_name) == variable_value

    def test__read_is_not_implemented(self):
        with pytest.raises(NotImplementedError):
            BaseFileReader().setup().read()

    def test__search_config_path_default(self, monkeypatch):
        monkeypatch.delenv(BaseFileReader.ENV_NAME_OF_CONFIG_PATH)
        default_config_path = os.path.join(
            DEFAULT_CONFIG_PATH, DEFAULT_CONFIG_NAME
        )

        file_reader = BaseFileReader()
        file_reader.search_config_path()
        assert file_reader.config_path == default_config_path

    def test__search_config_path_custom(self, monkeypatch):
        ANSWER = '/foo/bar/baz.yaml'
        monkeypatch.setenv(BaseFileReader.ENV_NAME_OF_CONFIG_PATH, ANSWER)

        file_reader = BaseFileReader()
        file_reader.search_config_path()
        assert file_reader.config_path == ANSWER

    def test__search_environment_default(self, monkeypatch):
        monkeypatch.delenv(BaseFileReader.ENV_NAME_OF_ENVIRONMENT)

        file_reader = BaseFileReader()
        file_reader.search_environment()
        assert file_reader.environment == BaseFileReader.DEFAULT_ENVIRONMENT

    def test__search_environment_custom(self, monkeypatch):
        ANSWER = 'env'
        monkeypatch.setenv(BaseFileReader.ENV_NAME_OF_ENVIRONMENT, ANSWER)

        file_reader = BaseFileReader()
        file_reader.search_environment()
        assert file_reader.environment == ANSWER


@pytest.mark.unit
class TestYAMLFileReader:
    def test__read(self, monkeypatch):
        config_path = os.path.join(get_etc_dir(), 'app.yaml')

        monkeypatch.setitem(
            environs,
            ENV_NAME_OF_CONFIG_PATH,
            config_path
        )
        monkeypatch.setattr(
            reader,
            'get_from_environ',
            fake_get_from_environ
        )

        yaml_file_reader = YAMLFileReader()
        result = yaml_file_reader.setup().read()

        assert isinstance(result, dict)
