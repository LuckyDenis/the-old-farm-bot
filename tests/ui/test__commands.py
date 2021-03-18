# coding: utf8

import pytest
from app.ui.commands import Commands
from app.ui.commands import BaseCmd


ATTR_UI = 'ui'
ATTR_UI_TYPE = str
ATTR_ENDPOINT = 'endpoint'
ATTR_ENDPOINT_TYPE = str


@pytest.mark.unit
class TestCommands:
    @pytest.mark.parametrize(
        'cmd',
        (
            'Start',
            'Help'
        )
    )
    def test__availability_of_command(self, cmd):
        assert hasattr(Commands, cmd)


@pytest.mark.unit
class TestBaseCmd:
    @pytest.mark.parametrize(
        ('attr', 'attr_type'),
        (
            (ATTR_UI, ATTR_UI_TYPE),
            (ATTR_ENDPOINT, ATTR_ENDPOINT_TYPE)
        )
    )
    def test__attr(self, attr, attr_type):
        assert hasattr(BaseCmd, attr)
        assert isinstance(getattr(BaseCmd, attr), attr_type)


@pytest.mark.unit
class TestCmd:
    @pytest.mark.parametrize(
        ('cmd', 'attr', 'attr_type'),
        (
            (Commands.Start, ATTR_UI, ATTR_UI_TYPE),
            (Commands.Start, ATTR_ENDPOINT, ATTR_ENDPOINT_TYPE),
            (Commands.Help, ATTR_UI, ATTR_UI_TYPE),
            (Commands.Help, ATTR_UI, ATTR_ENDPOINT_TYPE)
        )
    )
    def test__attr(self, cmd, attr, attr_type):
        assert hasattr(cmd, attr)
        assert isinstance(getattr(cmd, attr), attr_type)
