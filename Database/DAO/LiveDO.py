#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : LiveDO.py
# @Time     : 2021/9/6 20:23
# @Author   : NagisaCo
import asyncio
from Database.MySQL import MySQL


class LiveDO(object):
    def __init__(self, mysql: MySQL):
        self.mysql = mysql

    async def insert_unknown(self, room_id):
        sql = f"INSERT INTO live VALUES (NULL, {room_id}, NULL, NULL, NULL, NULL);"
        live_id = await self.mysql.execute(sql)
        return live_id

    async def insert_start(self, room_id, user_name: str, title: str, start_time: str):
        sql = f"INSERT INTO live VALUES (NULL, {room_id}, '{user_name}', '{title}', {start_time}, NULL);"
        live_id = await self.mysql.execute(sql)
        return live_id

    async def update_end(self, live_id: int, end_time: str):
        sql = f"UPDATE live SET end_time={end_time} WHERE id={live_id};"
        await self.mysql.execute(sql)

    async def update_unknown_start(self, live_id: int, user_name: str, title: str, start_time: str):
        sql = f"UPDATE live SET title='{title}', user_name='{user_name}', start_time={start_time} WHERE id={live_id};"
        await self.mysql.execute(sql)

    async def update_unknown_end(self, live_id: int, user_name: str, title: str, start_time: str, end_time: str):
        sql = f"UPDATE live SET title='{title}', user_name='{user_name}', start_time={start_time}, end_time={end_time} WHERE id={live_id};"
        await self.mysql.execute(sql)