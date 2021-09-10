#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : SCMsg.py
# @Time     : 2021/8/26 16:09
# @Author   : NagisaCo
from BiliLive.Msg.Info.User import UserDetail, VipType, Medal
from BiliLive.Msg.Info.Gift import Gift, CoinType
from BiliLive.Msg.Msg import Msg
from BiliLive.Msg.Info.Guard import GuardType


class SCMsg(Msg):
    def __init__(self, event):
        super().__init__(event)
        data = event.get('data').get('data')
        self.id = data.get('id')
        self.message = data.get('message')
        self.coin_type = CoinType['gold']
        self.total_coin = data.get('rate')*data.get('price')
        self.timestamp = data.get('ts')*1000
        self.time = data.get('time')
        self.start_time = data.get('start_time')
        self.end_time = data.get('end_time')

        vip = VipType.NORMAL
        if data.get('user_info').get('is_vip') == 1:
            if data.get('user_info').get('is_svip') == 0:
                vip = VipType.VIP
            elif data.get('user_info').get('is_svip') == 1:
                vip = VipType.SVIP

        medal = None
        if data.get('medal_info'):
            card = data.get('medal_info')
            medal = Medal(card.get("medal_level"), card.get("medal_name"), card.get("anchor_uname"),
                          card.get("anchor_roomid"), bool(card.get("is_lighted")),
                          GuardType(card.get("guard_level")))

        self.user = UserDetail(data.get('uid'), data.get('user_info').get('uname'),
                               bool(data.get('user_info').get('manager')), vip,
                               GuardType(data.get('user_info').get('guard_level')),
                               data.get('user_info').get('user_level'),
                               medal)

        self.gift = Gift(data.get('gift').get('gift_id'), data.get('gift').get('gift_name'), 0,
                         CoinType['gold'], data.get('rate'), data.get('rate'))
