#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : MySQL.py
# @Time     : 2021/9/6 15:31
# @Author   : NagisaCo
import asyncio
import aiomysql


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
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.lock = asyncio.Lock()

    async def connect(self):
        self.connection = await aiomysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db)
        print("mysql connected")

    async def disconnect(self):
        self.connection.close()

    async def execute(self, sql: str):
        async with self.lock:
            async with self.connection.cursor() as cur:
                await cur.execute(sql)
                last_id = cur.lastrowid
                await self.connection.commit()
        return last_id
