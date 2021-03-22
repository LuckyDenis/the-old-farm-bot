# coding: utf8

from logging import getLogger
from app.ui import answer
from app.ui import keyboards
from app.ui import i18n
from app.ui import commands
from app.ui import templates


getLogger('app.ui')


__all__ = [
    answer,
    keyboards,
    i18n,
    commands,
    templates
]
