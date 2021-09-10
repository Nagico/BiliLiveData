#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : Analysor.py
# @Time     : 2021/9/5 17:55
# @Author   : NagisaCo
import asyncio

from Database.MySQL import MySQL
from Database.Redis import Redis
from Database.RabbitMQ import RabbitMQ
from Porter.Receiver.Processor import Processor
from Porter.Receiver.Receiver import Receiver


async def start():
    mysql = MySQL(  # mysql数据库配置
        host="localhost",
        port=3306,
        user="bili_live_data",
        password="bili_live_data",
        db="bili_live_data"
    )
    redis = Redis(  # redis数据库配置
        host='localhost',
        port=6379,
        db=2
    )
    mq = RabbitMQ(  # 消息队列配置
        host="localhost",
        port=5672,
        username="BiliLiveData",
        password="BiliLiveData",
        virtualhost="BiliLiveData",
        queue_name="Data",
        ssl=False
    )

    processor = Processor(redis, mysql)

    receiver = Receiver(processor, mq)

    await receiver.init()
    await receiver.run()


if __name__ == "__main__":
    asyncio.run(start())
