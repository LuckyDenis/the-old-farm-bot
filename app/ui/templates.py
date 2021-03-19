# coding: utf8
from .i18n import I18N
from .utils import emojize

i18n = I18N()
_ = i18n.gettext_lazy


class BaseMessage:
    @staticmethod
    def rendering(states=None):
        raise NotImplementedError()


class SystemException(BaseMessage):
    @staticmethod
    def rendering(states=None):
        format_data = {
            **states
        }

        template = _(":teddy_bear: [ <b>Teddy</b> ]\n"
                     "Hello!"
                     ).format(**format_data)

        return emojize(template)
