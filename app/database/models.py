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
from sqlalchemy import Index

logger = getLogger('app.database.models')


db = Gino()


class GameItemCategory(db.Model):
    __tablename__ = 'item_category'
    __table_args__ = (
        {'schema': 'game'}
    )

    id = Column(
        String(16),
        primary_key=True,
        autoincrement=False
    )


class GameCurrency(db.Model):
    __tablename__ = 'currency'
    __table_args__ = (
        {'schema': 'game'}
    )

    id = Column(
        String(4),
        primary_key=True,
        autoincrement=False
    )


class GameItem(db.Model):
    __tablename__ = 'item'
    __table_args__ = (
        CheckConstraint(
            'sell_price >= 0',
            name='sell_price_cannot_be_negative'
        ),
        {'schema': 'game'}
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
            GameItemCategory.id,
            ondelete='RESTRICT',
            onupdate='CASCADE',
            use_alter=True
        ),
        nullable=False
    )
    sell_price = Column(
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


class GamePetFood(db.Model):
    __tablename__ = 'pet_food'
    __table_args__ = (
        {'schema': 'game'}
    )

    id_item = Column(
        String(32),
        ForeignKey(
            GameItem.id,
            ondelete='RESTRICT',
            onupdate='CASCADE',
            use_alter=True
        ),
        primary_key=True,
        autoincrement=False,
        unique=True
    )
    saturation = Column(
        Integer(),
        nullable=False
    )


class GameEffect(db.Model):
    __tablename__ = 'effect'
    __table_args__ = (
        CheckConstraint(
            'multiplier != 0',
            name='multiplier_cannot_be_zero'
        ),
        {'schema': 'game'}
    )
    id_item = Column(
        String(32),
        ForeignKey(
            GameItem.id,
            ondelete='RESTRICT',
            onupdate='CASCADE',
            use_alter=True
        ),
        primary_key=True,
        autoincrement=False,
        unique=True
    )

    multiplier = Column(
        Integer(),
        default=1,
        nullable=False
    )

    maker_category = Column(
        String(16),
        ForeignKey(
            GameItemCategory.id,
            ondelete='RESTRICT',
            onupdate='CASCADE',
            use_alter=True
        ),
        nullable=False
    )


class GameRecipe(db.Model):
    __tablename__ = 'recipe'
    __table_args__ = (
        CheckConstraint(
            'quantity > 0',
            name='quantity_greater_than_zero'
        ),
        CheckConstraint(
            'quantity_after_robbery > 0',
            name='quantity_after_robbery_greater_than_zero'
        ),
        {'schema': 'game'}
    )

    maker = Column(
        String(32),
        ForeignKey(
            GameItem.id,
            ondelete='RESTRICT',
            onupdate='CASCADE',
            use_alter=True
        ),
        primary_key=True,
        index=True,
        autoincrement=False,
        unique=True
    )

    product = Column(
        String(32),
        ForeignKey(
            GameItem.id,
            ondelete='RESTRICT',
            onupdate='CASCADE',
            use_alter=True
        )
    )
    quantity = Column(
        Integer(),
        nullable=False
    )

    quantity_after_robbery = Column(
        Integer(),
        nullable=False
    )
    creation_time = Column(
        DateTime(),
        nullable=False
    )
    can_be_robbery = Column(
        Boolean(),
        default=True,
        nullable=False
    )


class GameDestroyMaker(db.Model):
    __tablename__ = 'destroy_maker'
    __table_args__ = (
        CheckConstraint(
            'money_back >= 0',
            name='money_back_cannot_be_negative'
        ),
        {'schema': 'game'}
    )

    id_maker = Column(
        String(32),
        ForeignKey(
            GameRecipe.maker,
            ondelete='RESTRICT',
            onupdate='CASCADE',
            use_alter=True
        ),
        primary_key=True,
        unique=True,
        autoincrement=False
    )
    money_back = Column(
        Integer(),
        nullable=False
    )
    money_back_currency = Column(
        String(4),
        ForeignKey(
            GameCurrency.id,
            ondelete='RESTRICT',
            onupdate='CASCADE',
            use_alter=True
        ),
        nullable=False
    )


class GamerAccount(db.Model):
    __tablename__ = 'account'
    __table_args__ = (
        CheckConstraint(
            'registered <= last_visited',
            name='last_visited_greater_than_registered'
        ),
        {'schema': 'gamer'}
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


class GamerSelectedFarm(db.Model):
    __tablename__ = 'selected_farm'
    __table_args__ = (
        CheckConstraint(
            'id_account != id_friend',
            name='id_gamer_not_eq_id_friend'
        ),
        {'schema': 'gamer'}
    )

    id_account = Column(
        BigInteger(),
        ForeignKey(
            GamerAccount.id,
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
            GamerAccount.id,
            ondelete='DEFAULT',
            onupdate='CASCADE',
            use_alter=True
        ),
        default=None
    )


class GamerPurse(db.Model):
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
        {'schema': 'gamer'}
    )

    id_account = Column(
        BigInteger(),
        ForeignKey(
            GamerAccount.id,
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


class GamerPet(db.Model):
    __tablename__ = 'pet'
    __table_args__ = (
        CheckConstraint(
            'was_grabbed >= 0',
            name='was_grabbed_cannot_be_negative'
        ),
        {'schema': 'gamer'}
    )

    id_gamer = Column(
        BigInteger(),
        ForeignKey(
            GamerAccount.id,
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


class GamerSelectedShopItem(db.Model):
    __tablename__ = 'selected_shop_item'
    __table_args__ = (
        {'schema': 'gamer'}
    )

    id_gamer = Column(
        BigInteger(),
        ForeignKey(
            GamerAccount.id,
            ondelete='CASCADE',
            onupdate='CASCADE',
            use_alter=True
        ),
        primary_key=True,
        index=True,
        unique=True
    )
    id_game_item = Column(
        String(32),
        ForeignKey(
            GameItem.id,
            ondelete='RESTRICT',
            onupdate='CASCADE',
            use_alter=True
        ),
        default=None
    )


class GamerGifts(db.Model):
    __tablename__ = 'gifts'
    __table_args__ = (
        CheckConstraint(
            'id_shelf > 0',
            name='id_shelf_must_be_greater_than_zero'
        ),
        CheckConstraint(
            'quantity >= 0 AND '
            'id_item IS NOT NULL '
            'OR quantity IS NULL',
            name='quantity_must_be_positive_or_not_matter'
        ),
        CheckConstraint(
            'quantity >= 0 AND '
            'id_item IS NOT NULL '
            'OR id_item IS NULL',
            name='id_item_must_have_quantity'
        ),
        {'schema': 'gamer'}
    )
    id_gamer = Column(
        BigInteger(),
        ForeignKey(
            GamerAccount.id,
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
    id_item = Column(
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


class ShopShowcase(db.Model):
    __tablename__ = 'shop_showcase'
    __table_args__ = (
        CheckConstraint(
            'buy_price >= 0',
            name='buy_prices_cannot_be_negative'
        ),
        CheckConstraint(
            'quantity >= 0',
            name='quantity_cannot_be_negative'
        ),
        {'schema': 'shop'}
    )

    id_game_item = Column(
        String(32),
        ForeignKey(
            GameItem.id,
            ondelete='RESTRICT',
            onupdate='CASCADE',
            use_alter=True
        ),
        primary_key=True,
        autoincrement=False,
        index=True
    )
    id_shelf = Column(
        Integer(),
        nullable=False
    )
    quantity = Column(
        Integer(),
        nullable=False
    )
    buy_price = Column(
        Integer(),
        nullable=False
    )
    buy_game_currency = Column(
        String(4),
        ForeignKey(
            GameCurrency.id,
            ondelete='RESTRICT',
            onupdate='CASCADE',
            use_alter=True
        ),
        nullable=False
    )


class FarmWarehouse(db.Model):
    __tablename__ = 'warehouse'
    __table_args__ = (
        CheckConstraint(
            'quantity > 0 AND '
            'id_item IS NOT NULL OR '
            'quantity IS NULL AND '
            'id_item IS NULL ',
            name='valid_quantity_and_id_item'),
        {'schema': 'farm'}
    )
    id_account = Column(
        BigInteger(),
        ForeignKey(
            GamerAccount.id,
            ondelete='CASCADE',
            onupdate='CASCADE',
            use_alter=True
        ),
        primary_key=True,
        autoincrement=False,
        unique=True
    )
    id_shelf = Column(
        Integer(),
        primary_key=True,
        autoincrement=False
    )
    id_item = Column(
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
    is_pick = Column(
        Boolean(),
        default=False,
        nullable=False
    )


class FarmField(db.Model):
    __tablename__ = 'field'
    __table_args__ = (
        Index(
            'field_pk_idx',
            'id_account',
            'id_place'
        ),
        {'schema': 'farm'}
    )

    id_account = Column(
        BigInteger(),
        ForeignKey(
            GamerAccount.id,
            ondelete='CASCADE',
            onupdate='CASCADE',
            use_alter=True
        ),
        primary_key=True,
        autoincrement=True
    )
    id_place = Column(
        Integer(),
        primary_key=True,
        autoincrement=False
    )
    plant = Column(
        String(32),
        ForeignKey(
            GameItem.id,
            ondelete='RESTRICT',
            onupdate='CASCADE',
            use_alter=True
        ),
        default=None
    )
    will_grow = Column(
        DateTime(),
        default=None
    )
    was_fertilized = Column(
        Boolean(),
        default=False
    )
    was_weeded = Column(
        Boolean(),
        default=False
    )
    was_robbed = Column(
        Boolean(),
        default=False
    )


class FarmOrchard(db.Model):
    __tablename__ = 'orchard'
    __table_args__ = (
        Index(
            'orchard_pk_idx',
            'id_account',
            'id_place'
        ),
        {'schema': 'farm'}
    )

    id_account = Column(
        BigInteger(),
        ForeignKey(
            GamerAccount.id,
            ondelete='CASCADE',
            onupdate='CASCADE',
            use_alter=True
        ),
        primary_key=True,
        autoincrement=True
    )
    id_place = Column(
        Integer(),
        primary_key=True,
        autoincrement=False
    )
    tree = Column(
        String(32),
        ForeignKey(
            GameItem.id,
            ondelete='RESTRICT',
            onupdate='CASCADE',
            use_alter=True
        ),
        default=None
    )
    will_ripen = Column(
        DateTime(),
        default=None
    )
    was_fertilized = Column(
        Boolean(),
        default=False
    )
    was_watered = Column(
        Boolean(),
        default=False
    )
    was_robbed = Column(
        Boolean(),
        default=False
    )
    is_pick = Column(
        Boolean(),
        default=False
    )


class FarmMeadow(db.Model):
    __tablename__ = 'meadow'
    __table_args__ = (
        Index(
            'meadow_pk_idx',
            'id_account',
            'id_place'
        ),
        {'schema': 'farm'}
    )

    id_account = Column(
        BigInteger(),
        ForeignKey(
            GamerAccount.id,
            ondelete='CASCADE',
            onupdate='CASCADE',
            use_alter=True
        ),
        primary_key=True,
        autoincrement=True
    )
    id_place = Column(
        Integer(),
        primary_key=True,
        autoincrement=False
    )
    animal = Column(
        String(32),
        ForeignKey(
            GameItem.id,
            ondelete='RESTRICT',
            onupdate='CASCADE',
            use_alter=True
        ),
        default=None
    )
    will_produce = Column(
        DateTime(),
        default=None
    )
    was_given_vitamins = Column(
        Boolean(),
        default=False
    )
    was_given_water = Column(
        Boolean(),
        default=False
    )
    was_robbed = Column(
        Boolean(),
        default=False
    )
    is_pick = Column(
        Boolean(),
        default=False
    )


class QuestReward(db.Model):
    __tablename__ = 'reward'
    __table_args__ = (
        CheckConstraint(
            'quantity >= 0',
            name='quantity_cannot_be_negative'
        ),
        {'schema': 'quest'}
    )

    id = Column(
        Integer(),
        primary_key=True,
        index=True,
        autoincrement=False
    )
    id_item = Column(
        String(32),
        ForeignKey(
            GameItem.id,
            ondelete='RESTRICT',
            onupdate='CASCADE',
            use_alter=True
        ),
        nullable=False
    )
    quantity = Column(
        Integer(),
        nullable=False
    )


class QuestTask(db.Model):
    __tablename__ = 'task'
    __table_args__ = (
        CheckConstraint(
            'quantity >= 0',
            name='quantity_cannot_be_negative'
        ),
        {'schema': 'quest'}
    )

    id = Column(
        Integer(),
        primary_key=True,
        autoincrement=False,
        index=True
    )

    id_item = Column(
        String(32),
        ForeignKey(
            GameItem.id,
            ondelete='RESTRICT',
            onupdate='CASCADE',
            use_alter=True
        ),
        nullable=False
    )

    quantity = Column(
        Integer(),
        nullable=False
    )


class DonationCurrency(db.Model):
    __tablename__ = 'currency'
    __table_args__ = (
        {'schema': 'donation'}
    )

    id = Column(
        String(3),
        primary_key=True,
        autoincrement=False
    )


class DonationPackage(db.Model):
    __tablename__ = 'package'
    __table_args__ = (
        CheckConstraint(
            'quantity >= 0',
            name='quantity_cannot_be_negative'
        ),
        CheckConstraint(
            'sell_price >= 0',
            name='sell_price_cannot_be_negative'
        ),
        {'schema': 'donation'}
    )

    id = Column(
        Integer(),
        primary_key=True,
        autoincrement=False
    )
    quantity = Column(
        Integer(),
        nullable=False
    )
    sell_price = Column(
        Integer(),
        nullable=False
    )
    sell_currency = Column(
        String(3),
        ForeignKey(
            DonationCurrency.id,
            ondelete='RESTRICT',
            onupdate='CASCADE',
            use_alter=True
        ),
        nullable=False
    )


class DonationPayment(db.Model):
    __tablename__ = 'payment'
    __table_args__ = (
        {'schema': 'donation'}
    )

    id = Column(
        Integer(),
        primary_key=True,
        autoincrement=False
    )
    id_account = Column(
        BigInteger(),
        ForeignKey(
            GamerAccount.id,
            ondelete='CASCADE',
            onupdate='CASCADE',
            use_alter=True
        ),
        nullable=False
    )
    id_package = Column(
        Integer(),
        ForeignKey(
            DonationPackage.id,
            ondelete='RESTRICT',
            onupdate='CASCADE',
            use_alter=True
        ),
        nullable=False
    )
    datetime = Column(
        DateTime(),
        nullable=False,
        server_default=func.now()
    )
    unique_id = Column(
        String(128),
        nullable=False
    )
