"""APIs for study files"""
import datetime
import importlib
import os

from urllib.parse import quote

import requests
from dateutil import tz
from flask_restx import Namespace, Resource, reqparse

api = Namespace("File", description="File operations", path="/")


@api.route("/study/<study_id>/files")
class Files(Resource):
    """Files for a study"""

    parser = reqparse.RequestParser()
    parser.add_argument("path", type=str, required=False, location="args")

    @api.doc(description="Return a list of all files for a study")
    @api.param("path", "The folder path on the file system")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def get(self, study_id):
        """Return a list of all files for a study"""

        # todo: anticipating that each study will have a folder in the storage account
        # with the same name as the study id.

        # Determine the appropriate configuration module
        # based on the testing context
        if os.environ.get("FLASK_ENV") == "testing":
            config_module_name = "pytest_config"
        else:
            config_module_name = "config"

        config_module = importlib.import_module(config_module_name)

        if os.environ.get("FLASK_ENV") == "testing":
            # If testing, use the 'TestConfig' class for accessing 'secret'
            config = config_module.TestConfig
        else:
            # If not testing, directly use the 'config' module
            config = config_module

        storage_account_name = config.FAIRHUB_AZURE_STORAGE_ACCOUNT_NAME
        storage_account_sas_token = config.FAIRHUB_AZURE_READ_SAS_TOKEN
        request_time = datetime.datetime.now(datetime.timezone.utc).strftime(
            "%a, %d %b %Y %H:%M:%S GMT"
        )

        container = "pooled-data-pilot"  # todo: this should be the study id

        query_params = (
            f"recursive=false&resource=filesystem&{storage_account_sas_token}"
        )

        request_args = self.parser.parse_args()

        # subdirectory traversal
        if prefix_path := request_args["path"]:
            print(prefix_path)
            query_path = quote(prefix_path.encode("utf-8"))
            query_params = f"directory={query_path}&{query_params}"

        url = f"https://{storage_account_name}.dfs.core.windows.net/{container}?{query_params}"  # noqa: E501 # pylint: disable=line-too-long

        print(url)

        api_version = "2023-08-03"
        headers = {
            "x-ms-date": request_time,
            "x-ms-version": api_version,
        }

        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=30,
            )

            response_json = response.json()

            paths = []

            for file in response_json["paths"]:
                data = {
                    "contentLength": file["contentLength"],
                    "creationTime": file["creationTime"],
                    "name": file["name"],
                    "isDirectory": bool("isDirectory" in file and file["isDirectory"]),
                }

                # convert lastModified to unix timestamp
                if "lastModified" in file:
                    date_string = file["lastModified"]
                    date_object = datetime.datetime.strptime(
                        date_string, "%a, %d %b %Y %H:%M:%S %Z"
                    )
                    utc_timestamp = date_object.replace(tzinfo=tz.tzutc()).timestamp()
                    data["lastModified"] = utc_timestamp

                paths.append(data)

            return paths
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return "Something went wrong with the request", 500
