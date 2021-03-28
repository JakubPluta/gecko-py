# https://www.coingecko.com/en/api
import json
import requests
from config import GeckoConfig
from typing import List, Tuple, Optional, Dict, Callable, Iterable, Union, Any
from client.restclient import RestClient


class GeckoClient(RestClient):

    def __init__(self, config=GeckoConfig):
        super(GeckoClient, self).__init__(config)

    def ping(self):
        return self._request('GET', 'ping')

    def get_price(self,
                  ids: [str, list], vs_currencies: [str, list],
                  include_market_cap=False, include_24hr_vol=False,
                  include_24hr_change=False, include_last_updated_at=False, **kwargs
                  ):
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
        payload = self._build_payload(locals(),**kwargs)
        return self._request('GET', 'simple/price', payload=payload)




gecko = GeckoClient()
gecko.get_price('bitcoin','eth')

