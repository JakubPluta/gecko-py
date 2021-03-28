from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from dataclasses import dataclass


@dataclass
class Config:
    BASE_URL: str
    RETRY_STRATEGY: Retry
    ADAPTER: HTTPAdapter
    SESSION: bool = True


    @classmethod
    def from_dct(cls, dct):
        return cls()

@dataclass
class GeckoConfig(Config):
    BASE_URL: str = 'https://api.coingecko.com/api/v3/'
    RETRY_STRATEGY: Retry = Retry(total=3, status_forcelist=[429, 500, 502, 503, 504],
                                   method_whitelist=["HEAD", "GET", "OPTIONS"])
    ADAPTER: HTTPAdapter = HTTPAdapter(max_retries=RETRY_STRATEGY)
    SESSION = True

    @classmethod
    def from_dct(cls, dct):
        return cls()