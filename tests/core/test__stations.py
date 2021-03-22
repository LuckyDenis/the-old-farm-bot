# coding: utf8

import pytest
from app.core import stations as st
from app.core.train import Train


UNIQUE_ID = '123456789-0'
CHAT_ID = 123456789
LOCALE = 'en'


@pytest.fixture()
def train():
    return Train(
        unique_id=UNIQUE_ID,
        chat_id=CHAT_ID,
        destination='test',
        storage={'FOO': 'foo'}
    )


@pytest.mark.unit
class TestBaseStation:
    async def test__stopover(self, train, monkeypatch):
        async def _stopover(*_):
            raise KeyError()

        monkeypatch.setattr(
            st.BaseStation, '_stopover', _stopover)

        await st.BaseStation.stopover(train)
        assert train.has_fail is True

    async def test__logger_error(self, train, monkeypatch):
        async def _stopover(*_):
            raise KeyError()

        monkeypatch.setattr(
            st.BaseStation, '_stopover', _stopover)

        logger_error_msg = [False]

        def logger_error_hdl(*_, **__):
            logger_error_msg[0] = True

        monkeypatch.setattr(
            st.logger, 'error', logger_error_hdl)

        await st.BaseStation.stopover(train)

        assert train.has_fail is True
        assert logger_error_msg[0] is True

    async def test__sub_stopover(self, train):
        with pytest.raises(NotImplementedError):
            await st.BaseStation.stopover(train)


@pytest.mark.unit
class TestUISystemException:
    async def test__sub_stopover(self, train, monkeypatch):
        answer = 'foo'
        monkeypatch.setattr(
            st.ui.SystemException, 'generate',
            lambda _, tr: tr.answers.append(answer)
        )
        train.storage['user_info'] = {
            'unique_id': UNIQUE_ID,
            'chat_id': CHAT_ID,
            'locale': LOCALE
        }
        await st.UISystemExceptionSt.stopover(train)

        assert len(train.answers) == 1
        assert train.answers[-1] == answer
