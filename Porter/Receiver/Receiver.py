#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : Receiver.py
# @Time     : 2021/8/28 9:59
# @Author   : NagisaCo
import asyncio
import signal

from Porter.Receiver.Processor import Processor
from Database.RabbitMQ import RabbitMQ


class Receiver(object):
    def __init__(self, processor: Processor, mq: RabbitMQ):
        self.processor = processor
        self.mq = mq
        self.cnt = 0
        self.status = False

        def stop(signum, frame):
            asyncio.create_task(self.__quit())

        signal.signal(signal.SIGINT, stop)  # 由Interrupt Key产生，通常是CTRL+C或者DELETE产生的中断
        signal.signal(signal.SIGTERM, stop)

    async def __quit(self):
        print("Canceling...")
        await self.mq.disconnect()

        while True:
            if not self.status:
                break
            await asyncio.sleep(0.1)

        await self.processor.mysql.disconnect()
        await self.processor.redis.disconnect()
        exit("KeyboardInterrupt")

    async def init(self):
        await self.processor.init()
        await self.mq.connect()

    async def run(self):
        while True:
            data = await self.mq.get()
            self.status = True
            self.cnt += 1
            print(self.cnt)
            await self.processor.store(data)
            self.status = False
