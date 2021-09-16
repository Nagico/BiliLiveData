#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : RedisConfig.py
# @Time     : 2021/9/16 21:26
# @Author   : NagisaCo
from Configer.Config.IConfig import IConfig


class RedisConfig(IConfig):
    def __init__(self):
        super().__init__(
            section='redis',
            default_dict=
            {
                'host': (str, 'localhost'),
                'password': (str, ''),
                'port': (int, 6379),
                'db': (int, 2)
            }
        )