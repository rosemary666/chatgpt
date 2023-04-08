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
from loguru import logger
from pathlib import Path
import importlib
import re

from flask import Blueprint

from py_chatgpt_plus.routes.api import app, api_blue
from py_chatgpt_plus.utils.conf import conf_inst


def auto_register_blue_print(app):
    for path in Path(__file__).parent.glob("*_route.py"):
        page_name = re.sub("$%s" % "_route", "", path.stem)
        module_name = ".".join(
            path.parts[path.parts.index("py_chatgpt_plus"): -1] + (page_name,)
        )
        auto_blueprint = importlib.import_module(module_name)
        print(module_name)
        print(page_name)
        auto_blueprint.blue_route = Blueprint(page_name, module_name)
        app.register_blueprint(auto_blueprint.blue_route, url_prefix=f"/{page_name}")


auto_register_blue_print(app)
app.register_blueprint(api_blue)


def main():
    logger.add(conf_inst.log_file, level=conf_inst.log_level, enqueue=True, serialize=False, rotation="100 MB")
    logger.info(f"service will listen on:{conf_inst.local_ip}:{conf_inst.local_port}")
    app.run(host=conf_inst.local_ip, port=conf_inst.local_port)