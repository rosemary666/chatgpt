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
import requests
from typing import Any, Optional, Generator


class HttpCall(object):
    def __init__(self, proxy_addr: str):
        self._session = requests.Session()
        if proxy_addr is not None or not proxy_addr:
            self._session.proxies.update({
                "http": proxy_addr,
                "https": proxy_addr,
            })

    def post_once(self, url: str,
                  header: dict = {"Content-Type": "application/json"},
                  json: Optional[Any] = None,
                  data=None,
                  files=None):
        """
        Non-streaming post interface.
        """
        if json is not None:
            header["Content-Type"] = "application/json"
        rsp = self._session.post(
            url=url,
            headers=header,
            data=data,
            json=json,
            files=files,
            stream=False,
        )
        rsp.raise_for_status()
        return rsp.json()

    def post_stream(self, url: str,
                    header: dict = {"Content-Type": "application/json"},
                    json: Optional[Any] = None,
                    data=None,
                    files=None) -> Generator:
        """
        Streaming post interface
        """
        if json is not None:
            header["Content-Type"] = "application/json"
        rsp = self._session.post(
            url=url,
            headers=header,
            data=data,
            files=files,
            json=json,
            stream=True,
        )
        rsp.raise_for_status()
        for line in rsp.iter_lines():
            if not line:
                continue
            yield line
