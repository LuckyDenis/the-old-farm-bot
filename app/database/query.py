# coding: utf8

from app.database.models import db
from app.database.models import GamerAccount
from app.database.models import GamerPurse
from app.database.models import FarmField
from app.database.models import FarmOrchard
from app.database.models import FarmMeadow
from app.database.models import FarmWarehouse
from app.database.models import GamerSelectedFarm
from app.database.models import GamerGifts
from app.database.models import GamerSelectedShopItem


class NewGamer:
    COINS = None
    GENS = None
    FIELD_SIZE = None
    ORCHARD_SIZE = None
    MEADOW_SIZE = None
    WAREHOUSE_SIZE = None
    GIFT_SIZE = None


class Account:
    @classmethod
    async def is_created(cls, data):
        account = await db.select(
            [GamerAccount.id]
        ).select_from(
            GamerAccount
        ).where(
            GamerAccount.id == data["id"]
        ).gino.one_or_none()
        return {'is_created': account is not None}

    @classmethod
    async def update(cls, data):
        async with db.transaction():
            await cls._clean_username(data)
            await GamerAccount.update().where(
                GamerAccount.id == data['id']
            ).values(username=data['username']).gino.status()

    @classmethod
    async def _clean_username(cls, data):
        await GamerAccount.update().where(
            GamerAccount.username == data['username']
        ).values(username=None).gino.status()

    @classmethod
    async def _create_field(cls, data):
        field = []
        for id_place in range(1, NewGamer.FIELD_SIZE + 1):
            field.append({
                'id_account': data['id'],
                'id_place': id_place
            })
        await FarmField.insert().values(field).gino.status()

    @classmethod
    async def _create_orchard(cls, data):
        orchard = []
        for id_place in range(1, NewGamer.ORCHARD_SIZE + 1):
            orchard.append({
                'id_account': data['id'],
                'id_place': id_place
            })
        await FarmOrchard.insert().values(orchard).gino.status()

    @classmethod
    async def _create_meadow(cls, data):
        meadow = []
        for id_place in range(1, NewGamer.MEADOW_SIZE + 1):
            meadow.append({
                'id_account': data['id'],
                'id_place': id_place
            })
        await FarmMeadow.insert().values(meadow).gino.status()

    @classmethod
    async def _create_warehouse(cls, data):
        warehouse = []
        for id_shelf in range(1, NewGamer.WAREHOUSE_SIZE):
            warehouse.append({
                'id_account': data[id],
                'id_shelf': id_shelf
            })
        await FarmWarehouse.insert().values(warehouse).gino.status()

    @classmethod
    async def _create_gift_storage(cls, data):
        gift_storage = []
        for id_shelf in range(1, NewGamer.GIFT_SIZE + 1):
            gift_storage.append({
                'id_account': data['id'],
                'id_shelf': id_shelf
            })
        await GamerGifts.insert().values(gift_storage).gino.status()

    @classmethod
    async def _create_account(cls, data):
        await GamerAccount.insert().values(
            id=data['id'],
            username=data['username'],
            is_bot=data['is_bot']
        ).gino.status()

    @classmethod
    async def _create_purse(cls, data):
        await GamerPurse.insert().values(
            id_account=data['id'],
            coins=NewGamer.COINS,
            gems=NewGamer.GENS
        ).gino().status()

    @classmethod
    async def _create_gamer_selected(cls, data):
        await GamerSelectedFarm.insert().values(
            id_account=data['id']
        ).gino.status()

        await GamerSelectedShopItem.insert().values(
            id_account=data['id']
        )

    @classmethod
    async def create(cls, data):
        async with db.transaction():
            await cls._clean_username(data)
            await cls._create_account(data)
            await cls._create_purse(data)
            await cls._create_field(data)
            await cls._create_orchard(data)
            await cls._create_meadow(data)
            await cls._create_warehouse(data)
            await cls._create_gift_storage(data)
            await cls._create_gamer_selected(data)
