# coding: utf8

# coding: utf8

from app.ui.i18n import I18N
from app.ui.elements.codes import GameItems
from app.ui.elements.codes import GameObject


i18n = I18N()
_ = i18n.gettext_lazy


EMOJI_TEMPLATE = ':{emoji}:'


class GameItemIcon:
    ICONS = {
        GameItems.BEE_ANIMAL: 'bee',
        GameItems.CHICKEN_ANIMAL: 'rooster',
        GameItems.COW_ANIMAL: 'cow2',
        GameItems.GOAT_ANIMAL: 'goat',
        GameItems.SHEEP_ANIMAL: 'sheep',

        GameItems.BEE_HONEY: 'honey_pot',
        GameItems.CHICKEN_EGG: 'egg2',
        GameItems.COW_MILK: 'glass_of_milk',
        GameItems.GOAT_CHEESE: 'cheese_wedge',
        GameItems.SHEEP_WOOL: 'wool',

        GameItems.BROCCOLI_SEED: 'seedling',
        GameItems.CARROT_SEED: 'seedling',
        GameItems.CORN_SEED: 'seedling',
        GameItems.CUCUMBER_SEED: 'seedling',
        GameItems.EGGPLANT_SEED: 'seedling',
        GameItems.HIBISCUS_SEED: 'seedling',
        GameItems.LEAFY_GREEN_SEED: 'seedling',
        GameItems.MELON_SEED: 'seedling',
        GameItems.MUSHROOM_SEED: 'seedling',
        GameItems.PEANUT_SEED: 'seedling',
        GameItems.PEPPER_SEED: 'seedling',
        GameItems.PINEAPPLE_SEED: 'seedling',
        GameItems.POTATO_SEED: 'seedling',
        GameItems.ROSE_SEED: 'seedling',
        GameItems.STRAWBERRY_SEED: 'seedling',
        GameItems.SUNFLOWER_SEED: 'seedling',
        GameItems.SWEET_POTATO_SEED: 'seedling',
        GameItems.TOMATO_SEED: 'seedling',
        GameItems.WATERMELON_SEED: 'seedling',
        GameItems.WHEAT_SEED: 'seedling',

        GameItems.BROCCOLI: 'broccoli',
        GameItems.CARROT: 'carrot',
        GameItems.CORN: 'corn',
        GameItems.CUCUMBER: 'cucumber',
        GameItems.EGGPLANT: 'eggplant',
        GameItems.HIBISCUS: 'hibiscus',
        GameItems.LEAFY_GREEN: 'leafy_green',
        GameItems.MELON: 'melon',
        GameItems.MUSHROOM: 'mushroom',
        GameItems.PEANUT: 'peanut',
        GameItems.PEPPER: 'pepper',
        GameItems.PINEAPPLE: 'pineapple',
        GameItems.POTATO: 'potato',
        GameItems.ROSE: 'rose',
        GameItems.STRAWBERRY: 'strawberry',
        GameItems.SUNFLOWER: 'sunflower',
        GameItems.SWEET_POTATO: 'sweet_potato',
        GameItems.TOMATO: 'tomato',
        GameItems.WATERMELON: 'watermelon',
        GameItems.WHEAT: 'wheat',

        GameItems.APPLE_TREE: 'deciduous_tree',
        GameItems.AVOCADO_TREE: 'deciduous_tree',
        GameItems.BANANA_TREE: 'palm_tree',
        GameItems.CHERRIES_TREE: 'deciduous_tree',
        GameItems.CHESTNUT_TREE: 'deciduous_tree',
        GameItems.COCONUT_TREE: 'palm_tree',
        GameItems.GRAPES_TREE: 'deciduous_tree',
        GameItems.KIWIFRUIT_TREE: 'deciduous_tree',
        GameItems.LEMON_TREE: 'deciduous_tree',
        GameItems.MANGO_TREE: 'deciduous_tree',
        GameItems.PEACH_TREE: 'deciduous_tree',
        GameItems.PEAR_TREE: 'deciduous_tree',
        GameItems.TANGERINE_TREE: 'deciduous_tree',

        GameItems.APPLE: 'apple',
        GameItems.AVOCADO: 'avocado',
        GameItems.BANANA: 'banana',
        GameItems.CHERRIES: 'cherries',
        GameItems.CHESTNUT: 'chestnut',
        GameItems.COCONUT: 'coconut',
        GameItems.GRAPES: 'grapes',
        GameItems.KIWIFRUIT: 'kiwi fruit',
        GameItems.LEMON: 'lemon',
        GameItems.MANGO: 'mango',
        GameItems.PEACH: 'peach',
        GameItems.PEAR: 'pear',
        GameItems.TANGERINE: 'tangerine',

        GameItems.PLANT_FERTILIZE: 'test_tube',
        GameItems.TREE_FERTILIZE: 'test_tube',
        GameItems.ANIMAL_VITAMIN: 'pill',

        GameItems.DOG: 'dog',

        GameItems.SMALL_BONE: 'bone',
        GameItems.MIDDLE_BONE: 'bone',
        GameItems.BIG_BONE: 'bone',

        GameItems.COINS_SMALL_BAG: 'moneybag',
        GameItems.COINS_MIDDLE_BAG: 'moneybag',
        GameItems.COINS_BIG_BAG: 'moneybag',
        GameItems.GEM_SMALL_BAG: 'red_envelope',
        GameItems.GEM_MIDDLE_BAG: 'red_envelope',
        GameItems.GEM_BIG_BAG: 'red_envelope',
        GameItems.GEM_COINS_CONVERT_BAG: 'barber'
    }

    @classmethod
    def get(cls, game_item_id):
        return EMOJI_TEMPLATE.format(emoji=cls.ICONS.get(game_item_id))


class GameObjectIcon:
    ICONS = {
        GameObject.FIELD: 'tractor',
        GameObject.ORCHARD: 'basket',
        GameObject.MEADOW: 'hatching_chick',
        GameObject.WAREHOUSE: 'closed_lock_with_key',
        GameObject.PURSE: 'credit_card',

        GameObject.HOUSE: 'house',
        GameObject.GIFTS: 'gifts',
        GameObject.GIFT: 'gift',
        GameObject.PHONE: 'phone',
        GameObject.LANGUAGES: 'languages',
        GameObject.QUESTS: 'quests',

        GameObject.NEIGHBORS: 'neighbors',
        GameObject.THIEF: 'thief',

        GameObject.SHOP: 'convenience_store',
        GameObject.SHOP_SEEDS: 'shopping_bags',
        GameObject.SHOP_TREES: 'shopping_bags',
        GameObject.SHOP_ANIMALS: 'shopping_bags',
        GameObject.SHOP_EFFECTS: 'shopping_bags',
        GameObject.SHOP_MONEY: 'shopping_bags',
        GameObject.SHOP_PETS: 'shopping_bags',
        GameObject.SHOP_PET_FOODS: 'shopping_bags',
        GameObject.SHOP_LANDS: 'shopping_bags',
        GameObject.SHOP_DONATION: 'shopping_bags',

        GameObject.ERROR: 'sos',
        GameObject.WARNING: 'warning',
        GameObject.INFORMATION: 'information_source',
        GameObject.SUCCESS: 'white_check_mark',

        GameObject.PROJECT_NEWS: 'newspaper'
    }

    @classmethod
    def get(cls, game_object_id):
        return EMOJI_TEMPLATE.format(emoji=cls.ICONS.get(game_object_id))
