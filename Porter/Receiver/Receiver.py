#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : Receiver.py
# @Time     : 2021/8/28 9:59
# @Author   : NagisaCo
import asyncio
import signal
import base64
from loguru import logger

from Porter.Receiver.Processor import Processor
from Database.RabbitMQ import RabbitMQ


class Receiver(object):
    def __init__(self, processor: Processor, mq: RabbitMQ):
        self.processor = processor
        self.closed = True
        self.mq = mq
        self.cnt = 0
        self.status = False

        def stop(signum, frame):
            asyncio.create_task(self.__quit())

        signal.signal(signal.SIGINT, stop)  # 由Interrupt Key产生，通常是CTRL+C或者DELETE产生的中断
        signal.signal(signal.SIGTERM, stop)

    async def __quit(self):
        logger.warning("Canceling...")
        self.closed = True


        while True:
            if not self.status:
                break
            await asyncio.sleep(0.1)

        await asyncio.sleep(0.1)
        await self.mq.disconnect()
        await asyncio.sleep(0.1)
        await self.processor.redis.disconnect()
        await asyncio.sleep(0.1)
        await self.processor.mysql.disconnect()

        raise KeyboardInterrupt("KeyboardInterrupt")

    async def init(self):
        await self.processor.init()
        await self.mq.connect()
        self.closed = False

    async def run(self):
        self.status = True
        while True:
            if self.closed:
                self.status = False
                await asyncio.sleep(1)
                break
            data = await self.mq.get()
            self.cnt += 1
            logger.info(f'Package received: {self.cnt}')
            logger.debug(f'Package content\n{base64.b64encode(data).decode(encoding="utf-8")}')
            await self.processor.store(data)
