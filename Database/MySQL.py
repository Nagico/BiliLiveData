#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : MySQL.py
# @Time     : 2021/9/6 15:31
# @Author   : NagisaCo
import asyncio
import aiomysql
from loguru import logger


class Connection(object):
    def __init__(self):
        self.conn = None
        self.lock = asyncio.Lock()

    async def connect(self, host: str, port: int, user: str, password: str, db: str):
        self.conn = await aiomysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                db=db
            )

    async def disconnect(self):
        await self.conn.ensure_closed()

    async def execute(self, sql: str):
        async with self.lock:
            async with self.conn.cursor() as cur:
                # logger.debug(f'Execute sql\n{sql}')
                await cur.execute(sql)
                last_id = cur.lastrowid
                await self.conn.commit()
        return last_id


class Pool(object):
    def __init__(self, maxsize: int = 10):
        self.maxsize = maxsize
        self.queue = asyncio.Queue(maxsize=self.maxsize)

    async def create(self, host: str, port: int, user: str, password: str, db: str):
        for i in range(self.maxsize):
            connection = Connection()
            await connection.connect(host, port, user, password, db)
            logger.debug(f'Connection {i} created')
            self.queue.put_nowait(connection)

    async def destroy(self):
        while not self.queue.empty():
            conn = self.queue.get_nowait()
            await conn.disconnect()

    async def execute(self, sql: str):
        conn = await self.queue.get()
        result = await conn.execute(sql)
        self.queue.put_nowait(conn)

        return result


class MySQL(object):
    def __init__(
            self,
            host: str = "localhost",
            port: int = 3306,
            user: str = "bili_live_data",
            password: str = "bili_live_data",
            db: str = "bili_live_data"):
        self.pool = Pool()
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
        await self.pool.create(self.host, self.port, self.user, self.password, self.db)

        logger.info('Connected')

    async def disconnect(self):
        await self.pool.destroy()

    async def execute(self, sql: str):
        return await self.pool.execute(sql)
