# coding: utf8
from logging import getLogger
from app.ui.i18n import I18N
from app.ui.utils import emojize

logger = getLogger('app.ui.templates')


i18n = I18N()
_ = i18n.gettext_lazy


class BaseTemplate:
    @classmethod
    def rendering(cls, state=None):
        logger.debug(f'state: {state}, '
                     f'locale: {i18n.ctx_locale.get()}')
        try:
            i18n.set_locale(state['locale'])
            return cls._rendering(state=state)
        except KeyError as e:
            logger.error(
                f'error: {e}, '
                f'locale: {i18n.ctx_locale.get()}, '
                f'state: {state}')

    @classmethod
    def _rendering(cls, state=None):
        raise NotImplementedError()


class SystemException(BaseTemplate):
    @classmethod
    def _rendering(cls, state=None):
        format_data = {
            **state
        }
        template = _(":teddy_bear: [ <b>Teddy</b> ]\n"
                     "Hello!"
                     ).format(**format_data)

        return emojize(template)


# ---------- cmd: start ---------- #
class NewUser(BaseTemplate):
    @classmethod
    def _rendering(cls, state=None):
        format_data = {
            **state
        }

        template = _(":teddy_bear: [ <b>Teddy</b> ]\n"
                     "Hello, {unique_id}!"
                     ).format(**format_data)

        return emojize(template)
