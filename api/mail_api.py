import requests
import os
import logging
import json
from dotenv import load_dotenv
from .custom_http_connection import CustomHTTPConnection  #used

load_dotenv()


class MailAPI:
    def __init__(self):
        self.base_url = os.getenv("MAIL_URL")
        self.logger = logging.getLogger("http.client")

    def make_request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint}"
        self.logger.info(f"Making {method} request to URL: {url}")
        if kwargs.get("headers"):
            self.logger.info(
                "Request Headers:\n" + json.dumps(kwargs["headers"], indent=4)
            )
        if kwargs.get("json"):
            self.logger.info(
                "Request JSON Body:\n" + json.dumps(kwargs["json"], indent=4)
            )
        if kwargs.get("data"):
            self.logger.info(
                "Request Form Data:\n" + json.dumps(kwargs["data"], indent=4)
            )

        response = requests.request(method, url, **kwargs)
        response.raise_for_status()

        self.logger.info(
            "Response Headers:\n" + json.dumps(dict(response.headers), indent=4)
        )
        if "application/json" in response.headers.get("Content-Type", ""):
            self.logger.info("Response Body:\n" + json.dumps(response.json(), indent=4))
        return response
