# coding: utf8
from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from app.typehint import TAnyStr


@dataclass
class BaseCmd:
    ui: TAnyStr
    endpoint: TAnyStr


@dataclass
class Commands:
    """
    Команды пользователя.

    Так как команды для пользователя и для обработчиков
    взаимосвязаны, и по своей сути являются одной
    сущностью, то для удобной работы и редактирования
    они собраны в одном месте.

    Commands.Cmd.ui:
    Шаблон для генерации команды пользователю,
    в модуле `app.ui.templates`

    Commands.Cmd.endpoint:
    Шаблон для подстановки в обработчики, в
    модуле `app.controllers.handlers`.
    """
    @dataclass
    class Start(BaseCmd):
        ui = '/start'
        endpoint = 'start'

    @dataclass
    class Help(BaseCmd):
        ui = '/help'
        endpoint = 'help'

    @dataclass
    class Bug(BaseCmd):
        ui = '/bug'
        endpoint = 'bug'
