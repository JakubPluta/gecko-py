from config import Config, GeckoConfig
import requests
from requests.exceptions import HTTPError
from client import logger
from client.exceptions import RestClientError

ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE"]
HEADERS = {}


class RestClient:
    def __init__(self, config: Config):

        self._url = config.BASE_URL
        self._adapter = config.ADAPTER
        self._retry_strategy = config.RETRY_STRATEGY

        if config.SESSION:
            self.session = requests.Session()
        else:
            self.session = requests

        self.session.mount("http://", self._adapter)

    def __repr__(self):
        return f'<RestClient(url="{self._url}")>'

    def _build_endpoint_url(self, url):
        return f"{self._url}{url}"

    def _build_payload(self, params):
        try:
            del params["self"]
        except Exception as e:
            logger.info(e)
        return params

    def _request(self, method: str, url: str, params: dict = None):
        endpoint_url = self._build_endpoint_url(url)
        response = self.session.request(method, endpoint_url, params=params)

        try:
            response.raise_for_status()
        except HTTPError as e:
            logger.error(response.json())
            raise RestClientError(e)
        print(response.json())
        return response.json()
