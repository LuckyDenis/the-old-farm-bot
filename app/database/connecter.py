# coding: utf8
from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.engine.url import URL
from sqlalchemy import func
from gino import create_engine
from app.database.models import db
from logging import getLogger


if TYPE_CHECKING:
    from app.typehint import TDBConnect


logger = getLogger('app.database.connect')


class DBConnectMeta(type):
    instance: TDBConnect = None

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            instance = super().__call__(*args, **kwargs)
            cls.instance = instance
        return cls.instance


class DBConnect:
    def __init__(self, drive=None, port=None,
                 host=None, username=None,
                 password=None, dbname=None,
                 min_pool=None, max_pool=None,
                 isolation_level=None
                 ):
        self.driver = drive
        self.port = port
        self.host = host
        self.username = username
        self.password = password
        self.dbname = dbname
        self.min_pool = min_pool
        self.max_pool = max_pool
        self.isolation_level = isolation_level
        self.engine = None

    def setup(self, drive=None, port=None,
              host=None, username=None,
              password=None, dbname=None,
              min_pool=None, max_pool=None,
              isolation_level=None):
        self.__init__(
            drive=drive,
            port=port,
            host=host,
            username=username,
            password=password,
            dbname=dbname,
            min_pool=min_pool,
            max_pool=max_pool,
            isolation_level=isolation_level
        )
        return self

    async def test(self):
        conn = await self.get()
        pg_info = await conn.scalar(func.version())
        logger.log(60, f'Postgres спецификация: {pg_info}')

    def make_connect_url(self):
        return URL(
                drivername=self.driver,
                username=self.username,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.dbname
            )

    async def get(self):
        if not self.engine:
            url = self.make_connect_url()
            self.engine = await create_engine(
                name_or_url=url,
                min_size=self.min_pool,
                max_size=self.max_pool,
                isolation_level=self.isolation_level
            )
            db.bind = self.engine
        return db

    async def shutdown(self):
        if self.engine:
            self.engine, db.bind = db.bind, None
            await self.engine.close()
        else:
            db.bind = None
        self.engine = None
