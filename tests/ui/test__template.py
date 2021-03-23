# coding: utf8

import pytest
from app.ui import templates as t


@pytest.mark.unit
class TestBaseTemplate:
    def test__sub_rendering(self):
        with pytest.raises(NotImplementedError):
            t.BaseTemplate._rendering({})

    def test__rendering_not_locale(self, monkeypatch):
        logger_error_msg = [False]

        def check_logger_msg(*_):
            logger_error_msg[0] = True

        monkeypatch.setattr(
            t.logger, 'error',
            check_logger_msg
        )
        t.BaseTemplate.rendering(state={})
        assert logger_error_msg[0] is True

    def test__rendering(self):
        with pytest.raises(NotImplementedError):
            t.BaseTemplate.rendering(state={'locale': 'en'})


@pytest.mark.skip(reason='Тестовый шаблон, нечего тестировать.')
@pytest.mark.unit
class TestSystemException:
    def test__sub_rendering(self):
        t.SystemException._rendering(state={
            'unique_id': '123456789-2'
        })


@pytest.mark.skip(reason='Тестовый шаблон, нечего тестировать.')
@pytest.mark.unit
class TestNewUser:
    def test__sub_rendering(self):
        t.NewUser._rendering(state={
            'unique_id': '123456789-2'
        })
