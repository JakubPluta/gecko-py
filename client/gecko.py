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
        return self._request("GET", "ping")

    def get_price(
        self,
        ids: [str, list],
        vs_currencies: [str, list],
        include_market_cap=False,
        include_24hr_vol=False,
        include_24hr_change=False,
        include_last_updated_at=False,
        **kwargs
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
        payload = self._build_payload(locals(), **kwargs)
        return self._request("GET", "simple/price", payload=payload)

    def get_token_price(
        self,
        id: str,
        contract_addresses: [str,list],
        vs_currencies: [str, list],
        include_market_cap=False,
        include_24hr_vol=False,
        include_24hr_change=False,
        include_last_updated_at=False,
        **kwargs
    ):
        """/simple/token_price/{id}
        Get current price of tokens (using contract addresses) for a given platform in any other currency that you need.

        Params:
            * id string (string) [required] - the id of the platform issuing tokens (Only ethereum is supported for now)
            * contract_addresses (string) [required] contract address of tokens, comma separated

            * vs_currencies (string) [required]  - vs_currency of coins,
                comma-separated if querying more than 1 vs_currency*refers to simple/supported_vs_currencies

            * include_market_cap (string) [optional] - true/false to include market_cap, default: false
            * include_24hr_vol (string) [optional] - true/false to include 24hr_vol, default: false
            * include_24hr_change (string) [optional] - true/false to include 24hr_change, default: false
            * include_last_updated_at (string) [optional] - true/false to include last_updated_at of price, default: false

        example:
            simple/token_price/ethereum?contract_addresses=0xA8b919680258d369114910511cc87595aec0be6D&vs_currencies=eth%2Cbitcoin%2Cdot

        """
        payload = self._build_payload(locals(), **kwargs)
        del payload['id']
        return self._request("GET", f"simple/token_price/{id}", payload=payload)

    def get_supported_vs_currencies(self):
        """/simple/supported_vs_currencies
        Get list of supported_vs_currencies.
        """
        return self._request("GET", "simple/supported_vs_currencies")

    def get_all_coins_list(self, include_platform=False):
        """/coins/list
        List all supported coins id, name and symbol (no pagination required)
        Use this to obtain all the coins’ id in order to make API calls
        """
        payload = self._build_payload(include_platform)
        return self._request("GET", "coins/list", payload=payload)

