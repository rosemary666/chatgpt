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
class ChatGptError(Exception):
    def __init__(self, ret_code: int = 0, ret_msg: str = "success"):
        """Define base error.

        Args:
            ret_code (int): The code of ret, default to 0.
            ret_msg: The description of ret, default to success.
        """
        self._ret_code = ret_code
        self._ret_msg = ret_msg

    def ret_code(self) -> int:
        return self._ret_code

    def ret_msg(self) -> str:
        return self._ret_msg

    def set_ret_msg(self, msg: str):
        self._ret_msg = msg
        return self