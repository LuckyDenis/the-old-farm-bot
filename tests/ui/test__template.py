# coding: utf8

import pytest
from app.ui.templates import BaseMessage


@pytest.mark.unit
class TestBaseMessage:
    def test__rendering(self):
        with pytest.raises(NotImplementedError):
            BaseMessage.rendering()
