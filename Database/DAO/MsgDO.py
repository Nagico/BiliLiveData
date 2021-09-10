#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : MsgDO.py
# @Time     : 2021/9/6 18:30
# @Author   : NagisaCo
import time
from math import log10

import aiomysql
import pymysql

import BiliLive.Msg.Status
from Database.DAO.LiveDO import LiveDO
from Database.Redis import Redis


class BasicInfo(object):
    def __init__(self):
        self.table_name = ""
        self.live_id = 0
        self.live_status = 0
        self.room_id = 0
        self.create_time = ""


class MsgDO(object):
    def __init__(self, connection: aiomysql.Connection, redis: Redis):
        self.connection = connection
        self.redis = redis
        self.live = LiveDO(self.connection)

    async def _prepare_info(self, msg) -> BasicInfo:
        info = BasicInfo()
        info.table_name = time.strftime("%Y%m", time.localtime(msg.fetchTime / 1000))
        if isinstance(msg, BiliLive.Msg.Status.Status):
            info.room_id = msg.room_id
        else:
            info.room_id = msg.roomRealId
        info.create_time = self.t2d(msg.fetchTime)
        info.live_id, info.live_status = await self._get_live_info(info)

        return info

    async def _get_live_info(self, info: BasicInfo) -> (int, int):
        result = await self.redis.pool.get(str(info.room_id))
        if result is None:  # 不存在room_id, 初始化
            live_id = await self.live.insert_unknown(info.room_id)
            await self.redis.pool.set(str(info.room_id), '|'.join([str(live_id), '2']))
            return live_id, 2
        result_list = result.split('|')
        return int(result_list[0]), int(result_list[1])

    async def update_live_info(self, msg: BiliLive.Msg.Status, info: BasicInfo):
        await self._set_live_info(info, new_live_status=int(msg.live_status), username=msg.username, title=msg.title,
                                  start_time=msg.live_start_time, end_time=msg.fetchTime)

    async def _set_live_info(self, info: BasicInfo, new_live_status: int, username: str = None, title: str = None,
                             start_time: int = None, end_time: int = None) -> None:
        if info.live_status == 2 and new_live_status == 1:  # 原状态为未知, 现在正在直播
            await self.live.update_unknown_start(info.live_id, username, title, self.t2d(start_time))
            await self.redis.pool.set(str(info.room_id), '|'.join([str(info.live_id), '1']))
            info.live_id, info.live_status = info.live_id, 1
        elif info.live_status == 2 and new_live_status == 0:  # 原状态为未知, 现在未直播
            await self.live.update_unknown_end(info.live_id, username, title, 'NULL', self.t2d(end_time))
            await self.redis.pool.set(str(info.room_id), '|'.join([str(info.live_id), '0']))
            info.live_id, info.live_status = info.live_id, 0
        elif info.live_status == 0 and new_live_status == 1:  # 原状态为未直播, 现在开始直播
            new_live_id = await self.live.insert_start(info.room_id, username, title, self.t2d(start_time))
            await self.redis.pool.set(str(info.room_id), '|'.join([str(new_live_id), '1']))
            info.live_id, info.live_status = new_live_id, 1
        elif info.live_status == 1 and new_live_status == 0:  # 原状态为直播中, 现在停止直播
            await self.live.update_end(info.live_id, self.t2d(end_time))
            await self.redis.pool.set(str(info.room_id), '|'.join([str(info.live_id), '0']))
            info.live_status = 0

    @staticmethod
    def _check_null(_: int):
        if _ is None:
            return 'NULL'
        else:
            return _

    @staticmethod
    def _check_null_str(_: str):
        if _ is None:
            return 'NULL'
        elif _ == "":
            return 'NULL'
        else:
            return f"'{_}'"

    @staticmethod
    def t2d(timestamp: int):
        if timestamp == 0:
            return 'NULL'
        if int(log10(timestamp)) + 1 == 13:  # 处理13位timestamp
            t = timestamp / 1000
        else:
            t = timestamp
        return f"'{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))}'"

    async def _get_info(self, msg):
        return await self._prepare_info(msg)

    async def _create_live_table(self):
        sql = f"""
        CREATE TABLE `live` (
            `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '直播id',
            `room_id` INT UNSIGNED NOT NULL COMMENT '房间号',
            `user_name` VARCHAR ( 255 ) DEFAULT NULL COMMENT '主播名',
            `title` VARCHAR ( 255 ) CHARACTER 
            SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '直播标题',
            `start_time` datetime DEFAULT NULL COMMENT '开始时间',
            `end_time` datetime DEFAULT NULL COMMENT '结束时间',
            PRIMARY KEY ( `id` ),
            UNIQUE KEY `search_id` ( `id` ) USING BTREE COMMENT '获取id',
            KEY `search_room_id` ( `room_id` ) USING BTREE COMMENT '获取房间号',
        KEY `search_user_name` ( `user_name` ) 
        ) ENGINE = INNODB AUTO_INCREMENT = 85 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
        """
        await self._execute(sql)

    async def insert(self, msg):
        info = None
        try:
            info = await self._get_info(msg)
        except pymysql.err.ProgrammingError as e:
            if "doesn't exist" in e.args[1]:
                await self._create_live_table()
                info = await self._get_info(msg)
        if isinstance(msg, BiliLive.Msg.Status.Status):
            await self.update_live_info(msg, info)
        try:
            await self._insert(msg, info)
        except pymysql.err.ProgrammingError as e:
            if "doesn't exist" in e.args[1]:
                await self._create_new_table(info)
                await self._insert(msg, info)

    async def _execute(self, sql):
        # print(sql)
        async with self.connection.cursor() as cursor:
            await cursor.execute(sql)
            await self.connection.commit()

    async def _insert(self, msg, info: BasicInfo):
        raise NotImplementedError

    async def _create_new_table(self, info: BasicInfo):
        raise NotImplementedError
