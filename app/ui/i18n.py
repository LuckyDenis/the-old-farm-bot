# coding: utf8
"""
Шаг 1: Извлекаем текст
    $ pybabel extract --input-dirs=./app/ui/locales -o ./app/ui/locales/app.pot

    Опции:
     * Извлечение текстов с поддержкой плюрализации
     -k __:1,2

     * Добавить комментарии для переводчиков
     -add-comments=Note

     * Установить имя проекта
     --project=my_app

     * Установить версию
     --version=1.2

Шаг 2: Создание *.po файлов. Например для en, ru языков
    $ pybabel init -i ./app/ui/locales/app.pot -d locales -D app -l en
    $ pybabel init -i ./app/ui/locales/app.pot -d locales -D app -l ru

Шаг 3: Перевести тексты расположенные в locales/{language}/LC_MESSAGES/app.po

Шаг 4: Компилируем перевод
    $ pybabel compile -d ./app/ui/locales -D app

Шаг 5: При внесении изменений кода, нужно обновить файлы *.po и *.mo.
    Шаг 5.1: регенерировать файл *.pot:
        Шаг 1
    Шаг 5.2: Обновить *.po файлы
        $ pybabel update -d ./app/ui/locales -D app -i ./app/ui/locales/app.pot
    Шаг 5.3: Обновить перевод
        расположение вы знаете из шага 3
    Шаг 5.4: Скомпилировать *.mo файлы
        Шаг 4

"""
from __future__ import annotations
from typing import TYPE_CHECKING

from logging import getLogger
import gettext
import os
from contextvars import ContextVar

from babel.support import LazyProxy

if TYPE_CHECKING:
    from app.typehint import TContextVar
    from app.typehint import TAnyStr
    from app.typehint import TI18N
    from app.typehint import TDict


logger = getLogger('app.ui.i18n')


class I18NMeta(type):
    """
    Паттерн `Одиночка`, для класса I18N.

    Необходим, что бы выполнить настройку
    при старте в единой точке настройки
    `app.setup`, и не импортировать на
    прямую в модуль `ConfigReader`.
    """
    instance: TI18N = None

    def __call__(cls, *args, **kwargs) -> TI18N:
        if not cls.instance:
            instance = super().__call__(*args, **kwargs)
            cls.instance = instance
        return cls.instance


class I18N(metaclass=I18NMeta):
    ctx_locale: TContextVar = ContextVar(
        'ctx_user_locale', default='en')

    def __init__(self, path=None, domain=None, default_locale=None):
        self.path = path
        self.domain = domain
        self.locales = dict()
        self._set_default_local(default_locale)

    def setup(self, path=None, domain=None, default_locale=None):
        logger.debug(f'path: {path}, domain: {domain}, '
                     f'default_locale: {default_locale}')

        self.__init__(path, domain, default_locale)
        self.reload()
        return self

    @classmethod
    def _set_default_local(cls, default_local: TAnyStr):
        """
        Устанавливает глобальное значение языка.
        :param default_local: str
        """
        cls.ctx_locale.set(default_local)

    def reload(self):
        self.locales = self.find_locales()
        return self

    def set_locale(self, language: TAnyStr):
        """
        Устанавливает для конкретного пользователя
        значения языка.

        :param language: str
        """
        self.ctx_locale.set(language)

    def find_locales(self) -> TDict:
        translations = dict()

        for name in os.listdir(self.path):
            if not os.path.isdir(os.path.join(self.path, name)):
                continue
            mo_path = os.path.join(
                self.path, name, 'LC_MESSAGES', self.domain + '.mo')

            if os.path.exists(mo_path):
                with open(mo_path, "rb") as fp:
                    translations[name] = gettext.GNUTranslations(fp)

            elif os.path.exists(mo_path[:-2] + "po"):
                logger.warning(f"Найден язык '{name}, "
                               f"но этот язык не скомпилирован. "
                               f"Подробней в docstring модуля "
                               f"`app.ui.i18n`.")

        logger.log(60, f'Найденные переводы: {translations.keys()}')
        return translations

    def gettext(self, singular, plural=None, n=1, locale=None):
        if locale is None:
            locale = self.ctx_locale.get()

        if locale not in self.locales:
            if n == 1:
                return singular
            return plural

        translator = self.locales[locale]

        if plural is None:
            return translator.gettext(singular)
        return translator.ngettext(singular, plural, n)

    def gettext_lazy(
            self, singular, plural=None, n=1,
            locale=None, enable_cache=True):
        return LazyProxy(
            self.gettext, singular, plural, n,
            locale, enable_cache=enable_cache)

    def __call__(self, singular, plural=None, n=1, locale=None) -> TAnyStr:
        logger.debug(
            f'(singular: {singular}, plural: {plural}, n: {n}, locale: {locale})')
        return self.gettext(singular, plural, n, locale)
