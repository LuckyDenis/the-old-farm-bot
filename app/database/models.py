# coding: utf8

from logging import getLogger
from gino import Gino
from sqlalchemy import Column
from sqlalchemy import BigInteger
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import CheckConstraint
from sqlalchemy import ForeignKey
from sqlalchemy import Integer


logger = getLogger('app.database.models')


db = Gino()

convention = {
  'ix': '%(column_0_label)s_idx',
  'uq': '%(table_name)s_%(column_0_name)s_uq',
  'ck': '%(table_name)s_%(constraint_name)s_ck',
  'fk': '%(table_name)s_%(column_0_name)s_%(referred_table_name)s_fk',
  'pk': '%(table_name)s_pk'
}

db.naming_convention = convention


# todo: Подумать как лучше перегрузить метод __repr__


class Gamer(db.Model):
    __tablename__ = 'gamer'
    __table_args__ = (
        CheckConstraint(
            'registered <= last_visited',
            name='last_visited_greater_than_registered'
        ),
        {'schema': 'profile'}
    )

    id = Column(
        BigInteger(),
        primary_key=True,
        nullable=False,
        index=True,
        autoincrement=False
    )
    username = Column(
        String(length=32),
        index=True,
        unique=True
    )

    is_accept_terms = Column(
        Boolean(),
        default=False,
        nullable=False
    )

    is_blocked = Column(
        Boolean(),
        default=False,
        nullable=False
    )

    is_tester = Column(
        Boolean(),
        default=False,
        nullable=False
    )

    registered = Column(
        DateTime(timezone=False),
        server_default=func.now(),
        nullable=False
    )

    last_visited = Column(
        DateTime(timezone=False),
        server_onupdate=func.now(),
        nullable=False
    )


class ChoiceOfFriend(db.Model):
    __tablename__ = 'choice_of_friend'
    __table_args__ = (
        CheckConstraint(
            'id_gamer != id_friend',
            name='id_gamer_not_eq_id_friend'
        ),
        {'schema': 'profile'}
    )

    id_gamer = Column(
        BigInteger(),
        ForeignKey(
            Gamer.id,
            ondelete='CASCADE',
            onupdate='CASCADE',
            use_alter=True
        ),
        primary_key=True,
        index=True,
        unique=True
    )

    id_friend = Column(
        BigInteger(),
        ForeignKey(
            Gamer.id,
            ondelete='DEFAULT',
            onupdate='CASCADE',
            use_alter=True
        ),
        server_default=None
    )


class Purse(db.Model):
    __tablename__ = 'purse'
    __table_args__ = (
        CheckConstraint(
            'coins >= 0',
            name='coins cannot_be_negative'
        ),
        CheckConstraint(
            'gems >= 0',
            name='gems cannot_be_negative'
        ),
        {'schema': 'profile'}
    )

    id_gamer = Column(
        BigInteger(),
        ForeignKey(
            Gamer.id,
            ondelete='CASCADE',
            onupdate='CASCADE',
            use_alter=True
        ),
        primary_key=True,
        index=True
    )

    coins = Column(
        Integer(),
        default=0,
        nullable=False
    )
    gems = Column(
        Integer(),
        default=0,
        nullable=False
    )
