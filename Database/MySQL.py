#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : MySQL.py
# @Time     : 2021/9/6 15:31
# @Author   : NagisaCo
import aiomysql


class MySQL(object):
    def __init__(
            self,
            host: str = "localhost",
            port: int = 3306,
            user: str = "bili_live_data",
            password: str = "bili_live_data",
            db: str = "bili_live_data"):
        self.pool = None
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db

    async def connect(self):
        self.pool = await aiomysql.create_pool(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db)
        print("mysql connected")

    async def disconnect(self):
        self.pool.close()

    async def get_connection(self):
        return await self.pool.acquire()
