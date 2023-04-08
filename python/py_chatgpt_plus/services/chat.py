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
from typing import Generator
from py_chatgpt_plus.core.chat_gpt_3 import ChatGptV3


class ChatService(object):
    def __init__(self, api_key: str):
        self._api_key = api_key

    def chat_once(self, prompt: str, system_prompt: str) -> str:
        cg = ChatGptV3(api_key=self._api_key,
                       system_prompt=system_prompt)
        return cg.chat_once(prompt=prompt)

    def chat_stream(self, prompt: str, system_prompt: str) -> Generator:
        cg = ChatGptV3(api_key=self._api_key)
        return cg.chat_stream(prompt=prompt,
                              system_prompt=system_prompt)