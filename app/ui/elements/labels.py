# coding: utf8

from app.ui.i18n import I18N
from app.ui.elements.codes import GameItems

i18n = I18N()
_ = i18n.gettext_lazy


class GameItemLabel:
    LABELS = {
        GameItems.BEE_ANIMAL:  _('bee hive'),
        GameItems.CHICKEN_ANIMAL: _('chicken'),
        GameItems.COW_ANIMAL: _('cow'),
        GameItems.GOAT_ANIMAL: _('goat'),
        GameItems.SHEEP_ANIMAL: _('sheep'),

        GameItems.BEE_HONEY: _('bee honey'),
        GameItems.CHICKEN_EGG: _('chicken egg'),
        GameItems.COW_MILK: _('cow milk'),
        GameItems.GOAT_CHEESE: _('goat cheese'),
        GameItems.SHEEP_WOOL: _('sheep wool'),

        GameItems.BROCCOLI_SEED: _('broccoli'),
        GameItems.CARROT_SEED: _('carrot'),
        GameItems.CORN_SEED: _('corn'),
        GameItems.CUCUMBER_SEED: _('cucumber'),
        GameItems.EGGPLANT_SEED: _('eggplant'),
        GameItems.HIBISCUS_SEED: _('hibiscus'),
        GameItems.LEAFY_GREEN_SEED: _('leafy green'),
        GameItems.MELON_SEED: _('melon'),
        GameItems.MUSHROOM_SEED: _('mushroom'),
        GameItems.PEANUT_SEED: _('peanut'),
        GameItems.PEPPER_SEED: _('pepper'),
        GameItems.PINEAPPLE_SEED: _('pineapple'),
        GameItems.POTATO_SEED: _('potato'),
        GameItems.ROSE_SEED: _('rose'),
        GameItems.STRAWBERRY_SEED: _('strawberry'),
        GameItems.SUNFLOWER_SEED: _('sunflower'),
        GameItems.SWEET_POTATO_SEED: _('sweet_potato'),
        GameItems.TOMATO_SEED: _('tomato'),
        GameItems.WATERMELON_SEED: _('watermelon'),
        GameItems.WHEAT_SEED: _('wheat'),

        GameItems.BROCCOLI: _('broccoli'),
        GameItems.CARROT: _('carrot'),
        GameItems.CORN: _('corn'),
        GameItems.CUCUMBER: _('cucumber'),
        GameItems.EGGPLANT: _('eggplant'),
        GameItems.HIBISCUS: _('hibiscus'),
        GameItems.LEAFY_GREEN: _('leafy green'),
        GameItems.MELON: _('melon'),
        GameItems.MUSHROOM: _('mushroom'),
        GameItems.PEANUT: _('peanut'),
        GameItems.PEPPER: _('pepper'),
        GameItems.PINEAPPLE: _('pineapple'),
        GameItems.POTATO: _('potato'),
        GameItems.ROSE: _('rose'),
        GameItems.STRAWBERRY: _('strawberry'),
        GameItems.SUNFLOWER: _('sunflower'),
        GameItems.SWEET_POTATO: _('sweet_potato'),
        GameItems.TOMATO: _('tomato'),
        GameItems.WATERMELON: _('watermelon'),
        GameItems.WHEAT: _('wheat'),

        GameItems.APPLE_TREE: _('apple-tree'),
        GameItems.AVOCADO_TREE: _('avocado tree'),
        GameItems.BANANA_TREE: _('banana palm'),
        GameItems.CHERRIES_TREE: _('cherries tree'),
        GameItems.CHESTNUT_TREE: _('chestnut tree'),
        GameItems.COCONUT_TREE: _('coconut palm'),
        GameItems.GRAPES_TREE: _('grapes bush'),
        GameItems.KIWIFRUIT_TREE: _('actinidia chinensis'),
        GameItems.LEMON_TREE: _('lemon tree'),
        GameItems.MANGO_TREE: _('mango tree'),
        GameItems.PEACH_TREE: _('peach tree'),
        GameItems.PEAR_TREE: _('pear tree'),
        GameItems.TANGERINE_TREE: _('tangerine tree'),

        GameItems.APPLE: _('apple'),
        GameItems.AVOCADO: _('avocado'),
        GameItems.BANANA: _('banana'),
        GameItems.CHERRIES: _('cherries'),
        GameItems.CHESTNUT: _('chestnut'),
        GameItems.COCONUT: _('coconut'),
        GameItems.GRAPES: _('grapes'),
        GameItems.KIWIFRUIT: _('kiwi fruit'),
        GameItems.LEMON: _('lemon'),
        GameItems.MANGO: _('mango'),
        GameItems.PEACH: _('peach'),
        GameItems.PEAR: _('pear'),
        GameItems.TANGERINE: _('tangerine'),

        GameItems.PLANT_FERTILIZE: _('fertilize: plant'),
        GameItems.TREE_FERTILIZE: _('fertilize: tree'),
        GameItems.ANIMAL_VITAMIN: _('vitamin: animal'),

        GameItems.DOG: _('dog'),

        GameItems.SMALL_BONE: _('small bone'),
        GameItems.MIDDLE_BONE: _('middle bone'),
        GameItems.BIG_BONE: _('big bone'),

        GameItems.COINS_SMALL_BAG: _('coins small bag'),
        GameItems.COINS_MIDDLE_BAG: _('coins middle bag'),
        GameItems.COINS_BIG_BAG: _('coins big bag'),
        GameItems.GEM_SMALL_BAG: _('gem small bag'),
        GameItems.GEM_MIDDLE_BAG: _('gem middle bag'),
        GameItems.GEM_BIG_BAG: _('gem big elements'),
        GameItems.GEM_COINS_CONVERT_BAG: _('convert bag')
    }

    @classmethod
    def get(cls, game_item_id):
        return cls.LABELS.get(game_item_id)
