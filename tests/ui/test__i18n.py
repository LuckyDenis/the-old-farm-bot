# coding: utf8

import os
import contextvars

import gettext
import pytest

from os.path import exists
from os.path import join
from os.path import dirname
from app.ui.i18n import I18N, I18NMeta

LC_PATH = join(dirname(__file__), 'locales')
LC_DOMAIN = 'text'


class Translator:
    def __init__(self, *_):
        pass

    @staticmethod
    def gettext(singular):
        return singular

    @staticmethod
    def ngettext(singular, plural, n):
        if n == 1 or plural is None:
            return singular
        return plural


@pytest.fixture()
def mock_translation(monkeypatch):
    monkeypatch.setattr(
        gettext, 'GNUTranslations',
        Translator
    )


@pytest.mark.unit
class TestI18N:
    @staticmethod
    def create_i18n(default_local=None):
        I18NMeta._instance = False
        i18n = I18N()
        i18n.path = LC_PATH
        i18n.domain = LC_DOMAIN

        if default_local:
            i18n.default_locale = default_local

        return i18n

    def test__create_once(self):
        i18n_a = I18N()
        i18n_b = I18N()
        assert id(i18n_a) == id(i18n_b)

    def test__set_default_local(self):
        i18n = self.create_i18n()
        default_local = 'en'
        i18n._set_default_local(default_local)
        ctx_user_locale = i18n.ctx_locale.get()
        assert ctx_user_locale == default_local

    def test__call__(self, monkeypatch):
        ANSWER = 'foo'
        monkeypatch.setattr(
            I18N, 'gettext',
            lambda *_: ANSWER
        )
        i18n = self.create_i18n()
        result = i18n(ANSWER)
        assert result == ANSWER

    def test_set_locale(self):
        """
        Тестируется изменения в разных контекстах.
        """
        default_locale = 'en'
        new_locale = 'ru'
        i18n = self.create_i18n(default_locale)

        inside_ctx = default_locale

        def change_ctx():
            nonlocal inside_ctx
            i18n.set_locale(new_locale)
            inside_ctx = i18n.ctx_locale.get()

        ctx = contextvars.copy_context()
        ctx.run(change_ctx)

        assert i18n.ctx_locale.get() == default_locale
        assert inside_ctx == new_locale

    def test__reload(self, monkeypatch):
        monkeypatch.setattr(
            I18N, 'find_locales',
            lambda *_: answer
        )

        i18n = self.create_i18n()
        answer = {'FOO': 'foo'}

        i18n.reload()
        locales = i18n.locales
        i18n.locales.clear()

        assert locales == answer

    def test__gettext_lazy(self):
        answer = 'foo'
        i18n = self.create_i18n()
        assert i18n.gettext_lazy(answer) == answer

    @pytest.mark.parametrize(
        ('locale', 'singular', 'plural', 'n', 'answer'),
        (
                ('FOO', 'dog', 'dogs', 1, 'dog'),
                ('FOO', 'cat', 'cats', 2, 'cats')
        )
    )
    def test__gettext_locale_not_in_locales(
            self, locale, singular, plural, n, answer, monkeypatch):
        i18n = self.create_i18n()
        monkeypatch.setitem(i18n.locales, 'BAR', Translator)
        result = i18n.gettext(
            singular, plural, n, locale=locale)
        assert result == answer

    @pytest.mark.parametrize(
        ('locale', 'singular', 'plural', 'n', 'answer'),
        (
                ('FOO', 'dog', 'dogs', 1, 'dog'),
                ('FOO', 'cat', None, 1, 'cat'),
                ('FOO', 'horse', 'horses', 2, 'horses')
        )
    )
    def test__gettext_locale_in_locales(
            self, locale, singular, plural, n, answer, monkeypatch):
        i18n = self.create_i18n()
        monkeypatch.setitem(i18n.locales, 'FOO', Translator)
        result = i18n.gettext(
            singular, plural, n, locale=locale)
        assert result == answer

    @pytest.mark.skipif(
        exists(join(LC_PATH, 'en')) is False,
        reason='Необходимо использовать `make test`.')
    def test__find_compiled_locales(self, monkeypatch):
        monkeypatch.setattr(
            os, 'listdir',
            lambda *_: ['en']
        )

        i18n = self.create_i18n()
        locales = i18n.find_locales()

        assert isinstance(locales, dict)
        assert 'en' in locales

    @pytest.mark.skipif(
        exists(join(LC_PATH, 'ru')) is False,
        reason='Необходимо использовать `make test`.')
    def test__find_not_compiled_locales(self, monkeypatch):
        monkeypatch.setattr(
            os, 'listdir',
            lambda *_: ['ru']
        )

        i18n = self.create_i18n()
        with pytest.raises(RuntimeError):
            i18n.find_locales()

    def test__skip_file_is_not_locales(self, monkeypatch):
        monkeypatch.setattr(
            os, 'listdir',
            lambda *_: ['text.py']
        )

        i18n = self.create_i18n()
        locales = i18n.find_locales()

        assert isinstance(locales, dict)
        assert len(locales) == 0
