# coding=utf-8

import logging
import os
import pickle
import uuid
from enum import Enum
from typing import Dict, Optional, Tuple

import yaml
from ehforwarderbot import Chat, Message, Middleware, MsgType, coordinator, utils
from ehforwarderbot.chat import GroupChat, SelfChatMember
from ehforwarderbot.exceptions import EFBException

from .__version__ import __version__ as version


class WorkFilter(Enum):
    black_person = "black_persons"
    white_person = "white_persons"
    black_group = "black_groups"
    white_group = "white_groups"


class FilterMiddleware(Middleware):
    middleware_id: str = "zerorigin.filter"
    middleware_name: str = "Filter Middleware"
    __version__: str = version

    mappings: Dict[Tuple[str, str], str] = {}
    chat: Chat = None

    def __init__(self, instance_id: str = None):
        super().__init__(instance_id)

        storage_path = utils.get_data_path(self.middleware_id)
        config_path = utils.get_config_path(self.middleware_id)

        if not os.path.exists(storage_path):
            os.makedirs(storage_path)

        if not os.path.exists(config_path):
            raise EFBException("Filter middleware is not configured.")
        else:
            config = yaml.safe_load(open(config_path, encoding="UTF-8"))
            self.config_version = 0

            self.match_mode = config.get("match_mode")  # fuzz and exact
            if self.match_mode is None:
                self.match_mode = "fuzz"

            self.strict_mode = config.get("strict_mode")  # yes or no
            if self.strict_mode is None:
                self.strict_mode = False

            pass

        # configuring the logger
        self.logger = logging.getLogger("zerorigin.filter")
        hdlr = logging.FileHandler('./zerorigin.filter.log', encoding="UTF-8")
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.ERROR)

        pass

    def process_message(self, message: Message) -> Optional[Message]:

        config = yaml.full_load(open(utils.get_config_path(self.middleware_id), encoding="UTF-8"))

        if isinstance(message.author, SelfChatMember):
            return message

        if self.config_version != config.get('version'):
            self.logger.debug("config changed!")
            self.config_version = config.get('version')
            self.work_filters = config.get('work_filters')

        is_keep = list()
        for work_filter in WorkFilter:
            if work_filter.value in self.work_filters:
                is_keep.append(
                    config.get(work_filter.value)
                    and self.is_keep_message(work_filter, message, config.get(work_filter.value))
                )
                pass
            pass

        if self.strict_mode:
            if False not in is_keep:
                return message
        elif True in is_keep:
            return message

        pass

    # match blacklisted return False - no keep message
    def black_match(self, from_, from_alias, configs):
        if self.match_mode == "fuzz":
            for config in configs:
                if config in from_ or config in from_alias:
                    return False
                pass
        elif from_ in configs or from_alias in configs:
            return False

        return True

    # match whitelisted return True - keep message
    def white_match(self, from_, from_alias, configs):
        if self.match_mode == "fuzz":
            for config in configs:
                if config in from_ or config in from_alias:
                    return True
                pass
        elif from_ in configs or from_alias in configs:
            return True

        return False

    def is_keep_message(self, work_filter: WorkFilter, message: Message, configs: list) -> bool:

        # self.logger.debug("message is_mp type:%s", message.chat.vendor_specific['is_mp'])
        self.logger.debug("Received message from chat: %s--%s", message.chat.alias, message.chat.name)
        self.logger.debug("match_mode: %s", self.match_mode)
        from_ = message.author.name
        from_alias = message.author.alias

        if from_alias is None:
            from_alias = from_

        chat_name = message.chat.name
        chat_alias = message.chat.alias

        if chat_alias is None:
            chat_alias = chat_name

        self.logger.debug("Received message from : %s--%s", from_, from_alias)

        if isinstance(message.chat, GroupChat):
            self.logger.debug("Receive group chat")
            if work_filter is WorkFilter.black_group:
                return self.black_match(chat_name, chat_alias, configs)
            if work_filter is WorkFilter.white_group:
                return self.white_match(chat_name, chat_alias, configs)
        else:
            if work_filter is WorkFilter.black_person:
                self.logger.debug("Receive black person")
                return self.black_match(from_, from_alias, configs)
            if work_filter is WorkFilter.white_person:
                return self.white_match(from_, from_alias, configs)
