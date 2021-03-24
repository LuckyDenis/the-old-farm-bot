# coding: utf8

import pytest
from app.core import dispatcher as dp


LOCALE = 'en'
CHAT_ID = 123456789
UNIQUE_ID = f'{CHAT_ID}-2'
USER_INFO = {
    'locale': LOCALE,
    'chat_id': CHAT_ID,
    'unique_id': UNIQUE_ID
}


@pytest.fixture()
def train():
    return dp.Train(
        unique_id=UNIQUE_ID,
        chat_id=CHAT_ID,
        destination='test',
        storage={}
    )


@pytest.mark.unit
class TestBaseItinerary:
    async def test__stations(self):
        with pytest.raises(NotImplementedError):
            dp.BaseItinerary._stations()

    def test__prepare_train(self):
        train = dp.BaseItinerary._prepare_train(USER_INFO)
        assert train.unique_id == UNIQUE_ID
        assert train.chat_id == CHAT_ID
        assert train.storage.get('user_info', False)
        assert train.storage['user_info'] == USER_INFO
        assert isinstance(train.answers, list)
        assert len(train.answers) == 0
        assert len(train.visited) == 0
        assert isinstance(train.visited, list)
        assert isinstance(train.has_fail, bool)
        assert train.has_fail is False

    async def test__travel_is_fail(self, train, monkeypatch):
        answer = 'foo'

        async def stopover(tr):
            tr.answers.append(answer)

        monkeypatch.setattr(
            dp.stations.BaseStation,
            'stopover', stopover
        )
        await dp.BaseItinerary._travel_is_fail(train)

        assert train.answers[-1] == answer
        assert train.has_fail is False

    async def test__traveling_correct(self, train, monkeypatch):
        async def stopover(tr):
            tr.visited.append('foo')

        monkeypatch.setattr(
            dp.stations.BaseStation,
            'stopover', stopover
        )
        monkeypatch.setattr(
            dp.BaseItinerary, '_stations',
            lambda *_: [
                dp.stations.BaseStation,
                dp.stations.BaseStation
            ]
        )
        await dp.BaseItinerary._traveling(train)

        assert train.has_fail is False
        assert len(train.visited) == 2

    async def test__traveling_with_error(self, train, monkeypatch):
        async def stopover(tr):
            tr.visited.append('foo')
            tr.has_fail = True

        monkeypatch.setattr(
            dp.stations.BaseStation,
            'stopover', stopover
        )
        monkeypatch.setattr(
            dp.BaseItinerary, '_stations',
            lambda *_: [
                dp.stations.BaseStation,
                dp.stations.BaseStation
            ]
        )
        await dp.BaseItinerary._traveling(train)

        assert train.has_fail is True
        assert len(train.visited) == 1

    async def test__on_itinerary_correct(self, monkeypatch):
        async def _traveling(tr):
            tr.visited.append('foo')

        monkeypatch.setattr(
            dp.BaseItinerary, '_traveling',
            _traveling
        )
        train = await dp.BaseItinerary.on_itinerary(USER_INFO)
        assert len(train.visited) == 1
        assert len(train.answers) == 0

    async def test__on_itinerary_with_error(self, monkeypatch):
        async def _traveling(tr):
            tr.visited.append('foo')
            tr.has_fail = True

        monkeypatch.setattr(
            dp.BaseItinerary, '_traveling',
            _traveling
        )

        async def _travel_is_fail(tr):
            tr.answers.append('foo')

        monkeypatch.setattr(
            dp.BaseItinerary, '_travel_is_fail',
            _travel_is_fail
        )

        train = await dp.BaseItinerary.on_itinerary(USER_INFO)
        assert len(train.visited) == 1
        assert len(train.answers) == 1
