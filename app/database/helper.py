# coding: utf8

from dataclasses import dataclass


@dataclass()
class GameItemCategory:
    SEED = 'seed'
    TREE = 'tree'
    ANIMAL = 'animal'

    PLANT = 'plant'
    FRUIT = 'fruit'
    PRODUCTION = 'production'


@dataclass()
class GameCurrency:
    COIN = 'coin'
    GEN = 'gen'
