#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : GiftMsg.py
# @Time     : 2021/8/26 13:34
# @Author   : NagisaCo
from BiliLive.Msg.Msg import Msg
from BiliLive.Msg.Info.Gift import Gift, BlindGift, CoinType
from BiliLive.Msg.Info.User import UserBasic, Medal
from BiliLive.Msg.Info.Guard import GuardType


class GiftMsg(Msg):
    """
    礼物消息
    """
    def __init__(self, event):
        super().__init__(event)
        data = event.get('data').get('data')
        self.tid = data.get('tid')
        self.timestamp = data.get('timestamp')*1000
        self.action = data.get('action')

        blindGift = None
        if data.get('blind_gift'):
            blindGift = BlindGift(data.get('blind_gift').get('blind_gift_config_id'),
                                  data.get('blind_gift').get('original_gift_id'),
                                  data.get('blind_gift').get('original_gift_name'))

        self.gift = Gift(data.get('giftId'), data.get('giftName'), data.get('giftType'),
                         CoinType[data.get('coin_type')], data.get('price'),
                         data.get('discount_price'), blindGift)

        medal = None
        if data.get('medal_info'):
            medalInfo = data.get('medal_info')
            medal = Medal(medalInfo.get('medal_level'), medalInfo.get('medal_name'),
                          medalInfo.get('anchor_uname'), medalInfo.get('anchor_roomid'),
                          bool(medalInfo.get('is_lighted')),
                          GuardType(medalInfo.get('guard_level')))

        self.user = UserBasic(data.get('uid'), data.get('uname'), medal)
        self.num = data.get('num')
        self.coin_type = CoinType[data.get('coin_type')]
        self.total_coin = data.get('total_coin')
