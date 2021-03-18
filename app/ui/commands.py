# coding: utf8
from dataclasses import dataclass
from typing import AnyStr


@dataclass
class BaseCmd:
    ui: AnyStr = 'ui'
    endpoint: AnyStr = 'endpoint'


@dataclass
class Commands:
    """
    Команды пользователя.

    Так как команды для пользователя и для обработчик
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
