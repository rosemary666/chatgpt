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
import uuid
from typing import Any

from flask import Flask, Blueprint
from flask_restx import Api, fields

from py_chatgpt_plus.errors.error import ChatGptError, Success

app = Flask(__name__)

app.config.SWAGGER_UI_OPERATION_ID = True  # type: ignore
app.config.SWAGGER_UI_REQUEST_DURATION = True  # type: ignore
app.url_map.strict_slashes = False
app.config["JSON_AS_ASCII"] = False
app.config["ERROR_INCLUDE_MESSAGE"] = False  # 必须设置为False
app.config["SECRET_KEY"] = "@&^&N908jksd#"

api_blue = Blueprint("api", __name__, url_prefix="/api/v1")

api = Api(
    api_blue,
    version="1.0",
    title="ChatGpt service!",
    description="ChatGpt service!",
    doc="/doc",
)


@api.errorhandler(ChatGptError)
def chat_gpt_error_response(e):
    return get_json_result(e), 200


@api.errorhandler(Exception)
def server_internal_err_response(e):
    return "internal server error", 500


def get_json_result(
    custom_err: ChatGptError = Success.SuccessResponse, data=None
):
    """Get API json result.

    Args:
        custom_err (ChatGptError): The Error class include ret_msg and ret_code.
        data (Any): The custom result data.

    Returns:
    """
    result_dict = {"ret_code": custom_err.ret_code(), "ret_msg": custom_err.ret_msg()}
    if data is not None:
        result_dict["data"] = data
    return result_dict


def custom_response(data: Any = None) -> Any:
    if data is not None:
        custom_model = api.model(
            "CustomResponse" + str(uuid.uuid4()),
            {
                "ret_code": fields.Integer(description="The code of result", default=0),
                "ret_msg": fields.String(
                    description="The message of result", default="success"
                ),
                "data": fields.Nested(data),
            },
        )
    else:
        custom_model = api.model(
            "CustomResponse",
            {
                "ret_code": fields.Integer(description="The code of result", default=0),
                "ret_msg": fields.String(
                    description="The message of result", default="success"
                ),
            },
        )
    return custom_model
