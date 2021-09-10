#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : StatusDO.py
# @Time     : 2021/9/6 17:17
# @Author   : NagisaCo
from BiliLive.Msg.Status import Status
from Database.DAO.MsgDO import MsgDO, BasicInfo


class StatusDO(MsgDO):
    async def _create_new_table(self, info: BasicInfo):
        async with self.connection.cursor() as cur:
            await cur.execute(f"""
                CREATE TABLE `{info.table_name}_status` (
              `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT 'status id',
              `live_id` bigint unsigned NOT NULL COMMENT 'live id',
              `room_id` int unsigned NOT NULL,
              `short_id` int unsigned NOT NULL,
              `uid` int unsigned NOT NULL COMMENT '主播uid',
              `username` varchar(255) NOT NULL COMMENT '主播昵称',
              `fans_count` int unsigned NOT NULL COMMENT '粉丝数',
              `fansclub_count` int unsigned DEFAULT NULL COMMENT '粉丝团人数',
              `guard_count` int unsigned NOT NULL COMMENT '舰长人数',
              `title` varchar(255) NOT NULL COMMENT '直播标题',
              `tags` varchar(255) DEFAULT NULL COMMENT '房间标签',
              `live_status` tinyint unsigned NOT NULL COMMENT '直播状态',
              `live_start_time` datetime DEFAULT NULL COMMENT '直播开始时间',
              `gold_rank_uid_list` varchar(255) DEFAULT NULL COMMENT '|分隔',
              `gold_rank_username_list` varchar(255) DEFAULT NULL COMMENT '|分隔',
              `gold_rank_score_list` varchar(255) DEFAULT NULL COMMENT '|分隔',
              `area_name` varchar(255) NOT NULL,
              `parent_area_name` varchar(255) NOT NULL,
              `popularity` int unsigned NOT NULL COMMENT '人气值',
              `UUID` varchar(255) NOT NULL,
              `create_time` datetime NOT NULL COMMENT '获取时间',
              PRIMARY KEY (`id`),
              UNIQUE KEY `search_id` (`id`),
              KEY `search_room_id` (`room_id`) USING BTREE,
              KEY `search_uid` (`uid`) USING BTREE,
              KEY `search_live` (`live_id`,`live_status`) USING BTREE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            """)
            await self.connection.commit()

    async def _insert(self, msg: Status, info: BasicInfo):

        if msg.gold_rank:
            gold_rank_uid_list = None
            gold_rank_username_list = None
            gold_rank_score_list = None
            for item in msg.gold_rank:
                if gold_rank_uid_list is None and gold_rank_username_list is None and gold_rank_score_list is None:
                    gold_rank_uid_list = []
                    gold_rank_username_list = []
                    gold_rank_score_list = []
                gold_rank_uid_list.append(str(item['uid']))
                gold_rank_username_list.append(item['name'])
                gold_rank_score_list.append(item['score'])
            gold_rank_uid_str = '|'.join(gold_rank_uid_list)
            gold_rank_username_str = '|'.join(gold_rank_username_list)
            gold_rank_score_str = '|'.join(gold_rank_score_list)
        else:
            gold_rank_uid_str = None
            gold_rank_username_str = None
            gold_rank_score_str = None

        sql = f"INSERT INTO {info.table_name}_status " \
              f"VALUES (NULL, {info.live_id}, {info.room_id}, {msg.short_id}, {msg.uid}, " \
              f"'{msg.username}', {msg.fans_count}, {self._check_null(msg.fansclub_count)}, " \
              f"{msg.guard_count}, '{msg.title}', {self._check_null_str(msg.tags)}, {info.live_status}, " \
              f"{self.t2d(msg.live_start_time)}, {self._check_null_str(gold_rank_uid_str)}, " \
              f"{self._check_null_str(gold_rank_username_str)}, {self._check_null_str(gold_rank_score_str)}, " \
              f"'{msg.area_name}', '{msg.parent_area_name}', {msg.popularity}, '{msg.UUID}', {info.create_time});"

        await self._execute(sql)
