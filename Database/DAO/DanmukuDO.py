#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : DanmukuDO.py
# @Time     : 2021/9/7 15:53
# @Author   : NagisaCo
from BiliLive.Msg.DanmukuMsg import DanmukuMsg
from Database.DAO.MsgDO import MsgDO, BasicInfo


class DanmukuDO(MsgDO):
    async def _create_new_table(self, info: BasicInfo):
        async with self.connection.cursor() as cur:
            await cur.execute(f"""
                CREATE TABLE `{info.table_name}_danmuku` (
                  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
                  `live_id` bigint unsigned NOT NULL,
                  `live_status` tinyint unsigned NOT NULL,
                  `room_id` int unsigned NOT NULL,
                  `color` int unsigned NOT NULL,
                  `content` varchar(255) NOT NULL,
                  `user_uid` int unsigned NOT NULL,
                  `user_username` varchar(255) NOT NULL,
                  `user_level` int unsigned NOT NULL,
                  `user_room_admin` tinyint unsigned NOT NULL,
                  `user_vip_type` int unsigned NOT NULL,
                  `user_guard_type` int unsigned NOT NULL,
                  `medal_name` varchar(255) DEFAULT NULL,
                  `medal_liver_name` varchar(255) DEFAULT NULL,
                  `medal_level` int unsigned DEFAULT NULL,
                  `medal_guard_type` int unsigned DEFAULT NULL,
                  `medal_lighting` tinyint unsigned DEFAULT NULL,
                  `UUID` varchar(255) NOT NULL, 
                  `create_time` datetime NOT NULL,
                  PRIMARY KEY (`id`),
                  UNIQUE KEY `search_id` (`id`),
                  KEY `search_room_id` (`room_id`),
                  KEY `search_uid` (`user_uid`),
                  KEY `search_live` (`live_id`,`live_status`) USING BTREE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                """)
            await self.connection.commit()

    async def _insert(self, msg: DanmukuMsg, info: BasicInfo):
        if msg.user.medal is None:
            medal_name = medal_liver_name = medal_level = medal_guard_type = medal_lighting = 'NULL'
        else:
            medal_name = self._check_null_str(msg.user.medal.cardName)
            medal_liver_name = self._check_null_str(msg.user.medal.liverName)
            medal_level = self._check_null(msg.user.medal.level)
            medal_guard_type = self._check_null(msg.user.medal.guardType.value)
            medal_lighting = self._check_null(int(msg.user.medal.lighting))

        sql = f"""
        INSERT INTO {info.table_name}_danmuku 
        VALUES (
            NULL, 
            {info.live_id}, 
            {info.live_status}, 
            {info.room_id}, 
            {msg.color}, 
            '{msg.content}', 
            {msg.user.uid}, 
            '{msg.user.name}', 
            {msg.user.level}, 
            {int(msg.user.roomAdmin)}, 
            {msg.user.vip.value}, 
            {msg.user.guard.value}, 
            {medal_name}, 
            {medal_liver_name}, 
            {medal_level}, 
            {medal_guard_type}, 
            {medal_lighting}, 
            '{msg.UUID}', 
            {info.create_time}
        );
        """

        await self._execute(sql)
