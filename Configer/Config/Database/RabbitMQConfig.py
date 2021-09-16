#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : RabbitMQConfig.py
# @Time     : 2021/9/16 17:37
# @Author   : NagisaCo
from Configer.Config.IConfig import IConfig


class RabbitMQConfig(IConfig):
    def __init__(self):
        super().__init__(
            section='rabbitmq',
            default_dict=
            {
                'host': (str, "localhost"),
                'port': (int, 5672),
                'username': (str, 'BiliLiveData'),
                'password': (str, 'BiliLiveData'),
                'virtualhost': (str, '/'),
                'queue_name': (str, "Data"),
                'ssl': (bool, False)
            }
        )
