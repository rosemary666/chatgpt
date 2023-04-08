#!/bin/bash
set -e

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"/../
export PYTHONPATH=$PYTHONPATH:${PWD}/python
export SERVICE_C0NF=python/py_chatgpt/conf/service.yaml

# export swagger schema json file to docs
export server_swagger_file=${PWD}/doc/docs/api/swagger/chatgpt_service_swagger.json
python python/py_chatgpt/routes/export.py --type 0 --dst_file ${server_swagger_file}
