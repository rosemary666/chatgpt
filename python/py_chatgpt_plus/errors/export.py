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
import argparse
import importlib
import inspect
import sys
from typing import Dict, List, Union

from py_chatgpt_plus.errors import ChatGptError
from pytablewriter import MarkdownTableWriter

module_paths = ["py_chatgpt_plus.errors.error"]


def dynamic_import(module):
    return importlib.import_module(module)


def get_module_attributes(module_path: str):
    errcode_dict: Dict[str, List[Dict[str, Union[str, int]]]] = {}
    module = dynamic_import(module_path)
    for class_name, class_ in inspect.getmembers(
        sys.modules[module.__name__], inspect.isclass
    ):
        attributes = inspect.getmembers(class_, lambda a: not (inspect.isroutine(a)))
        attr_list = [
            a for a in attributes if not (a[0].startswith("__") and a[0].endswith("__"))
        ]
        for attr in attr_list:
            if isinstance(attr[1], ChatGptError):
                module_name = attr[0]
                ret_code = attr[1].__dict__["_ret_code"]
                ret_msg = attr[1].__dict__["_ret_msg"]
                if class_name not in errcode_dict:
                    errcode_dict[class_name] = [
                        {
                            "ret_code": ret_code,
                            "ret_msg": ret_msg,
                            "ret_module": module_name,
                        }
                    ]
                else:
                    errcode_dict[class_name].append(
                        {
                            "ret_code": ret_code,
                            "ret_msg": ret_msg,
                            "ret_module": module_name,
                        }
                    )
    return errcode_dict


def export(dst_file: str):
    errcode_api_md_content = "# Server Errcode API    \n"
    for module_path in module_paths:
        errcode_dict = get_module_attributes(module_path)
        for className, code_info_lists in errcode_dict.items():
            writer = MarkdownTableWriter(
                table_name=className,
                headers=["ret_module", "ret_code", "ret_msg"],
                value_matrix=[],
                margin=1,  # add a whitespace for both sides of each cell
            )
            value_matrix = []
            for code_info_dict in code_info_lists:
                value_matrix.append(
                    [
                        code_info_dict["ret_module"],
                        code_info_dict["ret_code"],
                        code_info_dict["ret_msg"],
                    ]
                )
            writer.value_matrix = value_matrix
            content = writer.dumps()
            errcode_api_md_content += str(content) + "    \n"
    with open(dst_file, "w") as md_file:
        md_file.write(errcode_api_md_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export errcode")
    parser.add_argument("-f", "--dst_file", type=str, required=True, help="output file")
    args = parser.parse_args()

    export(dst_file=args.dst_file)
