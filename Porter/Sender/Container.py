#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : Container.py
# @Time     : 2021/8/27 18:57
# @Author   : NagisaCo
import asyncio
import hashlib
import json
import lzma
import pickle
from time import time
from typing import Coroutine

from Porter.UUID import UUID


class Unit(object):
    def __init__(self, obj):
        md5 = ""
        if hasattr(obj, 'data'):
            md5 = hashlib.md5(json.dumps(obj.data).encode(encoding='utf-8')).hexdigest()
            del obj.data
        self.data = pickle.dumps(obj)
        self.md5 = md5


class Container(object):
    def __init__(self, MAX_TIME: int = 300, MAX_NUM: int = 200):
        self.MAX_TIME = MAX_TIME
        self.MAX_NUM = MAX_NUM
        self.data = []
        self.createTime = 0
        self.endTime = 0
        self.callback = None

    async def append(self, obj):
        if not self.data:
            self.createTime = int(time())
        self.endTime = int(time())
        unit = Unit(obj)
        self.data.append(unit)
        print(len(self.data))
        if self.endTime - self.createTime > self.MAX_TIME or len(self.data) >= self.MAX_NUM:
            await self.__pack()

    async def send_all(self):
        if len(self.data) != 0:
            await self.__pack()

    def __clear(self):
        self.data = []
        self.createTime = 0
        self.endTime = 0

    def send(self, func: Coroutine):
        """
        注册回调函数
        """
        self.callback = func
        return func

    async def __pack(self):
        data = pickle.dumps({
            'data': self.data,
            'UUID': UUID.uuid,
            'time': int(time())
        })
        compressed = lzma.compress(data)
        self.__clear()
        import base64
        print(base64.b64encode(compressed).decode(encoding='utf-8'))
        await asyncio.create_task(self.callback(compressed))
