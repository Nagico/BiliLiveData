#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : ConfigException.py
# @Time     : 2021/9/16 17:21
# @Author   : NagisaCo

class ConfigException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f'config read failed: {self.msg}'


class FileNotFoundException(ConfigException):
    pass


class ConfigReadException(ConfigException):
    pass
