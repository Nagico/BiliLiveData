#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : Logger.py
# @Time     : 2021/9/20 22:10
# @Author   : NagisaCo
import os.path
import sys
from loguru import logger


class Logger(object):
    def __init__(self):
        logger.remove()

    def set_cmd(self, level: str):
        logger.add(sys.stderr, level=level.upper())

    def set_file(self, file_name: str, level):
        if file_name != '':
            logger.add('log/'+os.path.splitext(file_name)[0]+'_{time}'+os.path.splitext(file_name)[1], rotation='1 day', level=level.upper())
