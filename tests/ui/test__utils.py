# coding: utf8

import pytest
from app.ui.utils import emojize
from app.ui.utils import demojize


@pytest.mark.unit
class TestEmojiInterface:
    SMILE_TEXT = ':relaxed:'
    SMILE_CODE = u'\U0000263A'

    def test__emojize(self):
        assert emojize(self.SMILE_TEXT) == self.SMILE_CODE

    def test__demojize(self):
        assert demojize(self.SMILE_CODE) == self.SMILE_TEXT
