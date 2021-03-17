# coding: utf8

import pytest

from enum import Enum
from app.configer.variables import BaseVariables
from app.configer.variables import AiogramVariables
from app.configer.variables import ConfigVariables


@pytest.mark.unit
class TestBaseVariables:
    def test__subclass_enum(self):
        assert issubclass(BaseVariables, Enum)

    def test__value(self):
        value = 'FOO'

        class Test(BaseVariables):
            FOO = value

        assert str(Test.FOO) == value


@pytest.mark.unit
class TestAiogramVariables:
    def test__subclass_base_variables(self):
        assert issubclass(AiogramVariables, BaseVariables)

    @pytest.mark.parametrize(
        ('name', 'value'),
        (
            ('API_TOKEN', 'API_TOKEN'),
            ('WEBHOOK_HOST', 'WEBHOOK_HOST'),
            ('WEBHOOK_PORT', 'WEBHOOK_PORT'),
            ('WEBHOOK_PATH', 'WEBHOOK_PATH'),
            ('USE_POLLING', 'USE_POLLING'),
            ('PARSE_MOD',  'PARSE_MOD'),
            ('SKIP_UPDATES', 'SKIP_UPDATES'),
            ('CHECK_IP', 'CHECK_IP'),
            ('RETRY_AFTER', 'RETRY_AFTER'),
            ('TIMEOUT', 'TIMEOUT'),
            ('RELAX', 'RELAX'),
            ('FAST', 'FAST')
        )
    )
    def test_variables(self, name, value):
        assert hasattr(AiogramVariables, name)
        assert str(getattr(AiogramVariables, name)) == value


@pytest.mark.unit
class TestConfigVariables:
    def test__subclass_base_variables(self):
        assert issubclass(ConfigVariables, BaseVariables)

    @pytest.mark.parametrize(
        ('name', 'value'),
        (
            ('VERSION', 'VERSION'),
            ('LOGGING', 'logging'),
            ('AIOGRAM', 'aiogram'),
        )
    )
    def test_variables(self, name, value):
        assert hasattr(ConfigVariables, name)
        assert str(getattr(ConfigVariables, name)) == value
