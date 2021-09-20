#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : Processor.py
# @Time     : 2021/8/28 10:04
# @Author   : NagisaCo
import lzma
import pickle
from loguru import logger
import base64

from BiliLive.Msg.DanmukuMsg import DanmukuMsg
from BiliLive.Msg.GiftMsg import GiftMsg
from BiliLive.Msg.GuardMsg import GuardMsg
from BiliLive.Msg.SCMsg import SCMsg
from BiliLive.Msg.Status import Status
from Database.DAO.DanmukuDO import DanmukuDO
from Database.DAO.GiftDO import GiftDO
from Database.DAO.GuardDO import GuardDO
from Database.DAO.SCDO import SCDO
from Database.DAO.StatusDO import StatusDO
from Database.MySQL import MySQL
from Database.Redis import Redis


class Processor(object):
    def __init__(self, redis: Redis, mysql: MySQL):
        self.redis = redis
        self.mysql = mysql
        self.statusDO = None
        self.danmukuDO = None
        self.giftDO = None
        self.scDO = None
        self.guardDO = None

    async def init(self):
        await self.redis.connect()
        await self.mysql.connect()

        self.statusDO = StatusDO(self.mysql, self.redis)
        self.danmukuDO = DanmukuDO(self.mysql, self.redis)
        self.giftDO = GiftDO(self.mysql, self.redis)
        self.scDO = SCDO(self.mysql, self.redis)
        self.guardDO = GuardDO(self.mysql, self.redis)

    async def store(self, data: bytes):
        raw = lzma.decompress(data)
        content = pickle.loads(raw)
        UUID = content['UUID']
        for item in content['data']:
            logger.debug(f'Get MD5:{item.md5}')
            if item.md5 != "":
                dup = await self._check_duplicate(item.md5)
            else:
                dup = False
            if not dup:
                item_data = pickle.loads(item.data)
                item_data.UUID = UUID
                await self._insert(item_data)
                await self._tag(item.md5)
            else:
                pass

    async def _check_duplicate(self, md5: str) -> bool:
        return await self.redis.pool.exists(md5)

    async def _tag(self, md5: str) -> None:
        await self.redis.pool.set(md5, '0', expire=600)

    async def _insert(self, result):
        if isinstance(result, Status):
            await self.statusDO.insert(result)
        elif isinstance(result, DanmukuMsg):
            await self.danmukuDO.insert(result)
        elif isinstance(result, GiftMsg):
            await self.giftDO.insert(result)
        elif isinstance(result, SCMsg):
            await self.scDO.insert(result)
        elif isinstance(result, GuardMsg):
            await self.guardDO.insert(result)
