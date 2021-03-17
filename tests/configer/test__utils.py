# coding: utf8

import pytest
from app.configer.utils import get_from_environ


@pytest.mark.unit
class TestUtils:
    def test__get_from_environ(self, monkeypatch):
        variables = 'foo'
        value = 'bar'
        monkeypatch.setenv(variables, value)

        answer = get_from_environ(variables)
        assert answer == value
