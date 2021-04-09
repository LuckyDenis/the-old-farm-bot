# coding: utf8

from logging import getLogger

from gino import Gino
from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import func

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

# todo: *_cost || *_price


class CategoryOfGameItem(db.Model):
    __tablename__ = 'category_of_game_item'
    __table_args__ = (
        {'schema': 'component'}
    )

    id = Column(
        String(16),
        primary_key=True,
        autoincrement=False
    )


class GameCurrency(db.Model):
    __tablename__ = 'game_currency'
    __table_args__ = (
        {'schema': 'component'}
    )

    id = Column(
        String(4),
        primary_key=True,
        autoincrement=False
    )


class GameItem(db.Model):
    __tablename__ = 'game_item'
    __table_args__ = (
        CheckConstraint(
            'sell_cost >= 0',
            name='sell_cost_cannot_be_negative'
        ),
        {'schema': 'component'}
    )

    id = Column(
        String(32),
        primary_key=True,
        autoincrement=False,
        index=True
    )
    category = Column(
        String(16),
        ForeignKey(
            CategoryOfGameItem.id,
            ondelete='RESTRICT',
            onupdate='CASCADE',
            use_alter=True
        ),
        nullable=False
    )
    sell_cost = Column(
        Integer(),
        default=0
    )
    sell_game_currency = Column(
        String(4),
        ForeignKey(
            GameCurrency.id,
            ondelete='RESTRICT',
            onupdate='CASCADE',
            use_alter=True
        ),
        nullable=False
    )


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
    is_admin = Column(
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
        DateTime(),
        server_default=func.now(),
        nullable=False
    )
    last_visited = Column(
        DateTime(),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False
    )


class SelectedFarm(db.Model):
    __tablename__ = 'selected_farm'
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
        default=None
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


class Pet(db.Model):
    __tablename__ = 'pet'
    __table_args__ = (
        CheckConstraint(
            'was_grabbed >= 0',
            name='was_grabbed_cannot_be_negative'
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
    moniker = Column(
        String(16),
        default=None
    )
    not_hungry_to_time = Column(
        DateTime(timezone=False),
        default=0
    )
    was_grabbed = Column(
        Integer(),
        default=0
    )


class SelectedShopItem(db.Model):
    __tablename__ = 'selected_shop_item'
    __table_args__ = (
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
    id_object = Column(
        String(32),
        ForeignKey(
            GameItem.id,
            ondelete='RESTRICT',
            onupdate='CASCADE',
            use_alter=True
        ),
        default=None
    )


class Gifts(db.Model):
    __tablename__ = 'gifts'
    __table_args__ = (
        CheckConstraint(
            'id_shelf > 0',
            name='id_shelf_must_be_greater_than_zero'
        ),
        CheckConstraint(
            'quantity >= 0 AND '
            'id_object IS NOT NULL '
            'OR quantity IS NULL',
            name='quantity_must_be_positive_or_not_matter'
        ),
        CheckConstraint(
            'quantity >= 0 AND'
            'id_object IS NOT NULL '
            'OR id_object IS NULL',
            name='id_object_must_have_quantity'
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
        autoincrement=False,
        index=True
    )
    id_shelf = Column(
        Integer(),
        primary_key=True,
        autoincrement=False,
        index=True
    )
    id_object = Column(
        String(32),
        ForeignKey(
            GameItem.id,
            ondelete='RESTRICT',
            onupdate='CASCADE',
            use_alter=True
        ),
        default=None
    )
    quantity = Column(
        Integer(),
        default=None
    )
