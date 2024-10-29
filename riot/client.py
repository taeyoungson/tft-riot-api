import json
from typing import Any

from loguru import logger
import requests
from requests.exceptions import HTTPError

from riot import utils

_DEFAULT_REQUEST_TIMEOUT = 30


class RiotApiClient:
    def __init__(self, api_key: str):
        self._api_key = api_key

    def _print_error_msg(self, error_code: int) -> str:
        match error_code:
            case 400:
                return "Bad request"
            case 401:
                return "Unauthorized"
            case 403:
                return "Forbidden"
            case 404:
                return "Not found"
            case 405:
                return "Method Not Allowed"
            case 415:
                return "Unsupported Media Type"
            case 429:
                return "Rate Limit Exceeded"
            case 500:
                return "Internal Server Error"
            case 502:
                return "Bad Gateway"
            case 503:
                return "Service unavailable"
            case 504:
                return "Gateway Timeout"
            case _:
                return "Unknown Error"

    @property
    def _api_base(self) -> str:
        return "https://{platform_or_region}.api.riotgames.com"

    @property
    def _headers(self) -> dict[str, str]:
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",  # pylint: disable=line-too-long
            "Accept-Language": "en-US,en;q=0.9,ko;q=0.8",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": self._api_key,
        }

    def _request(
        self, method: str, url: str, params: dict | None = None, timeout: int = _DEFAULT_REQUEST_TIMEOUT, **kwargs
    ) -> dict[str, Any]:
        try:
            response = requests.request(method=method, url=url, params=params, timeout=timeout, **kwargs)
            response.raise_for_status()
        except HTTPError as err:
            logger.error(self._print_error_msg(response.status_code))
            raise err

        return json.loads(response.text)

    def _get(
        self,
        url: str,
        params: dict | None = None,
        timeout: int = _DEFAULT_REQUEST_TIMEOUT,
        **kwargs,
    ) -> dict[str, Any]:
        return self._request(
            "GET",
            url,
            params=params,
            headers=self._headers,
            timeout=timeout,
            **kwargs,
        )

    def _make_request_url(
        self,
        platform_or_region: str,
        game_type: str,
        query_type: str,
        version_type: str,
    ) -> str:
        return "/".join(
            [
                self._api_base.format(platform_or_region=platform_or_region),
                game_type,
                query_type,
                version_type,
            ]
        )

    def fetch(
        self,
        game_type: utils.GameType,
        query_type: utils.QueryType,
        version_type: utils.VersionType,
        platform_or_region: str,
        extra_url: str | None = None,
        params: dict | None = None,
    ) -> dict[str, Any]:
        url = self._make_request_url(
            platform_or_region=platform_or_region,
            game_type=game_type,
            query_type=query_type,
            version_type=version_type,
        )

        if extra_url:
            url = url + "/" + extra_url

        return self._get(url=url, params=params)
