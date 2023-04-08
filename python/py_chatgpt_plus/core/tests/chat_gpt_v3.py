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
from py_chatgpt_plus.core.chat_gpt_3 import ChatGptV3

api_key = "*******"


def test_stream():
    cg = ChatGptV3(
        api_key=api_key
    )
    streams = cg.chat_stream("请详细介绍一下你自己")
    for stream in streams:
        print(stream)


def test_once():
    cg = ChatGptV3(
        api_key=api_key,
        system_prompt="请帮我把以下的工作内容填充为工作周报，用markdown格式以分点叙述的方式输出:",
    )
    answer = cg.chat_once("主要开展了三件事情, 第一是完成功能1的开发，第二是完成了xx的需求评审，第三是接待了xx客户")
    print(answer)
    cg.save_conversations("./conversations.json")


if __name__ == "__main__":
    # test_stream()
    test_once()