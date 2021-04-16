# coding: utf8

from dataclasses import dataclass


@dataclass()
class GameItems:
    # animal
    BEE_ANIMAL = 'a_bee'
    CHICKEN_ANIMAL = 'a_chicken'
    COW_ANIMAL = 'a_cow'
    GOAT_ANIMAL = 'a_goat'
    SHEEP_ANIMAL = 'a_sheep'

    # animal production
    BEE_HONEY = 'honey'
    CHICKEN_EGG = 'chicken_egg'
    COW_MILK = 'cow_milk'
    GOAT_CHEESE = 'goat_cheese'
    SHEEP_WOOL = 'sheep_wool'

    # seeds
    BROCCOLI_SEED = 's_broccoli'
    CARROT_SEED = 's_carrot'
    CORN_SEED = 's_corn'
    CUCUMBER_SEED = 's_cucumber'
    EGGPLANT_SEED = 's_eggplant'
    HIBISCUS_SEED = 's_hibiscus'
    LEAFY_GREEN_SEED = 's_leafy_green'
    MELON_SEED = 's_melon'
    MUSHROOM_SEED = 's_mushroom'
    PEANUT_SEED = 's_peanut'
    PEPPER_SEED = 's_pepper'
    PINEAPPLE_SEED = 's_pineapple'
    POTATO_SEED = 's_potato'
    ROSE_SEED = 's_rose'
    STRAWBERRY_SEED = 's_strawberry'
    SUNFLOWER_SEED = 's_sunflower'
    SWEET_POTATO_SEED = 's_sweet_potato'
    TOMATO_SEED = 's_tomato'
    WATERMELON_SEED = 's_watermelon'
    WHEAT_SEED = 's_wheat'

    # plant
    BROCCOLI = 'broccoli'
    CARROT = 'carrot'
    CORN = 'corn'
    CUCUMBER = 'cucumber'
    EGGPLANT = 'eggplant'
    HIBISCUS = 'hibiscus'
    LEAFY_GREEN = 'leafy_green'
    MELON = 'melon'
    MUSHROOM = 'mushroom'
    PEANUT = 'peanut'
    PEPPER = 'pepper'
    PINEAPPLE = 'pineapple'
    POTATO = 'potato'
    ROSE = 'rose'
    STRAWBERRY = 'strawberry'
    SUNFLOWER = 'sunflower'
    SWEET_POTATO = 'sweet_potato'
    TOMATO = 'tomato'
    WATERMELON = 'watermelon'
    WHEAT = 'wheat'

    # seedling
    APPLE_TREE = 't_apple'
    AVOCADO_TREE = 't_avocado'
    BANANA_TREE = 't_banana'
    CHERRIES_TREE = 't_cherries'
    CHESTNUT_TREE = 't_chestnut'
    COCONUT_TREE = 't_coconut'
    GRAPES_TREE = 't_grapes'
    KIWIFRUIT_TREE = 't_kiwifruit'
    LEMON_TREE = 't_lemon'
    MANGO_TREE = 't_mango'
    PEACH_TREE = 't_peach'
    PEAR_TREE = 't_pear'
    TANGERINE_TREE = 't_tangerine'

    # fruit
    APPLE = 'apple'
    AVOCADO = 'avocado'
    BANANA = 'banana'
    CHERRIES = 'cherries'
    CHESTNUT = 'chestnut'
    COCONUT = 'coconut'
    GRAPES = 'grapes'
    KIWIFRUIT = 'kiwifruit'
    LEMON = 'lemon'
    MANGO = 'mango'
    PEACH = 'peach'
    PEAR = 'pear'
    TANGERINE = 'tangerine'

    # positive effect
    PLANT_FERTILIZE = 'e_plant_fertilize'
    TREE_FERTILIZE = 'e_tree_fertilize'
    ANIMAL_VITAMIN = 'e_animal_vitamin'

    # pet
    DOG = 'p_dog'

    # pet food
    SMALL_BONE = 'f_small_bone'
    MIDDLE_BONE = 'f_middle_bone'
    BIG_BONE = 'f_big_bone'

    # elements current package
    COINS_SMALL_BAG = 'c_small_bag'
    COINS_MIDDLE_BAG = 'c_middle_bag'
    COINS_BIG_BAG = 'c_big_bag'
    GEM_SMALL_BAG = 'g_small_bag'
    GEM_MIDDLE_BAG = 'g_middle_bag'
    GEM_BIG_BAG = 'g_big_game'
    GEM_COINS_CONVERT_BAG = 'gc_convert_bag'


@dataclass()
class GameObject:
    FIELD = 'field'
    ORCHARD = 'orchard'
    MEADOW = 'meadow'
    WAREHOUSE = 'warehouse'
    PURSE = 'purse'
    HOUSE = 'house'
    GIFTS = 'gifts'
    GIFT = 'gift'
    PHONE = 'phone'
    LANGUAGES = 'languages'
    QUESTS = 'quests'

    NEIGHBORS = 'neighbors'
    THIEF = 'thief'

    SHOP = 'shop'
    SHOP_SEEDS = 'shop_seed'
    SHOP_TREES = 'shop trees'
    SHOP_ANIMALS = 'shop animals'
    SHOP_EFFECTS = 'shop effects'
    SHOP_MONEY = 'shop money'
    SHOP_PET_FOODS = 'shop pet foods'
    SHOP_PETS = 'shop pets'
    SHOP_LANDS = 'shop lands'
    SHOP_DONATION = 'shop donation'

    ERROR = 'error'
    WARNING = 'warning'
    INFORMATION = 'information'
    SUCCESS = 'success'

    PROJECT_NEWS = 'projects news'


@dataclass()
class GameLanguage:
    RUSSIAN = 'russian'
    ENGLISH = 'english'
