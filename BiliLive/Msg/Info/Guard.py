#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : Guard.py
# @Time     : 2021/8/26 15:36
# @Author   : NagisaCo
from enum import Enum, unique


@unique
class GuardType(Enum):
    """
    舰队类型

    NORMAL = 0 非舰队

    SOUTOKU = 1 总督

    TEITOKU = 2 提督

    CAPTAIN = 3 舰长
    """
    NORMAL = 0
    SOUTOKU = 1
    TEITOKU = 2
    CAPTAIN = 3