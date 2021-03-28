# https://www.coingecko.com/en/api
import json
import requests
from config import GeckoConfig
from typing import List, Tuple, Optional, Dict, Callable, Iterable, Union, Any
from client.restclient import RestClient
import inspect
from client.utils import convert_list_to_coma_sep


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
        ids = convert_list_to_coma_sep(ids)
        vs_currencies = convert_list_to_coma_sep(vs_currencies)
        params = self._build_payload(locals())
        return self._request("GET", "simple/price", params=params)

    def get_token_price(
        self,
        id: str,
        contract_addresses: [str, list],
        vs_currencies: [str, list],
        include_market_cap=False,
        include_24hr_vol=False,
        include_24hr_change=False,
        include_last_updated_at=False,
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
        contract_addresses = convert_list_to_coma_sep(contract_addresses)
        vs_currencies = convert_list_to_coma_sep(vs_currencies)
        params = self._build_payload(locals())
        del params["id"]
        return self._request("GET", f"simple/token_price/{id}", params=params)

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
        return self._request("GET", "coins/list", params=params)

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
        params = self._build_payload(locals())
        return self._request("GET", "coins/markets", params)

    def get_coin(
        self,
        id: str,
        localization=True,
        tickers=True,
        market_data=True,
        community_data=True,
        developer_data=True,
        sparkline=False,
    ):
        """/coins/{id}
        Get current data (name, price, market, … including exchange tickers) for a coin.

        IMPORTANT:
        Ticker object is limited to 100 items, to get more tickers, use /coins/{id}/tickers
        Ticker is_stale is true when ticker that has not been updated/unchanged from the exchange for a while.
        Ticker is_anomaly is true if ticker’s price is outliered by our system.
        You are responsible for managing how you want to display these information
        (e.g. footnote, different background, change opacity, hide)

        * id (string) [required] - pass the coin id (can be obtained from /coins) eg. bitcoin
        * localization (string) [optional] -  Include all localized languages in response (true/false) [default: true]
        * tickers (boolean) [optional] - Include tickers data (true/false) [default: true]
        * market_data (boolean) [optional] - Include market_data (true/false) [default: true]
        * community_data - (boolean) [optional] - Include community_data data (true/false) [default: true]
        * developer_data - (boolean) [optional] - Include developer_data data (true/false) [default: true]
        * sparkline (boolean) [optional] - Include sparkline 7 days data (eg. true, false) [default: false]

        example:
        coins/eth?localization=true&tickers=true&market_data=true&community_data=true&developer_data=true&sparkline=false
        """
        params = self._build_payload(locals())
        del params["id"]
        return self._request("GET", f"coins/{id}", params=params)

    def get_coin_tickers(
        self,
        id: str,
        exchange_ids=None,
        include_exchange_logo=False,
        page=1,
        order="trust_score_desc",
        depth=True,
    ):
        """/coins/{id}/tickers
        Get coin tickers (paginated to 100 items)

        IMPORTANT:
        Ticker is_stale is true when ticker that has not been updated/unchanged from the exchange for a while.
        Ticker is_anomaly is true if ticker’s price is outliered by our system.
        You are responsible for managing how you want to display these information
        (e.g. footnote, different background, change opacity, hide)

        * id (string) [required] - pass the coin id (can be obtained from /coins) eg. bitcoin
        * exchange_ids (string) [optional] - filter results by exchange_ids (ref: v3/exchanges/list)
        * include_exchange_logo(boolean) [optional] - flag to show exchange_logo
        * page (int) [optional] -  Page through results Default value : 1
        * order (string) [optional] - valid values: trust_score_desc (default), trust_score_asc and volume_desc
        * depth (string) [optional] - flag to show 2% orderbook depth. valid values: true, false

        """
        params = self._build_payload(locals())
        del params["id"]
        return self._request("GET", f"coins/{id}/tickers", params=params)

    def get_coin_history(self, id: str, date: str, localization=True):
        """/coins/{id}/history
        Get coin tickers (paginated to 100 items)

        * id (string) [required] - pass the coin id (can be obtained from /coins) eg. bitcoin
        * date (string) [required] - The date of data snapshot in dd-mm-yyyy eg. 30-12-2017
        * localization (string) [optional] - Set to false to exclude localized languages in response

        """
        # TODO: ADD A HANDLER FOR DIFFERENT KIND OF DATE
        params = self._build_payload(locals())
        del params["id"]
        return self._request("GET", f"coins/{id}/history", params=params)

    def get_coin_market_chart(
        self,
        id: str,
        vs_currency: str = "usd",
        days: [str, int] = "max",
        interval="daily",
    ):
        """/coins/{id}/market_chart
        Get historical market data include price, market cap, and 24h volume (granularity auto)
        Minutely data will be used for duration within 1 day,
        Hourly data will be used for duration between 1 day and 90 days, Daily data will be used for duration above 90 days.

        * id (string) [required] - pass the coin id (can be obtained from /coins) eg. bitcoin
        * vs_currency (string) [required]  - The target currency of market data (usd, eur, jpy, etc.)
        * days (int) [required] - Data up to number of days ago (eg. 1,14,30,max)
        * interval (string) [optional] - Data interval. Possible value: daily

        """
        params = self._build_payload(locals())
        del params["id"]
        return self._request("GET", f"coins/{id}/market_chart", params=params)

    def get_coin_market_chart_range(
        self, id: str, from_: [str, int], to: str, vs_currency: str = "usd",
    ):
        """/coins/{id}/market_chart/range
        Get historical market data include price, market cap, and 24h volume (granularity auto)
        Minutely data will be used for duration within 1 day,
        Hourly data will be used for duration between 1 day and 90 days, Daily data will be used for duration above 90 days.

        * id (string) [required] - pass the coin id (can be obtained from /coins) eg. bitcoin
        * vs_currency (string) [required]  - The target currency of market data (usd, eur, jpy, etc.)
        * from int - From date in UNIX Timestamp (eg. 1392577232)
        * to int - To date in UNIX Timestamp (eg. 1392577232)

        """
        params = self._build_payload(locals())
        del params["id"]
        params["from"] = params.pop("from_")

        return self._request("GET", f"coins/{id}/market_chart/range", params=params)

    def get_coin_status_updates(self, id: str, per_page=100, page=1):
        """/coins/{id}/status_updates
        Get status updates for a given coin (beta)


        * id (string) [required] - pass the coin id (can be obtained from /coins) eg. bitcoin
        * per_page (int) [optional] - valid values: 1…250, Total results per page, Default value : 100
        * page (int) [optional] -  Page through results Default value : 1

        """
        params = self._build_payload(locals())
        del params["id"]
        return self._request("GET", f"coins/{id}/status_updates", params=params)

    def get_coin_ohlc(self, id:str, vs_currency='usd', days=90):
        """/coins/{id}/ohlc
        Get coin's OHLC (Beta)
        Candle’s body:
        1 - 2 days: 30 minutes
        3 - 30 days: 4 hours
        31 and before: 4 days

        * id (string) [required] - pass the coin id (can be obtained from /coins) eg. bitcoin
        * vs_currency (string) [required]  - The target currency of market data (usd, eur, jpy, etc.)
        * days (int) [required] - Data up to number of days ago (eg. 1,14,30,max)
        """

        # TODO: IDEA ADD METHOD TO PARSE UNIX TS TO HUMAN READABLE DATE FORMAT IF NEEDED
        params = self._build_payload(locals())
        del params["id"]
        return self._request("GET", f"coins/{id}/ohlc", params=params)


