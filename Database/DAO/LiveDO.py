#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : LiveDO.py
# @Time     : 2021/9/6 20:23
# @Author   : NagisaCo
import asyncio

import aiomysql


class LiveDO(object):
    def __init__(self, connection: aiomysql.Connection):
        self.connection = connection

    async def insert_unknown(self, room_id):
        async with self.connection.cursor() as cur:
            await cur.execute(
                f"INSERT INTO live "
                f"VALUES (NULL, {room_id}, NULL, NULL, NULL, NULL);"
            )
            live_id = cur.lastrowid
            await self.connection.commit()
            return live_id

    async def insert_start(self, room_id, user_name: str, title: str, start_time: str):
        async with self.connection.cursor() as cur:
            await cur.execute(
                f"INSERT INTO live "
                f"VALUES (NULL, {room_id}, '{user_name}', '{title}', {start_time}, NULL);"
            )
            live_id = cur.lastrowid
            await self.connection.commit()
        return live_id

    async def update_end(self, live_id: int, end_time: str):
        async with self.connection.cursor() as cur:
            await cur.execute(
                f"UPDATE live "
                f"SET end_time={end_time} "
                f"WHERE id={live_id};"
            )
            await self.connection.commit()

    async def update_unknown_start(self, live_id: int, user_name: str, title: str, start_time: str):
        async with self.connection.cursor() as cur:
            await cur.execute(
                f"UPDATE live "
                f"SET title='{title}', user_name='{user_name}', start_time={start_time} "
                f"WHERE id={live_id};"
            )
            await self.connection.commit()

    async def update_unknown_end(self, live_id: int, user_name: str, title: str, start_time: str, end_time: str):
        async with self.connection.cursor() as cur:
            await cur.execute(
                f"UPDATE live "
                f"SET title='{title}', user_name='{user_name}', start_time={start_time}, end_time={end_time} "
                f"WHERE id={live_id};"
            )
            await self.connection.commit()

