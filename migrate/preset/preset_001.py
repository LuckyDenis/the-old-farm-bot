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
    op.execute(CreateSchema('profile'))
    op.execute(CreateSchema('component'))


def del_schemes(op):
    op.execute(DropSchema('profile'))
    op.execute(DropSchema('component'))
