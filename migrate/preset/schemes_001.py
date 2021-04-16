# coding: utf8
"""
Импортировать в первый commit в базу.

def upgrade():
    add_schemes(op)
    ...

def downgrade():
    ...
    del_schemes(op)
"""

from sqlalchemy.schema import CreateSchema
from sqlalchemy.schema import DropSchema


def add_schemes(op):
    op.execute(CreateSchema('gamer'))
    op.execute(CreateSchema('elements'))
    op.execute(CreateSchema('shop'))
    op.execute(CreateSchema('donation'))
    op.execute(CreateSchema('farm'))
    op.execute(CreateSchema('quest'))


def del_schemes(op):
    op.execute(DropSchema('gamer'))
    op.execute(DropSchema('elements'))
    op.execute(DropSchema('shop'))
    op.execute(DropSchema('donation'))
    op.execute(DropSchema('farm'))
    op.execute(DropSchema('quest'))
