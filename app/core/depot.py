# coding: utf8

from typing import AnyStr, List, Collection, Dict
from dataclasses import dataclass


@dataclass()
class Train:
    unique_id: int
    destination: AnyStr
    answers: List[Collection]
    has_fail: bool
    storage: Dict
