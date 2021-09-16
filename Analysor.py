#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : Analysor.py
# @Time     : 2021/9/5 17:55
# @Author   : NagisaCo
import asyncio
import click

from Database.MySQL import MySQL
from Database.Redis import Redis
from Database.RabbitMQ import RabbitMQ
from Porter.Receiver.Processor import Processor
from Porter.Receiver.Receiver import Receiver
from Configer.AnalysorConfiger import AnalysorConfiger
from Configer.ConfigException import ConfigException


async def start(config_file: str):
    try:
        configer = AnalysorConfiger(config_file)

        config = configer.get_config()
    except ConfigException as e:
        print(f'[config] {e.msg}')
        return

    mysql = MySQL(  # mysql数据库配置
        host=config['mysql']['host'],
        port=config['mysql']['port'],
        user=config['mysql']['user'],
        password=config['mysql']['password'],
        db=config['mysql']['db']
    )
    redis = Redis(  # redis数据库配置
        host=config['redis']['host'],
        port=config['redis']['port'],
        password=config['redis']['password'],
        db=config['redis']['db']
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

    processor = Processor(redis, mysql)

    receiver = Receiver(processor, mq)

    await receiver.init()
    await receiver.run()


@click.command()
@click.option('--config', default='Analysor.conf', help='your config file')
def main(config: str):
    asyncio.run(start(config))


if __name__ == "__main__":
    main()
