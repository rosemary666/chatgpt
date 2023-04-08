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
import asyncio
import websockets

from loguru import logger

from py_chatgpt_plus.utils.conf import conf_inst
from py_chatgpt_plus.core.chat_gpt_3 import ChatGptV3

cg = ChatGptV3(
    api_key=conf_inst.chatgpt_api_key,
    proxy_address=conf_inst.chatgpt_proxy)


async def chat_stream(websocket):
    async for message in websocket:
        logger.debug(f"chat_stream | receive prompt:{message}")
        streams = cg.chat_stream(prompt=message)
        all_stream_content = ""
        for stream in streams:
            all_stream_content += stream
            await websocket.send(stream)
        logger.debug(f"chat_stream | send rsp:{all_stream_content}")


async def chat_once(websocket):
    async for message in websocket:
        logger.debug(f"chat_once | receive prompt:{message}")
        rsp = cg.chat_once(prompt=message)
        logger.debug(f"chat_once | send rsp:{rsp}")
        await websocket.send(rsp)


async def handle(websocket, path):
    if path == "/chat_once":
        await chat_once(websocket)
    elif path == "/chat_stream":
        await chat_stream(websocket)
    else:
        raise ValueError(f"not support path:{path}")


async def main():
    logger.debug(f"service will listen on:{conf_inst.local_ip}:{conf_inst.local_port}")
    async with websockets.serve(handle, conf_inst.local_ip, conf_inst.local_port):
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())
