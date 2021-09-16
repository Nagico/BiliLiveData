#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : Status.py
# @Time     : 2021/8/26 22:22
# @Author   : NagisaCo
from time import time
from BiliLive.Msg.Info.User import GuardType


class Status(object):
    def __init__(self, data):
        self.fetchTime = int(round(time() * 1000))
        self.room_id = data.get('room_info').get('room_id')
        self.short_id = data.get('room_info').get('short_id')
        self.username = data.get('anchor_info').get('base_info').get('uname')
        self.uid = data.get('room_info').get('uid')
        self.fans_count = data.get('anchor_info').get('relation_info').get('attention')
        self.fansclub_count = None
        if data.get('anchor_info').get('medal_info'):
            self.fansclub_count = data.get('anchor_info').get('medal_info').get('fansclub')
        self.guard_count = data.get('guard_info').get('count')

        self.title = data.get('room_info').get('title')
        self.tags = data.get('room_info').get('tags')
        if data.get('room_info').get('live_status') == 1:
            self.live_status = True
        else:
            self.live_status = False
        self.live_start_time = data.get('room_info').get('live_start_time')
        self.popularity = data.get('room_info').get('online')

        self.gold_rank = None
        if data.get('online_gold_rank_info_v2').get('list'):
            self.gold_rank = []
            for item in data.get('online_gold_rank_info_v2').get('list'):
                userinfo = {
                    'uid': item.get('uid'),
                    'name': item.get('uname'),
                    'score': item.get('score'),
                    'rank': item.get('rank'),
                    'guard_level': GuardType(item.get('guard_level'))
                }
                self.gold_rank.append(userinfo)

        self.area_id = data.get('room_info').get('area_id')
        self.area_name = data.get('room_info').get('area_name')
        self.parent_area_id = data.get('room_info').get('parent_area_id')
        self.parent_area_name = data.get('room_info').get('parent_area_name')



