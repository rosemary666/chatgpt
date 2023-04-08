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
from abc import ABC, abstractmethod
from typing import Generator


class ChatAbc(ABC):
    """
    The chat abstract class encapsulated by calling the chatGpt interface.
    """
    @abstractmethod
    def chat_once(self, prompt: str) -> str:
        """
        Return results all at once, non-streaming return.
        Args:
            prompt(str): Typed prompt.

        Returns:
            str: The reply.
        """
        pass

    @abstractmethod
    def chat_stream(self, prompt: str) -> Generator:
        """
        Return result by stream.
        Args:
            prompt(str): Typed prompt.

        Returns:
            The reply stream.
        """
        pass

    @abstractmethod
    def save_conversations(self, file_path: str):
        """
        Save the conversations to a specified file.
        Args:
            file_path(str): The path of file.

        Returns:
        """
        pass

    @abstractmethod
    def load_conversations(self, file_path: str):
        """
        Load the conversations from a specified file.
        Returns:

        """
        pass
