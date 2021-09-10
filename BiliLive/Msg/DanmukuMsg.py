#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : DanmukuMsg.py
# @Time     : 2021/8/25 17:29
# @Author   : NagisaCo
from BiliLive.Msg.Msg import Msg
import BiliLive.Msg.Info.User as User


class DanmukuMsg(Msg):
    """
    弹幕消息
    """
    def __init__(self, event):
        super().__init__(event)
        info = event.get('data').get('info')
        self.color = info[0][3]
        self.timestamp = info[0][4]
        self.content = info[1]

        uid = info[2][0]
        name = info[2][1]
        roomAdmin = bool(info[2][2])

        vip = User.VipType.NORMAL
        if info[2][3] == 1:
            if info[2][4] == 0:
                vip = User.VipType.VIP
            elif info[2][4] == 1:
                vip = User.VipType.SVIP

        guard = User.GuardType(info[7])

        level = info[4][0]

        medal = None
        if info[3]:
            card = info[3]
            medal = User.Medal(card[0], card[1], card[2], card[3], bool(card[11]), User.GuardType(card[10]))

        self.user = User.UserDetail(uid, name, roomAdmin, vip, guard, level, medal)
