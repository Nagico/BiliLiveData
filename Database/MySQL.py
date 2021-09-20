#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : MySQL.py
# @Time     : 2021/9/6 15:31
# @Author   : NagisaCo
import asyncio
import aiomysql
from loguru import logger


class MySQL(object):
    def __init__(
            self,
            host: str = "localhost",
            port: int = 3306,
            user: str = "bili_live_data",
            password: str = "bili_live_data",
            db: str = "bili_live_data"):
        self.connection = None
        self.host = host
        logger.debug(f'Get config [host]: {self.host}')
        self.port = port
        logger.debug(f'Get config [port]: {self.port}')
        self.user = user
        logger.debug(f'Get config [user]: {self.user}')
        self.password = password
        logger.debug(f'Get config [password]: *length*{len(self.password)}')
        self.db = db
        logger.debug(f'Get config [db]: {self.db}')
        self.lock = asyncio.Lock()

    async def connect(self):
        self.connection = await aiomysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db)
        logger.info('Connected')

    async def disconnect(self):
        self.connection.close()

    async def execute(self, sql: str):
        async with self.lock:
            async with self.connection.cursor() as cur:
                # logger.debug(f'Execute sql\n{sql}')
                await cur.execute(sql)
                last_id = cur.lastrowid
                await self.connection.commit()
        return last_id
