#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : LoguruConfig.py
# @Time     : 2021/9/20 21:58
# @Author   : NagisaCo
from typing import List

from Configer.Config.IConfig import IConfig


class LoguruConfig(IConfig):
    def __init__(self, file_name: str = ''):
        super().__init__(
            section='loguru',
            default_dict=
            {
                'cmd_level': (str, 'DEBUG'),
                'enable_file_log': (bool, True),
                'file_name': (str, file_name),
                'file_level': (str, 'INFO')
            }
        )