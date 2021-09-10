#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : UUID.py
# @Time     : 2021/8/29 17:41
# @Author   : NagisaCo
import os
import sys


class ClassPropertyDescriptor(object):

    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        return self.fget.__get__(obj, klass)()

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError("can't msg_info_dict attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self


def classproperty(func):
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)

    return ClassPropertyDescriptor(func)


class UUID(object):
    _uuid = ""

    @classproperty
    def uuid(cls):
        if UUID._uuid == "":
            UUID._uuid = UUID.__generate_uuid()
        return UUID._uuid

    @staticmethod
    def __generate_uuid():
        uuid = ""
        if sys.platform == 'win32':
            uuid = os.popen('wmic csproduct get UUID').read()

            uuid = uuid.strip().replace('\n', '').replace('\r', '').split(" ")
            uuid = uuid[len(uuid) - 1]
        if sys.platform == 'linux':
            uuid = os.popen('dmidecode -t system | grep UUID').read()
            uuid = uuid.strip().split(" ")
            uuid = uuid[len(uuid) - 1]

        if uuid == "":
            from uuid import uuid1
            uuid = str(uuid1()).upper()

        return uuid
