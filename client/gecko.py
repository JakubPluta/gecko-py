# https://www.coingecko.com/en/api
import json
import requests
from config import GeckoConfig
from typing import List, Tuple, Optional, Dict, Callable, Iterable, Union, Any


class GeckoClient:

    def __init__(self, config=GeckoConfig):

        self.url = config.BASE_URL
        self._adapter = config.ADAPTER
        self._retry_strategy = config.RETRY_STRATEGY

        self.session = requests.Session()
        self.session.mount('http://', self._adapter)

    def _build_url(self, endpoint):
        pass

    def _make_request(self, url):
        response = self.session.get(url)
        if response.ok:
            print(response.json())
            return response.json()
        else:
            return None

    def ping(self):
        return self._make_request(self.url + 'ping')

    def get_price(self, ids: [str, list], vs_currencies: [str, list], **kwargs):
        """/simple/price
        Get the current price of any cryptocurrencies in any other supported currencies that you need.

        Params:
            * ids string (string) [required] - id of coins,
                comma-separated if querying more than 1 coin *refers to coins/list

            * vs_currencies (string) [required]  - vs_currency of coins,
                comma-separated if querying more than 1 vs_currency*refers to simple/supported_vs_currencies

            * include_market_cap (string) [optional] - true/false to include market_cap, default: false
            * include_24hr_vol (string) [optional] - true/false to include 24hr_vol, default: false
            * include_24hr_change (string) [optional] - true/false to include 24hr_change, default: false
            * include_last_updated_at (string) [optional] - true/false to include last_updated_at of price, default: false

        """

        return self._make_request(self.url + f'simple/price?ids={ids}&vs_currencies={vs_currencies}')



gecko = GeckoClient()
gecko.get_price('0x','eth')

