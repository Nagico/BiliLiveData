#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : Gift.py
# @Time     : 2021/8/26 14:23
# @Author   : NagisaCo
from enum import Enum, unique


@unique
class CoinType(Enum):
    undefined = 0
    silver = 1
    gold = 2


class BlindGift(object):
    """
    盲盒类原礼物信息
    """
    def __init__(self, blind_gift_config_id: int,
                 original_gift_id: int, original_gift_name: str):
        self.blind_gift_config_id = blind_gift_config_id
        self.original_gift_id = original_gift_id
        self.original_gift_name = original_gift_name


class Gift(object):
    """
    礼物信息
    """
    def __init__(self, giftId: int, giftName: str, giftType: int, coin_type: CoinType,
                 price: int, discount_price: int, blind_gift: BlindGift = None):
        self.giftId = giftId
        self.giftName = giftName
        self.giftType = giftType
        self.coin_type = coin_type
        self.price = price
        self.discount_price = discount_price
        self.blind_gift = blind_gift

