#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : Collector.py
# @Time     : 2021/8/25 11:44
# @Author   : NagisaCo
import asyncio
from typing import List

from BiliLive.LiveListener import LiveListener
from Porter.Sender.Container import Container
from Porter.Sender.Sender import Sender
from Database.RabbitMQ import RabbitMQ


async def start(room_id_list: List):
    container = Container(  # 消息存放容器配置
        MAX_TIME=300,  # 容纳消息的时间跨度超过该值则发送
        MAX_NUM=100  # 容纳消息的数量超过该值则发送
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

    sender = Sender(container, mq)

    await sender.init()

    tasks = []
    for room_id in room_id_list:
        live_room = LiveListener(room_id, container)
        tasks.append(asyncio.create_task(live_room.start()))

    done = await asyncio.wait(tasks)

    return done


if __name__ == "__main__":
    id_list = [21919321]
    asyncio.run(start(id_list))
