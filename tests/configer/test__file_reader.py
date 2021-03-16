# coding: utf-8

import os
import pytest
from app.configer import reader
from app.configer import BaseFileReader
from app.configer import YAMLFileReader

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

    def test_init_default_reader(self, monkeypatch):
        monkeypatch.setattr(
            reader,
            'get_from_environ',
            fake_get_from_environ
        )

        file_reader = BaseFileReader()
        assert file_reader.environment == DEFAULT_ENVIRONMENT

        default_config_path = os.path.join(
            DEFAULT_CONFIG_PATH,
            DEFAULT_CONFIG_NAME)
        assert file_reader.config_path == default_config_path

    def test_init_custom_reader(self, monkeypatch):
        env = 'env'
        config_path = 'config_path'
        monkeypatch.setitem(
            environs,
            ENV_NAME_OF_ENVIRONMENT,
            env
        )
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

        file_reader = BaseFileReader()
        assert file_reader.environment == env
        assert file_reader.config_path == config_path

    def test__method_read_is_not_create(self):
        file_reader = BaseFileReader()
        with pytest.raises(NotImplementedError):
            file_reader.read()


@pytest.mark.unit
class TestYAMLFileReader:
    def test__method_read(self, monkeypatch):
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
        result = yaml_file_reader.read()

        assert isinstance(result, dict)
