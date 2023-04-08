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
"""Export swagger schema."""
import argparse
import json

from py_chatgpt_plus.routes.api import api, app

def export_schema_to_swagger(dst_file: str):
    """Export schema to swagger json file.

    Args:
        dst_file: The output file.

    Returns:
    """
    app.config["SERVER_NAME"] = "localhost"
    app.app_context().__enter__()
    with open(dst_file, "w") as json_file:
        json.dump(api.__schema__, json_file, indent=4)


def export_schema_to_postman_collection(dst_file: str):
    """Export API schema as a Postman collection.

    Args:
        dst_file: The output file.

    Returns:
    """
    app.config["SERVER_NAME"] = "localhost"
    app.app_context().__enter__()
    urlvars = False  # Build query strings in URLs
    swagger = True  # Export Swagger specifications
    data = api.as_postman(urlvars=urlvars, swagger=swagger)
    with open(dst_file, "w") as json_file:
        json.dump(data, json_file, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export swagger schema")
    parser.add_argument(
        "-t",
        "--type",
        type=int,
        default=0,
        choices=[0, 1],
        help="export as swagger or postman collection, 0 for swagger, 1 for postman collection",
    )
    parser.add_argument("-f", "--dst_file", type=str, required=True, help="output file")
    args = parser.parse_args()

    if args.type == 0:
        export_schema_to_swagger(args.dst_file)
    elif args.type == 1:
        export_schema_to_postman_collection(args.dst_file)
    else:
        raise Exception("unsupported export type.")
