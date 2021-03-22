# coding: utf8

import pytest
from app.core.train import Train


# user_id, chat_id = 2^64
# https://core.telegram.org/bots/api
CHAT_ID = 18446744073709551616
UNIQUE_ID = '18446744073709551616 - 2'
DESTINATION = 'foo'


@pytest.mark.unit
class TestTrain:
    def test__make_train(self):
        train = Train(
            unique_id=UNIQUE_ID,
            chat_id=CHAT_ID,
            destination=DESTINATION,
            storage={}
        )
        assert isinstance(train.answers, list)
        assert len(train.answers) == 0
        assert isinstance(train.visited, list)
        assert len(train.visited) == 0
        assert isinstance(train.has_fail, bool)
        assert train.has_fail is False
