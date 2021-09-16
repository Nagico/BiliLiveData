#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @File     : IConfig.py
# @Time     : 2021/9/16 16:24
# @Author   : NagisaCo
import configparser
import json
from typing import List, Tuple, Dict, Type

import Configer.ConfigException


class IConfig(object):
    def __init__(self, section: str, default_dict: Dict[str, Tuple[type or Type, str or int or float or bool or List]]):
        self.config = None
        self.section = section
        self.default_dict = default_dict
        self.config_dict = None

    def set_configparser(self, config: configparser.ConfigParser):
        self.config = config

    def init_config(self):
        if self.config.has_section(self.section):
            self.config.remove_section(self.section)
        self.config.add_section(self.section)

        for key, value in self.default_dict.items():
            self.config.set(self.section, key, str(value[1]))

    def get_config(self) -> Dict[str, Dict[str, str or int or float or bool or List]]:
        if self.config_dict is None:
            try:
                self.config_dict = self._get_config_from_file()
            except (configparser.NoOptionError, configparser.NoSectionError, configparser.DuplicateOptionError):
                self.init_config()
                raise Configer.ConfigException.ConfigReadException(f'Section {self.section} read failed, already '
                                                                   f'restore default setting. ')

        return self.config_dict

    def _get_config_from_file(self) -> Dict[str, Dict[str, str or int or float or bool or List]]:
        config_dict = {}
        for key, value in self.default_dict.items():
            _type, _value = value

            value_get = _value

            try:
                if self.config.get(self.section, key) != '':
                    if _type == str:
                        value_get = self.config.get(self.section, key)
                    elif _type == int:
                        value_get = self.config.getint(self.section, key)
                    elif _type == float:
                        value_get = self.config.getfloat(self.section, key)
                    elif _type == bool:
                        value_get = self.config.getboolean(self.section, key)
                    elif _type == List[int]:
                        value_get = json.loads(self.config.get(self.section, key))
            except ValueError:
                value_get = _value

            config_dict.update({
                key: value_get
            })

        return {self.section: config_dict}

