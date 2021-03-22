# coding: utf8

from dataclasses import dataclass, field


@dataclass()
class Train:
    unique_id: str
    chat_id: int
    destination: str
    storage: dict
    answers: list = field(init=False)
    has_fail: bool = field(default=False)
    visited: list = field(init=False)

    def __post_init__(self):
        self.answers = list()
        self.visited = list()
