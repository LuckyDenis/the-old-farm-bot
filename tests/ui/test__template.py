# coding: utf8

import pytest
from app.ui.templates import BaseTemplate


@pytest.mark.unit
class TestBaseTemplate:
    def test__sub_rendering(self):
        with pytest.raises(NotImplementedError):
            BaseTemplate._rendering()
