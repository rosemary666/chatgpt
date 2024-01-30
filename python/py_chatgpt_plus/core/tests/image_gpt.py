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
from py_chatgpt_plus.core.image_gpt import ImageGpt

api_key = "****"


def test_image_generate_url():
    ig = ImageGpt(
        api_key=api_key
    )
    urls = ig.generate_url('Draw a white cat. it is a real cat, not a cartoon cat')
    print(urls)


def test_image_generate_content():
    ig = ImageGpt(
        api_key=api_key
    )
    contents = ig.generate_content('Draw a white cat. it is a real cat, not a cartoon cat')
    for i, content in enumerate(contents):
        with open(f"image_{i}.png", "wb") as f:
            f.write(content)


def test_image_generate_variations_url(image_path: str):
    ig = ImageGpt(
        api_key=api_key
    )
    urls = ig.generate_variations_url(image_path)
    print(urls)


if __name__ == "__main__":
    # test_image_generate_url()
    # test_image_generate_content()
    test_image_generate_variations_url("image_0.png")
