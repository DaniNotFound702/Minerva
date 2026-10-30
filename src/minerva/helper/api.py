import logging
import os
from typing import Any, Dict, Optional
import requests
from helper.log_api_message import log_api_message


logger = logging.getLogger(__name__)


class ZermeloAPIError(Exception):
    """Custom exception raised when the Zermelo API returns an error response."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Zermelo API Error {status_code}: {message}")


class ZermeloAPIClient:
    def __init__(
        self,
        school: Optional[str] = None,
        authorization: Optional[str] = None,
        api_version: str = "v3",
    ):
        self.school = school or os.getenv("SCHOOL")
        self.authorization = authorization or os.getenv("AUTHORIZATION")
        self.api_version = api_version

        if not self.school:
            raise ValueError(
                "Missing school domain. Provide 'school' or set the 'SCHOOL' environment variable."
            )
        if not self.authorization:
            raise ValueError(
                "Missing authorization token. Provide 'authorization' or set the 'AUTHORIZATION' environment variable."
            )

        self.base_url = f"https://{self.school}.zportal.nl/api/{self.api_version}/"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": self.authorization})

    def get_endpoint(self, endpoint: str, parameters: str) -> Optional[Any]:
        url = f"{self.base_url}{endpoint}?{parameters}"
        headers = dict(self.session.headers)

        try:
            response = self.session.get(url)
            json_data = response.json()
            log_api_message(url, headers, json_data)

            api_response = json_data.get("response", {})
            status = api_response.get("status")

            if status != 200:
                message = api_response.get("message", "Unknown error")
                logger.error("API error in get_endpoint: %s %s", status, message)

                if status == 401:
                    # In a library, raise an exception instead of calling quit()
                    raise ZermeloAPIError(
                        status,
                        "Token expired or unauthorized. Please refresh credentials."
                    )
                if status == 403:
                    logger.error("Access forbidden. Verify API token permissions.")
                    return None

                raise ZermeloAPIError(status, message)

            return api_response.get("data")

        except requests.exceptions.RequestException as error:
            logger.error("Network or HTTP error in get_endpoint: %s", error)
            raise
        except Exception as error:
            logger.error("Unexpected error in get_endpoint: %s", error)
            raise 