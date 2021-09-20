#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : GuardDO.py
# @Time     : 2021/9/7 22:55
# @Author   : NagisaCo
from BiliLive.Msg.GuardMsg import GuardMsg
from Database.DAO.MsgDO import MsgDO, BasicInfo


class GuardDO(MsgDO):
    async def create_new_table(self, info: BasicInfo):
        sql = f"""
            CREATE TABLE `{info.table_name}_guard` (
              `id` bigint unsigned NOT NULL AUTO_INCREMENT,
              `live_id` bigint unsigned NOT NULL,
              `live_status` tinyint unsigned NOT NULL,
              `room_id` bigint unsigned NOT NULL,
              `num` int unsigned NOT NULL,
              `user_uid` int unsigned NOT NULL,
              `user_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
              `guard_type` int unsigned DEFAULT NULL,
              `UUID` varchar(255) NOT NULL, 
              `create_time` datetime NOT NULL,
              PRIMARY KEY (`id`),
              UNIQUE KEY `search_id` (`id`) USING BTREE,
              KEY `search_live` (`live_id`,`live_status`) USING BTREE,
              KEY `search_room_id` (`room_id`) USING BTREE,
              KEY `search_uid` (`user_uid`) USING BTREE
              ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            """
        await self._execute(sql)

        return f'{info.table_name}_guard'

    async def _insert(self, msg: GuardMsg, info: BasicInfo):
        sql = f"""
                INSERT INTO {info.table_name}_guard 
                VALUES (
                    NULL, 
                    {info.live_id}, 
                    {info.live_status}, 
                    {info.room_id}, 
                    {msg.num}, 
                    {msg.user.uid}, 
                    '{msg.user.name}', 
                    {msg.guardType.value}, 
                    '{msg.UUID}', 
                    {info.create_time}
                );
                """

        await self._execute(sql)
