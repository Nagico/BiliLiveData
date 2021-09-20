#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : Redis.py
# @Time     : 2021/9/6 19:41
# @Author   : NagisaCo
import asyncio_redis
from loguru import logger


class Redis(object):
    def __init__(self, host: str = 'localhost', password: str = '', port: int = 6379, db: int = 2):
        self.host = host
        logger.debug(f'Get config [host]: {self.host}')
        if password == '':
            self.password = None
        else:
            self.password = password.encode(encoding='utf-8')
            logger.debug(f'Get config [password]: *length*{len(self.password)}')
        self.port = port
        logger.debug(f'Get config [port]: {self.port}')
        self.db = db
        logger.debug(f'Get config [db]: {self.db}')
        self.pool = None

    async def connect(self):
        self.pool = await asyncio_redis.Pool.create(
                host=self.host,
                password=self.password,
                port=self.port,
                db=self.db,
                poolsize=20
            )
        logger.info('Connected')

    async def disconnect(self):
        self.pool.close()
