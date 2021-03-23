# coding: utf8

import pytest
from app.ui.commands import Commands


ATTR_UI = 'ui'
ATTR_UI_TYPE = str
ATTR_ENDPOINT = 'endpoint'
ATTR_ENDPOINT_TYPE = str

CMD_LIST = (
    Commands.Start,
    Commands.Help,
    Commands.Bug
)


@pytest.mark.unit
class TestCmd:
    @pytest.mark.parametrize(
        'cmd',
        CMD_LIST
    )
    def test__attr_ui(self, cmd):
        assert hasattr(cmd, ATTR_UI)
        assert isinstance(getattr(cmd, ATTR_UI), ATTR_UI_TYPE)

    @pytest.mark.parametrize(
        'cmd',
        CMD_LIST
    )
    def test__attr_endpoint(self, cmd):
        assert hasattr(cmd, ATTR_ENDPOINT)
        assert isinstance(getattr(cmd, ATTR_ENDPOINT), ATTR_ENDPOINT_TYPE)
