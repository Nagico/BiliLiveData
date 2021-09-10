#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : User.py
# @Time     : 2021/8/26 11:16
# @Author   : NagisaCo
from enum import Enum, unique
from BiliLive.Msg.Info.Guard import GuardType


@unique
class VipType(Enum):
    """
    vip类型

    NORMAL = 0 一般用户

    VIP = 1 VIP

    SVIP = 2 SVIP
    """
    NORMAL = 0
    VIP = 1
    SVIP = 2


class Medal(object):
    """
    当前粉丝牌信息
    """
    def __init__(self, level: int, name: str, liverName: str, liverRoomId: int,
                 lighting: bool, guardType: GuardType):
        self.level = level
        """
        粉丝牌等级
        """
        self.cardName = name
        """
        粉丝牌名
        """
        self.liverName = liverName
        """
        所属主播名
        """
        self.liverRoomId = liverRoomId
        """
        所属主播房间ID
        """
        self.lighting = lighting
        """
        是否点亮
        """
        self.guardType = GuardType(guardType)
        """
        粉丝牌舰队图标类型
        """


class UserBasic(object):
    """
    用户基本信息
    """
    def __init__(self, uid: int, name: str, medal: Medal = None):
        self.uid = uid
        self.name = name
        self.medal = medal


class UserDetail(UserBasic):
    """
    用户详细信息
    """
    def __init__(self, uid: int, name: str, roomAdmin: bool,
                 vip: VipType, guard: GuardType, level: int, medal: Medal = None):
        super().__init__(uid, name, medal)
        self.roomAdmin = roomAdmin
        self.vip = vip
        self.guard = guard
        self.level = level
