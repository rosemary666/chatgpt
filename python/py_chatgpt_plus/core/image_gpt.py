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
from typing import List
import base64

from py_chatgpt_plus.utils.http_call import HttpCall


class ImageGpt(object):
    _image_gpt_url = "https://api.openai.com/v1/images/generations"
    _image_variations_url = "https://api.openai.com/v1/images/variations"

    def __init__(self,
                 api_key: str,
                 proxy_address: str = None,
                 ):
        """
        Creates an image given a prompt
        Args:
            api_key(str): The chatGpt api key, please refer https://platform.openai.com/account/api-keys.
            proxy_address(str): The address of proxy.
        """
        self._api_key = api_key
        self._proxy_address = proxy_address
        self._http_call = HttpCall(proxy_addr=proxy_address)

    def generate_url(self, prompt: str,
                     n: int = 1,
                     size: str = "1024x1024") -> List[str]:
        """
        Generate Image url.
        Args:
            prompt(str): Type prompt.
            n(int): The number of images to generate. Must be between 1 and 10.
            size(str): The size of the generated images. Must be one of 256x256, 512x512, or 1024x1024.
        Returns:
            List[str]: The list of generate image url.
        """
        content = self._http_call.post_once(
            url=self._image_gpt_url,
            header={
                "Authorization": f"Bearer {self._api_key}"
            },
            json={
                "prompt": prompt,
                "n": n,
                "size": size,
                "response_format": "url",
            }
        )
        urls = []
        for d in content["data"]:
            urls.append(d["url"])
        return urls

    def generate_content(self, prompt: str,
                         n: int = 1,
                         size: str = "1024x1024") -> List[bytes]:
        """
        Generate Image content, can be save to a file.
        Args:
            prompt(str): Type prompt.
            n(int): The number of images to generate. Must be between 1 and 10.
            size(str): The size of the generated images. Must be one of 256x256, 512x512, or 1024x1024.
        Returns:
            List[str]: The list of generate image content.
        """
        content = self._http_call.post_once(
            url=self._image_gpt_url,
            header={
                "Authorization": f"Bearer {self._api_key}"
            },
            json={
                "prompt": prompt,
                "n": n,
                "size": size,
                "response_format": "b64_json",
            }
        )
        b64_list = []
        for d in content["data"]:
            b64_list.append(base64.b64decode(d["b64_json"]))
        return b64_list

    def generate_variations_url(self,
                                image_path: str,
                                ) -> List[bytes]:
        """
        Generate a variation image url of a given image.
        Args:
            image_path(str): The image to use as the basis for the variation(s).
             Must be a valid PNG file, less than 4MB, and square.
        Returns:
            List[str]: The list of generate image content.
        """
        content = self._http_call.post_once(
            url=self._image_variations_url,
            header={
                "Authorization": f"Bearer {self._api_key}"
            },
            files={
                    "image": ("gpt_image.png", open(image_path, 'rb'), "image/png"),
                  }
        )
        urls = []
        for d in content["data"]:
            urls.append(base64.b64decode(d["url"]))
        return urls