from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class GeckoConfig:
    BASE_URL: str = 'https://api.coingecko.com/api/v3/'
    RETRY_STRATEGY: Retry = Retry(total=3, status_forcelist=[429, 500, 502, 503, 504],
                                   method_whitelist=["HEAD", "GET", "OPTIONS"])
    ADAPTER: HTTPAdapter = HTTPAdapter(max_retries=RETRY_STRATEGY)

    @classmethod
    def from_dct(cls, dct):
        return cls()