#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : RabbitMQ.py
# @Time     : 2021/9/9 17:30
# @Author   : NagisaCo
import aio_pika


class RabbitMQ(object):
    def __init__(self, host: str = "localhost", port: int = 5672,
                 username: str = 'BiliLiveData', password: str = 'BiliLiveData',
                 virtualhost: str = '/', queue_name: str = "Data", ssl: bool = False):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.virtualhost = virtualhost
        self.queue_name = queue_name
        self.ssl = ssl
        self.connection = None
        self.channel = None
        self.queue = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(
            host=self.host,
            port=self.port,
            login=self.username,
            password=self.password,
            virtualhost=self.virtualhost,
            ssl=self.ssl
        )

        self.channel = await self.connection.channel()
        print("mq connected")

    async def disconnect(self):
        await self.connection.close()

    async def send(self, data):
        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=data,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=self.queue_name,
        )

    async def get(self):
        if self.queue is None:
            self.queue = await self.channel.declare_queue(self.queue_name, durable=True)
        async with self.queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    return message.body
