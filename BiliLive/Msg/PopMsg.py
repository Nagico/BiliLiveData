#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : PopMsg.py
# @Time     : 2021/8/26 19:00
# @Author   : NagisaCo
from BiliLive.Msg.Msg import Msg


class PopMsg(Msg):
    def __init__(self, event):
        super().__init__(event)
        self.popularity = event.get('data')
