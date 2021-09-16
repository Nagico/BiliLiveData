#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : MySQLConfig.py
# @Time     : 2021/9/16 21:24
# @Author   : NagisaCo
from Configer.Config.IConfig import IConfig


class MySQLConfig(IConfig):
    def __init__(self):
        super().__init__(
            section='mysql',
            default_dict=
            {
                'host': (str, "localhost"),
                'port': (int, 3306),
                'user': (str, "bili_live_data"),
                'password': (str, "bili_live_data"),
                'db': (str, "bili_live_data")
            }
        )