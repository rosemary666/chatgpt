#!/bin/bash

export PYTHONPATH=`pwd`/..

echo $PYTHONPATH

SERVICE_C0NF="conf/service.yaml" python main.py