# coding: utf8
from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import dataclass, field


if TYPE_CHECKING:
    from app.typehint import TDict
    from app.typehint import TAnyStr
    from app.typehint import TBool
    from app.typehint import TInt
    from app.typehint import TAnswers
    from app.typehint import TVisited


@dataclass()
class Train:
    """
    Обертка для запроса пользователя. В которой хранится
    необходимая информация о запросе, данные, и ответы.
    """
    unique_id: TAnyStr
    chat_id: TInt
    destination: TAnyStr
    storage: TDict
    answers: TAnswers = field(init=False)
    has_fail: TBool = field(default=False)
    visited: TVisited = field(init=False)

    def __post_init__(self):
        self.answers: TAnswers = list()
        self.visited: TVisited = list()
