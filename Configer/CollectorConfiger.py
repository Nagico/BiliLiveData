#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : CollectorConfiger.py
# @Time     : 2021/9/16 17:39
# @Author   : NagisaCo
from Configer.IConfiger import IConfiger
from Configer.Config.ContainerConfig import ContainerConfig
from Configer.Config.ListenerConfig import ListenerConfig
from Configer.Config.Database.RabbitMQConfig import RabbitMQConfig


class CollectorConfiger(IConfiger):
    def __init__(self, config_file: str = 'Collector.conf'):
        super().__init__(config_file, [ContainerConfig(), ListenerConfig(), RabbitMQConfig()])

