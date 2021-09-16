#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : ListenerConfig.py
# @Time     : 2021/9/16 19:01
# @Author   : NagisaCo
from typing import List

from Configer.Config.IConfig import IConfig


class ListenerConfig(IConfig):
    def __init__(self):
        super().__init__(
            section='listener',
            default_dict=
            {
                'room_id_list': (List[int], [21919321, 21919321])
            }
        )
