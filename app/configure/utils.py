# coding: utf8

import os


def get_from_environ(environ_name):
    return os.environ.get(str(environ_name))
