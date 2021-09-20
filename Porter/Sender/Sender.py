#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : Sender.py
# @Time     : 2021/8/27 15:32
# @Author   : NagisaCo
import asyncio
import signal
from loguru import logger

from Porter.Sender.Container import Container
from Database.RabbitMQ import RabbitMQ


class Sender(object):
    def __init__(self, container: Container, mq: RabbitMQ):
        self.container = container
        self.mq = mq

        @self.container.send
        async def send(data):
            await self.send(data)

        def stop(signum, frame):
            asyncio.create_task(self.__quit())

        signal.signal(signal.SIGINT, stop)  # 由Interrupt Key产生，通常是CTRL+C或者DELETE产生的中断
        signal.signal(signal.SIGTERM, stop)

    async def __quit(self):
        print("Canceling...")
        if len(self.container.data) != 0:
            await self.container.send_all()
        await self.mq.disconnect()

        raise KeyboardInterrupt("KeyboardInterrupt")

    async def init(self):
        await self.mq.connect()

    async def send(self, data):
        import base64
        logger.debug(f'Sending data\n{base64.b64encode(data).decode(encoding="utf-8")}')
        await asyncio.sleep(0.05)
        await self.mq.send(data)
        logger.info(f'Send success. len: {len(data)}')
