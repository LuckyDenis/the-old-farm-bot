# coding: utf8

"""
Импортировать в первый commit в базу.

def upgrade():
    ...
    add_data(op)

"""

from app.database import models
from app.database.helper import GameCurrency
from app.database.helper import GameItemCategory
from app.ui.elements.codes import GameItems


def add_game_item_categories(op):
    ID = 'id'
    op.bulk_insert(
        models.GameItemCategory,
        [
            {ID: GameItemCategory.SEED},
            {ID: GameItemCategory.TREE},
            {ID: GameItemCategory.ANIMAL},
            {ID: GameItemCategory.PLANT},
            {ID: GameItemCategory.FRUIT},
            {ID: GameItemCategory.PRODUCTION}
        ]
    )


def add_game_currencies(op):
    ID = 'id'
    op.bulk_insert(
        models.GameCurrency,
        [
            {ID: GameCurrency.COIN},
            {ID: GameCurrency.GEN}
        ]
    )


def add_game_items(op):
    ID = 'id'
    CATEGORY = 'category'
    SELL_PRICE = 'sell_price'
    SELL_GAME_CURRENCY = 'sell_game_currency'
    op.bulk_insert(
        models.GameItem,
        [
            {
                ID: GameItems.APPLE,
                CATEGORY: GameItemCategory.FRUIT,
                SELL_PRICE: 10,
                SELL_GAME_CURRENCY: GameCurrency.COIN
            },
        ]
    )


def add_data(op):
    DATA = [
        add_game_item_categories,
        add_game_currencies,
        add_game_items
    ]

    for add_func in DATA:
        add_func(op)
