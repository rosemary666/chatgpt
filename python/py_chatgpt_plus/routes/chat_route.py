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
from flask import Response, request
from flask_restx import Resource, fields

from loguru import logger

from py_chatgpt_plus.services.chat import ChatService
from py_chatgpt_plus.routes.api import api, custom_response, get_json_result
from py_chatgpt_plus.utils.conf import conf_inst

ns = api.namespace("chat", description="Chat  API")

chat_service = ChatService(api_key=conf_inst.chatgpt_api_key)

chat_base_request_fields = api.clone(
    "ChatBaseRequest",
    {
        "prompt": fields.String(required=True, description="Type prompt."),
        "system_prompt": fields.String(required=True,
                                       description="System prompt",
                                       default="You are ChatGPT, a large language model trained by OpenAI. Respond conversationally"),
    }
)

chat_base_once_response_fields = api.model(
     "ChatBaseOnceResponseFields",
     {
        "answer": fields.String(required=True, description="The id of mpc job."),
     }
)


@ns.route("/once")
class ChatOnce(Resource):
    @ns.expect(chat_base_request_fields)
    @ns.marshal_with(custom_response(chat_base_once_response_fields))
    def post(self):
        """chat once, no stream!"""
        req_json = request.json
        logger.debug(f"receive chat once post request:{req_json}")
        answer = chat_service.chat_once(prompt=req_json.get("prompt", ""),
                                        system_prompt=req_json.get("system_prompt"))
        return get_json_result(data={"answer": answer})


@ns.route("/stream")
class ChatStream(Resource):
    @api.doc(responses={200: "Stream SSE data in text/event-stream format"})
    @api.representation("text/event-stream")
    @ns.expect(chat_base_request_fields)
    def post(self):
        """chat stream."""
        req_json = request.json
        logger.debug(f"receive chat stream post request:{req_json}")
        return Response(chat_service.chat_stream(prompt=req_json.get("prompt", ""),
                                                 system_prompt=req_json.get("system_prompt")),
                                                 mimetype="text/event-stream")