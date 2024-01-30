#  Copyright 2023 github.com/rosemary666. All Rights Reserved.
#  #
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  #
#      http://www.apache.org/licenses/LICENSE-2.0
#  #
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#  ==============================================================================
from typing import Any
import os

import yaml

from py_chatgpt_plus.utils.base_utils import Singleton

def read_yaml(path: str) -> Any:
    with open(path, "rb") as f:
        cf = f.read()
    cf = yaml.load(cf, Loader=yaml.SafeLoader)
    return cf

@Singleton
class ConfParse(object):
    def __init__(self):
        self._local_ip: str = "0.0.0.1"
        self._local_port: int = 32675
        self._chatgpt_api_key: str = None
        self._chatgpt_proxy: str = None
        self._log_file: str = None

    def __call__(self, path: str):
        cf = read_yaml(path)
        server_conf = cf.get("server")
        chatgpt_conf = cf.get("chatgpt")
        log_conf = cf.get("log")
        self._local_ip = server_conf.get("ip", "0.0.0.0")
        self._local_port = server_conf.get("port", 32675)
        self._chatgpt_api_key = chatgpt_conf.get("api_key", "")
        self._chatgpt_proxy = chatgpt_conf.get("proxy", "")
        self._log_file = log_conf.get("log_file", "service.log")
        self._log_level = log_conf.get("level", "DEBUG")

    @property
    def local_ip(self) -> str:
        return self._local_ip

    @property
    def local_port(self) -> int:
        return self._local_port

    @property
    def chatgpt_api_key(self) -> str:
        return self._chatgpt_api_key

    @property
    def chatgpt_proxy(self) -> str:
        return self._chatgpt_proxy

    @property
    def log_file(self) -> str:
        return self._log_file

    @property
    def log_level(self) -> str:
        return self._log_level


conf_inst = ConfParse()
conf_inst(
    path=os.getenv("SERVICE_C0NF", default="../conf/service.yaml")
)