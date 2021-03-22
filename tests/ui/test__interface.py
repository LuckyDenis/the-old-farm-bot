# coding: utf8

import pytest
from app.ui import interface as ui
from app.core.train import Train


@pytest.fixture()
def train():
    return Train(
        unique_id='123456789-0',
        chat_id=123456789,
        destination='test',
        storage={'FOO': 'foo'}
    )


@pytest.mark.unit
class TestBaseInterface:
    def test__generate(self, train, monkeypatch):
        answer = 'foo'
        monkeypatch.setattr(
            ui.BaseInterface, '_generate',
            lambda *_: answer
        )

        ui.BaseInterface.generate({}, train)
        assert len(train.answers) == 1
        assert train.answers[-1] == answer

    def test__logger_error_message(self, train, monkeypatch):
        monkeypatch.setattr(
            ui.BaseInterface, '_generate',
            lambda cls, answer_info: ValueError()
        )

        logger_error_msg = [False]

        def logger_error_hdl(*_, **__):
            logger_error_msg[0] = True

        monkeypatch.setattr(
            ui.logger, 'error',
            logger_error_hdl
        )

        ui.BaseInterface.generate({}, train)
        assert train.has_fail is True
        assert logger_error_msg[0] is True

    def test__sub_generate(self, train):
        with pytest.raises(NotImplementedError):
            ui.BaseInterface.generate({}, train)


@pytest.mark.skip(reason='Еще не реализован шаблон.')
@pytest.mark.unit
class TestSystemException:
    def test__sub_generate(self):
        ui.SystemException._generate(answer_info={
            'unique_id': '123456789-2'
        })


@pytest.mark.skip(reason='Еще не реализован шаблон.')
@pytest.mark.unit
class TestNewUser:
    def test__sub_generate(self):
        ui.NewUser._generate(answer_info={
            'unique_id': '123456789-2'
        })
