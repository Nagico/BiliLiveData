#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : ContainerConfig.py
# @Time     : 2021/9/16 16:29
# @Author   : NagisaCo
from Configer.Config.IConfig import IConfig


class ContainerConfig(IConfig):
    def __init__(self):
        super().__init__(
            section='container',
            default_dict=
            {
                'max_time': (int, 300),
                'max_num': (int, 200)
            }
        )
