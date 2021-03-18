# coding: utf8

import emoji


def emojize(text, use_aliases=True):
    return emoji.emojize(str(text), use_aliases=use_aliases)


def demojize(text, use_aliases=True):
    return emoji.demojize(text, use_aliases=use_aliases)
