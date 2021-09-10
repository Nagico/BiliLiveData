#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : GuardMsg.py
# @Time     : 2021/8/26 15:40
# @Author   : NagisaCo
from BiliLive.Msg.Msg import Msg
from BiliLive.Msg.Info.User import UserBasic
from BiliLive.Msg.Info.Guard import GuardType


class GuardMsg(Msg):
    """
    舰队消息
    """
    def __init__(self, event):
        super().__init__(event)
        data = event.get('data').get('data')
        self.gift_id = data.get('gift_id')
        self.gift_name = data.get('gift_name')
        self.guardType = GuardType(data.get('guard_level'))
        self.num = data.get('num')
        self.timestamp = data.get('start_time')*1000

        self.user = UserBasic(data.get('uid'), data.get('username'))
