# coding: utf8

from logging import getLogger
from app.controllers import handlers
from app.controllers import sender


getLogger('app.controllers')

__all__ = [
    handlers,
    sender
]
