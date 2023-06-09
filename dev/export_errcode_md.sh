#!/bin/bash

#
#  Copyright 2022 iFLYTEK. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#  ==============================================================================
#
set -e
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"/../
export PYTHONPATH=$PYTHONPATH:${PWD}/python

# export errcode as md file to docs dir
export server_errcode_md_file=${PWD}/doc/docs/api/errcode/chatgpt_service_errcode.md
python python/py_chatgpt_plus/errors/export.py --dst_file ${server_errcode_md_file}

