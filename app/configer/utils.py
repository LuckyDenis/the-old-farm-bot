# coding: utf8

import os
from typing import AnyStr


def get_from_environ(environ_name) -> AnyStr:
    return os.environ.get(str(environ_name))
