#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : RabbitMQ.py
# @Time     : 2021/9/9 17:30
# @Author   : NagisaCo
import aio_pika
import base64
from loguru import logger


class RabbitMQ(object):
    def __init__(self, host: str = "localhost", port: int = 5672,
                 username: str = 'BiliLiveData', password: str = 'BiliLiveData',
                 virtualhost: str = '/', queue_name: str = "Data", ssl: bool = False):
        self.host = host
        logger.debug(f'Get config [host]: {self.host}')
        self.port = port
        logger.debug(f'Get config [port]: {self.port}')
        self.username = username
        logger.debug(f'Get config [username]: {self.username}')
        self.password = password
        logger.debug(f'Get config [password]: *length*{self.password}')
        self.virtualhost = virtualhost
        logger.debug(f'Get config [virtualhost]: {self.virtualhost}')
        self.queue_name = queue_name
        logger.debug(f'Get config [queue_name]: {self.queue_name}')
        self.ssl = ssl
        logger.debug(f'Get config [ssl]: {self.ssl}')
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
        logger.info('Connected')

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
                    logger.debug(f'Get message\n{base64.b64encode(message.body).decode(encoding="utf-8")}')
                    return message.body
