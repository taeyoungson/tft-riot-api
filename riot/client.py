import ast
import os

import dotenv
from riot import platform_and_region
from riot import utils
from riot import objects
from loguru import logger

class RiotApiClient:
    def __init__(self, api_key: str, platform_or_region: platform_and_region.Platform | platform_and_region.Region):
        self._api_key = api_key
        self._platform_or_region = platform_or_region

        self._client = None

    @property
    def _api_base(self) -> str:
        return f"https://{self._platform_or_region}.api.riotgames.com"

    @property
    def _headers(self) -> dict[str, str]:
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9,ko;q=0.8",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": self._api_key,
        }

class TFTApiClient(RiotApiClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._query_type = "tft"

    def get_challenger_data(self, match_type: str, version: str) -> objects.LeagueListDTO:
        response = utils.get(
            url=f"{self._api_base}/{self._query_type}/{match_type}/{version}/challenger/",
            headers=self._headers,
            params={
                "queue": "RANKED_TFT",
            },
        )

        return objects.LeagueListDTO.from_dict(response)

# TODO(ty.son): temporary test code
def main():
    # TODO(ty.son): remove this line
    dotenv.load_dotenv("./riot/.env")

    kr_tft_client = TFTApiClient(
        api_key=os.getenv("RIOT_API_KEY"),
        platform_or_region=platform_and_region.Platform.KR,
    )
    response = kr_tft_client.get_challenger_data(match_type="league", version="v1")
    logger.info(response)

if __name__ == "__main__":
    main()