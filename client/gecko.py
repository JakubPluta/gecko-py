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
        **kwargs,
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
        contract_addresses: [str, list],
        vs_currencies: [str, list],
        include_market_cap=False,
        include_24hr_vol=False,
        include_24hr_change=False,
        include_last_updated_at=False,
        **kwargs,
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
        del payload["id"]
        return self._request("GET", f"simple/token_price/{id}", payload=payload)

    def get_supported_vs_currencies(self):
        """/simple/supported_vs_currencies
        Get list of supported_vs_currencies.
        """
        return self._request("GET", "simple/supported_vs_currencies")

    def get_coins_list(self, include_platform=None):
        """/coins/list
        List all supported coins id, name and symbol (no pagination required)
        Use this to obtain all the coins’ id in order to make API calls

        * include_platform (boolean) [optional] flag to include platform contract addresses
        (eg. 0x… for Ethereum based tokens). valid values: true, false
        """
        params = {"include_platform": include_platform}
        return self._request("GET", "coins/list", payload=params)

    def get_coin_markets(
        self,
        vs_currency: str = "usd",
        ids=None,
        category=None,
        order=None,
        per_page=100,
        page=1,
        sparkline=False,
        price_change_percentage=None,
    ):
        """/coins/markets
        List all supported coins price, market cap, volume, and market related data
        Use this to obtain all the coins market data (price, market cap, volume)
        * vs_currency (string) [optional]  - The target currency of market data (usd, eur, jpy, etc.)
        * ids string (string) [optional] - id of coins,
                comma-separated if querying more than 1 coin *refers to coins/list
                When left empty, returns numbers the coins observing the params limit and start
        * category (string) [optional] - filter by coin category, only `decentralized_finance_defi` is supported
        * order (string) [optional] - valid values: [market_cap_desc, gecko_desc, gecko_asc, market_cap_asc,
                market_cap_desc, volume_asc, volume_desc, id_asc, id_desc]
                sort results by field. Default value : market_cap_desc
        * per_page (int) [optional] - valid values: 1…250, Total results per page, Default value : 100
        * page (int) [optional] -  Page through results Default value : 1
        * sparkline (boolean) [optional]  - Include sparkline 7 days data (eg. true, false), Default value : false
        * price_change_percentage (string) [optional] - Include price change percentage in 1h, 24h, 7d, 14d, 30d,
                200d, 1y (eg. '1h,24h,7d' comma-separated, invalid values will be discarded)

        """

        payload = self._build_payload(locals())
        return self._request("GET", "coins/markets", payload=payload)



gecko = GeckoClient()
# gecko.get_price("bitcoin,0x", "eth,dot")
# gecko.get_token_price('ethereum','0xA8b919680258d369114910511cc87595aec0be6D', 'bitcoin,eth,dot')
gecko.get_coin_markets()

