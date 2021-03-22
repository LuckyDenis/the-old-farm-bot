# coding: utf8

from dataclasses import dataclass


@dataclass()
class Train:
    unique_id: str
    chat_id: int
    destination: str
    answers: list
    has_fail: bool
    storage: dict
