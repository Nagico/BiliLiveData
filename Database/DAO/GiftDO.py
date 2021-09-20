#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : GiftDO.py
# @Time     : 2021/9/7 16:55
# @Author   : NagisaCo
from BiliLive.Msg.GiftMsg import GiftMsg
from Database.DAO.MsgDO import MsgDO, BasicInfo


class GiftDO(MsgDO):
    async def _create_new_table(self, info: BasicInfo):
        sql = f"""
            CREATE TABLE `{info.table_name}_gift` (
              `id` bigint unsigned NOT NULL AUTO_INCREMENT,
              `live_id` bigint unsigned NOT NULL,
              `live_status` tinyint unsigned NOT NULL,
              `room_id` bigint unsigned NOT NULL,
              `action` varchar(255) NOT NULL,
              `coin_type` tinyint unsigned NOT NULL,
              `gift_name` varchar(255) NOT NULL,
              `num` int unsigned NOT NULL,
              `total_coin` int unsigned NOT NULL,
              `tid` bigint unsigned NOT NULL,
              `user_uid` int unsigned NOT NULL,
              `user_name` varchar(255) NOT NULL,
              `medal_name` varchar(255) DEFAULT NULL,
              `medal_liver_name` varchar(255) DEFAULT NULL,
              `medal_level` int unsigned DEFAULT NULL,
              `medal_guard_type` int unsigned DEFAULT NULL,
              `medal_lighting` tinyint unsigned DEFAULT NULL,
              `UUID` varchar(255) NOT NULL, 
              `create_time` datetime NOT NULL,
              PRIMARY KEY (`id`),
              UNIQUE KEY `search_id` (`id`),
              UNIQUE KEY `search_tid` (`tid`),
              KEY `search_live` (`live_id`,`live_status`),
              KEY `search_room_id` (`room_id`),
              KEY `search_uid` (`user_uid`)
              ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            """
        await self._execute(sql)

    async def _insert(self, msg: GiftMsg, info: BasicInfo):
        if msg.user.medal is None:
            medal_name = medal_liver_name = medal_level = medal_guard_type = medal_lighting = 'NULL'
        else:
            medal_name = self._check_null_str(msg.user.medal.cardName)
            medal_liver_name = self._check_null_str(msg.user.medal.liverName)
            medal_level = self._check_null(msg.user.medal.level)
            medal_guard_type = self._check_null(msg.user.medal.guardType.value)
            medal_lighting = self._check_null(int(msg.user.medal.lighting))

        sql = f"""
        INSERT INTO {info.table_name}_gift 
        VALUES(
        NULL, 
            {info.live_id}, 
            {info.live_status}, 
            {info.room_id}, 
            '{msg.action}', 
            {msg.coin_type.value}, 
            '{msg.gift.giftName}', 
            {msg.num}, 
            {msg.total_coin}, 
            {msg.tid}, 
            {msg.user.uid}, 
            '{msg.user.name}', 
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
