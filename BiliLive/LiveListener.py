#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : LiveListener.py
# @Time     : 2021/8/26 13:18
# @Author   : NagisaCo
from bilibili_api import live
from BiliLive.Msg.DanmukuMsg import DanmukuMsg
from BiliLive.Msg.GiftMsg import GiftMsg
from BiliLive.Msg.SCMsg import SCMsg
from BiliLive.Msg.GuardMsg import GuardMsg
from BiliLive.Msg.Status import Status


class LiveListener(object):
    def __init__(self, roomId, container):
        self.room = live.LiveRoom(roomId)
        self.ws = live.LiveDanmaku(roomId, False)
        self.container = container

        @self.ws.on('DANMU_MSG')
        async def on_danmaku(event):
            # 收到弹幕
            danmu = DanmukuMsg(event)
            print(f'[{danmu.user.guard.name}]{danmu.user.name}: {danmu.content}')
            await self.container.append(danmu)
            pass

        @self.ws.on('SEND_GIFT')
        async def on_gift(event):
            # 收到礼物
            gift = GiftMsg(event)
            print(f'[{gift.roomRealId}] {gift.user.name}: {gift.gift.giftName}*{str(gift.num)}')
            await self.container.append(gift)
            pass

        @self.ws.on('SUPER_CHAT_MESSAGE')
        async def on_sc(event):
            # 收到SC
            sc = SCMsg(event)
            print(f'[{sc.roomRealId}] {sc.user.name}: {sc.message} - {sc.time}s')
            await self.container.append(sc)
            pass

        @self.ws.on('GUARD_BUY')
        async def on_guard(event):
            # 舰队更新
            guard = GuardMsg(event)
            print(f'[{guard.roomRealId}] {guard.user.name}: {guard.guardType.name}')
            await self.container.append(guard)
            pass

        @self.ws.on('LIVE')
        @self.ws.on('PREPARING')
        @self.ws.on('VIEW')
        @self.ws.on('ROOM_CHANGE')
        async def on_status(event):
            data = await self.room.get_room_info()
            status = Status(data)
            print(f'[{status.room_id}] LIVE_STATUS: {status.live_status}|TITLE: {status.title}|POPULARITY: {status.popularity}|FANS: {status.fans_count}')
            await self.container.append(status)
            pass

    async def start(self):
        await self.ws.connect()

    async def stop(self):
        await self.ws.disconnect()
