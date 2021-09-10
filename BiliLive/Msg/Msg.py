#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : Msg.py
# @Time     : 2021/8/25 17:25
# @Author   : NagisaCo
from enum import Enum, unique
from time import time


class Msg(object):
    """
    消息基类
    """

    def __init__(self, event):
        """
        初始化

        :param event: 接收的json数据
        """
        self.roomDisplayId = event.get('room_display_id')
        self.roomRealId = event.get('room_real_id')
        self.type = MsgType[event.get('type')]
        self.fetchTime = int(round(time() * 1000))
        self.data = event.get('data')


@unique
class MsgType(Enum):
    """
    事件类型
    """
    UNDEFINED = 0
    """
    未定义
    """
    DANMU_MSG = 1
    """
    用户发送弹幕
    """
    SEND_GIFT = 2
    """
    礼物
    """
    COMBO_SEND = 3
    """
    礼物连击
    """
    GUARD_BUY = 4
    """
    续费大航海
    """
    SUPER_CHAT_MESSAGE = 5
    """
    醒目留言（SC）
    """
    SUPER_CHAT_MESSAGE_JPN = 6
    """
    醒目留言（带日语翻译）
    """
    WELCOME = 7
    """
    老爷进入房间
    """
    WELCOME_GUARD = 8
    """
    房管进入房间
    """
    NOTICE_MSG = 9
    """
    系统通知（全频道广播之类的）
    """
    PREPARING = 10
    """
    直播准备中
    """
    LIVE = 11
    """
    直播开始
    """
    ROOM_REAL_TIME_MESSAGE_UPDATE = 12
    """
    粉丝数等更新
    """
    ENTRY_EFFECT = 13
    """
    进场特效
    """
    ROOM_RANK = 14
    """
    房间排名更新
    """
    INTERACT_WORD = 15
    """
    用户进入直播间
    """
    ACTIVITY_BANNER_UPDATE_V2 = 16
    """
    好像是房间名旁边那个xx小时榜
    """
    VIEW = 17
    """
    直播间人气更新
    """
    DISCONNECT = 18
    """
    断开连接（传入连接状态码参数）
    """
    TIMEOUT = 19
    """
    心跳响应超时
    """