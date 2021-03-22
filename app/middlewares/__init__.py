# coding: utf8

from logging import getLogger
from app.middlewares.unique_id import UniqueIdMiddleware


getLogger('app.middleware')


__all__ = [
    UniqueIdMiddleware
]
