#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : Collector.py
# @Time     : 2021/8/25 11:44
# @Author   : NagisaCo
import asyncio
import click

from BiliLive.LiveListener import LiveListener
from Porter.Sender.Container import Container
from Porter.Sender.Sender import Sender
from Database.RabbitMQ import RabbitMQ
from Configer.CollectorConfiger import CollectorConfiger
from Configer.ConfigException import ConfigException


async def start(config_file: str):
    try:
        configer = CollectorConfiger(config_file)

        config = configer.get_config()
    except ConfigException as e:
        print(f'[config] {e.msg}')
        return

    container = Container(  # 消息存放容器配置
        MAX_TIME=config['container']['max_time'],  # 容纳消息的时间跨度超过该值则发送
        MAX_NUM=config['container']['max_num']  # 容纳消息的数量超过该值则发送
    )
    mq = RabbitMQ(  # 消息队列配置
        host=config['rabbitmq']['host'],
        port=config['rabbitmq']['port'],
        username=config['rabbitmq']['username'],
        password=config['rabbitmq']['password'],
        virtualhost=config['rabbitmq']['virtualhost'],
        queue_name=config['rabbitmq']['queue_name'],
        ssl=config['rabbitmq']['ssl']
    )

    sender = Sender(container, mq)

    await sender.init()

    tasks = []
    for room_id in set(config['listener']['room_id_list']):
        live_room = LiveListener(room_id, container)
        tasks.append(asyncio.create_task(live_room.start()))

    done = await asyncio.wait(tasks)

    return done


@click.command()
@click.option('--config', default='Collector.conf', help='your config file')
def main(config: str):
    asyncio.run(start(config))


if __name__ == "__main__":
    main()

