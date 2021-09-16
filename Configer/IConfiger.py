#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : IConfiger.py
# @Time     : 2021/9/16 16:15
# @Author   : NagisaCo
import configparser
import os
from typing import List, Dict

import Configer.ConfigException


class IConfiger(object):
    def __init__(self, config_file: str, config_list: List):
        self.config_file = config_file
        self.config_list = config_list
        self.config = configparser.ConfigParser()

        for item in self.config_list:
            item.set_configparser(self.config)

        self.config_dict = None

        if os.path.exists(self.config_file):
            try:
                self.config.read(self.config_file, encoding="utf-8")
            except configparser.ParsingError:
                self._init_all()
                raise Configer.ConfigException.FileNotFoundException(f'file {config_file} not found, already create '
                                                                     f'default file')
        else:
            self._init_all()
            raise Configer.ConfigException.FileNotFoundException(f'file {config_file} not found, already create '
                                                                 f'default file')

    def get_config(self) -> Dict[str, Dict[str, str or int or float or bool or List]]:
        if self.config_dict is None:
            config_dict = {}
            fail = []
            for item in self.config_list:
                try:
                    config_dict.update(item.get_config())
                except Configer.ConfigException.ConfigReadException as e:
                    fail.append(e.msg)

            if fail:
                self._store_file()
                raise Configer.ConfigException.ConfigReadException('\n'.join(fail))

            self.config_dict = config_dict

        return self.config_dict

    def _init_all(self):
        for item in self.config_list:
            item.init_config()

        self._store_file()

    def _store_file(self):
        with open(self.config_file, "w", encoding="utf-8") as f:
            self.config.write(f)
