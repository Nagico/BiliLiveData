#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : AnalysorConfiger.py
# @Time     : 2021/9/16 21:28
# @Author   : NagisaCo
from Configer.IConfiger import IConfiger
from Configer.Config.Database.MySQLConfig import MySQLConfig
from Configer.Config.Database.RedisConfig import RedisConfig
from Configer.Config.Database.RabbitMQConfig import RabbitMQConfig


class AnalysorConfiger(IConfiger):
    def __init__(self, config_file: str = 'Analysor.conf'):
        super().__init__(config_file, [MySQLConfig(), RedisConfig(), RabbitMQConfig()])