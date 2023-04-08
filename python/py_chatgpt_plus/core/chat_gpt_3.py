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
import json
from typing import List, Generator

from py_chatgpt_plus.core.chat_base import ChatAbc
from py_chatgpt_plus.utils.http_call import HttpCall


class ChatGptV3(ChatAbc):
    def __init__(self,
                 api_key: str,
                 model: str = "gpt-3.5-turbo",
                 chatgpt_url: str = "https://api.openai.com/v1/chat/completions",
                 system_prompt: str = "You are ChatGPT, a large language model trained by OpenAI. Respond conversationally",
                 proxy_address: str = None,
                 temperature: float = 0.6,
                 top_p: float = 1.0,
                 max_tokens: int = 2048,
                 ):
        """
        Call Official chatGpt interface.
        Args:
            api_key(str): The chatGpt api key, please refer https://platform.openai.com/account/api-keys.
            model(str): The model of chatGpt v3, default to 'gpt-3.5-turbo'.
            proxy_address(str): The address of proxy.
            system_prompt(str): You are a
            temperature(float): What sampling temperature to use, between 0 and 2.\
                  Higher values like 0.8 will make the output more random, while lower values like 0.2 will \
                  make it more focused and deterministic.
            top_p(float): An alternative to sampling with temperature, called nucleus sampling, where the model
                 considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens \
                 comprising the top 10% probability mass are considered.
            max_tokens(int): The maximum number of tokens to generate in the completion.The token count of your \
                 prompt plus max_tokens cannot exceed the model's context length. Most models have a context length \
                 of 2048 tokens (except for the newest models, which support 4096).
        """
        self._api_key = api_key
        self._model = model
        self._proxy_address = proxy_address
        self._temperature = temperature
        self._top_p = top_p
        self._max_tokens = max_tokens
        self._http_call = HttpCall(proxy_addr=proxy_address)
        self._system_prompt = system_prompt
        self._conversations: List[dict] = [
            {
                "role": "system",
                "content": self._system_prompt,
            }
        ]
        self._chatgpt_url = chatgpt_url

    def _add_to_conversations(self, content: str, role: str = "user"):
        self._conversations.append(
            {
                "role": role,
                "content": content,
            }
        )

    def chat_once(self, prompt: str) -> str:
        all_rsp: str = ""
        for stream in self.chat_stream(prompt):
            all_rsp += stream
        return all_rsp

    def chat_stream(self, prompt: str) -> Generator:
        self._add_to_conversations(prompt, "user")
        streams = self._http_call.post_stream(
            url=self._chatgpt_url,
            header={
                "Authorization": f"Bearer {self._api_key}"
            },
            json={
                "model": self._model,
                "messages": self._conversations,
                "stream": True,
                "temperature": self._temperature,
                "top_p": self._top_p,
                "user": "user",
                "max_tokens": self._max_tokens,
            }
        )
        all_stream_content = ""
        rsp_role: str = None
        for stream in streams:
            stream = stream.decode("utf-8")[6:]
            if stream == "[DONE]":
                break
            rsp: dict = json.loads(stream)
            choices = rsp.get("choices")
            if not choices:
                continue
            delta = choices[0].get("delta")
            if not delta:
                continue
            if "role" in delta:
                rsp_role = delta["role"]
            if "content" in delta:
                content = delta["content"]
                all_stream_content += content
                yield content
        self._add_to_conversations(all_stream_content, rsp_role)

    def save_conversations(self, file_path: str):
        conversations_json = json.dumps(self._conversations, indent=4, ensure_ascii=False)
        with open(file_path, "w") as f:
            f.write(conversations_json)

    def load_conversations(self, file_path: str):
        with open(file_path, "r") as f:
            content = f.read()
        self._conversations = json.loads(content)