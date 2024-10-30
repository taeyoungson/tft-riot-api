import json
from typing import Any

from loguru import logger
import requests
from requests.exceptions import HTTPError

from riot import errors
from riot import objects
from riot import platform_and_region
from riot.utils import types

_DEFAULT_REQUEST_TIMEOUT = 30


class RiotApiClient:
    def __init__(self, api_key: str):
        self._api_key = api_key

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
        self,
        method: str,
        url: str,
        params: dict | None = None,
        timeout: int = _DEFAULT_REQUEST_TIMEOUT,
        **kwargs,
    ) -> dict[str, Any]:
        try:
            response = requests.request(method=method, url=url, params=params, timeout=timeout, **kwargs)
            response.raise_for_status()
        except HTTPError as err:
            logger.error(errors.err_code_to_err_msg(response.status_code))
            raise err

        return json.loads(response.text)

    def _get(
        self,
        url: str,
        params: dict | None = None,
        headers: dict[str, str] | None = None,
        timeout: int = _DEFAULT_REQUEST_TIMEOUT,
        **kwargs,
    ) -> dict[str, Any]:
        return self._request(
            "GET",
            url,
            params=params,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )

    def _build_request_url(
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

    def _fetch(
        self,
        game_type: types.GameType,
        query_type: types.QueryType,
        version_type: types.VersionType,
        platform: platform_and_region.Platform | None = None,
        region: platform_and_region.Region | None = None,
        extra_url: str | None = None,
        params: dict | None = None,
    ) -> dict[str, Any] | list:
        if (platform and region) or (not platform and not region):
            logger.error("Only one of platform or region must be specified")
        platform_or_region = platform or region

        url = self._build_request_url(
            platform_or_region=str(platform_or_region),
            game_type=game_type,
            query_type=query_type,
            version_type=version_type,
        )

        if extra_url:
            url = url + "/" + extra_url

        return self._get(url=url, params=params, headers=self._headers)

    def get_league_data_by_tier(
        self,
        tier: types.TierType,
        game_type: types.GameType,
        version_type: types.VersionType,
        platform: platform_and_region.Platform,
        queue: str = "RANKED_TFT",
        **kwargs,  # pylint: disable=unused-argument
    ) -> objects.LeagueListDTO:
        return objects.LeagueListDTO.from_dict(
            self._fetch(
                game_type=game_type,
                query_type=types.QueryType.LEAGUE,
                version_type=version_type,
                platform=platform,
                extra_url=tier,
                params={"queue": queue},
            )
        )

    def _get_summoner_data_by_summoner_id(
        self,
        summoner_id: str,
        game_type: types.GameType,
        version_type: types.VersionType,
        platform: platform_and_region.Platform,
        **kwargs,  # pylint: disable=unused-argument
    ) -> objects.LeagueEntryDTO:
        entry = self._fetch(
            game_type=game_type,
            query_type=types.QueryType.LEAGUE,
            version_type=version_type,
            platform=platform,
            extra_url=f"entries/by-summoner/{summoner_id}",
        )

        if not len(entry) == 1:
            logger.warning(f"Something wrong! len(entries) is not 1 but {len(entry)} for id: {summoner_id}")

        return objects.LeagueEntryDTO.from_dict(entry[0])

    def _get_match_ids_by_puuid(
        self,
        puuid: str,
        game_type: types.GameType,
        version_type: types.VersionType,
        region: platform_and_region.Region,
        start: int,
        start_time: int,
        end_time: int,
        **kwargs,  # pylint: disable=unused-argument
    ) -> list[int]:
        return self._fetch(
            game_type=game_type,
            query_type=types.QueryType.MATCH,
            version_type=version_type,
            region=region,
            extra_url=f"matches/by-puuid/{puuid}/ids",
            params={"start": start, "startTime": start_time, "endTime": end_time},
        )

    def get_match_ids_by_puuids(
        self,
        puuids: list[str],
        **kwargs,
    ) -> list[list[int]]:
        return [self._get_match_ids_by_puuid(pid, **kwargs) for pid in puuids]

    def get_summoner_data_by_summoner_ids(self, summoner_ids: list[str], **kwargs) -> list[objects.LeagueEntryDTO]:
        return [self._get_summoner_data_by_summoner_id(summoner_id, **kwargs) for summoner_id in summoner_ids]

    def _get_match_data_by_match_id(
        self,
        match_id: str,
        game_type: types.GameType,
        version_type: types.VersionType,
        region: platform_and_region.Region,
        **kwargs,  # pylint: disable=unused-argument
    ) -> objects.MatchDTO:
        return objects.MatchDTO.from_dict(
            self._fetch(
                game_type=game_type,
                query_type=types.QueryType.MATCH,
                version_type=version_type,
                region=region,
                extra_url=f"matches/{match_id}",
            )
        )

    def get_match_data_by_match_ids(self, match_ids: list[str], **kwargs) -> list[objects.MatchDTO]:
        return [self._get_match_data_by_match_id(m_id, **kwargs) for m_id in match_ids]
