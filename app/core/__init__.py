# coding: utf8

from logging import getLogger
from app.core import depot
from app.core import dispatcher
from app.core import stations


getLogger('app.core')

__all__ = [
    depot,
    dispatcher,
    stations
]
