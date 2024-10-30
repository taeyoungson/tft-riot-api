import datetime
import os

import dotenv
from loguru import logger

from riot import client
from riot import platform_and_region
from riot.utils import types

_DEFAULT_SEARCH_CONFIG = {
    "game_type": types.GameType.TFT,
    "query_type": types.QueryType.LEAGUE,
    "version_type": types.VersionType.V1,
    "region": platform_and_region.Region.ASIA,
    "platform": platform_and_region.Platform.KR,
    "start": 0,
    "start_time": int(datetime.datetime(2024, 6, 1, 0, 0).timestamp()),
    "end_time": int(datetime.datetime(2024, 10, 30, 0, 0).timestamp()),
}


# TODO(ty.son): temporary usage example
def main():
    # TODO(ty.son): temporally get api key from .env
    dotenv.load_dotenv("./riot/.env")

    # 1. Initialize client
    riot_api_client = client.RiotApiClient(api_key=os.getenv("RIOT_API_KEY"))

    # 2. Get challenger-tier league data.
    challenger_league_data = riot_api_client.get_league_data_by_tier(
        tier=types.TierType.CHALLENGER, **_DEFAULT_SEARCH_CONFIG
    )

    # 3. Collect summoner ids of active challngers
    summoner_ids = []
    for entry in challenger_league_data.entries:
        if not entry.inactive:
            summoner_ids.append(entry.summoner_id)

    # 4. Get summoner data by summoner ids
    summoner_data = riot_api_client.get_summoner_data_by_summoner_ids(summoner_ids[:5], **_DEFAULT_SEARCH_CONFIG)

    # 5. Collect puuids from summoner data
    puuids = [d.puuid for d in summoner_data]

    # 6. Get Match Ids by puuids.
    match_ids = riot_api_client.get_match_ids_by_puuids(puuids, **_DEFAULT_SEARCH_CONFIG)

    # 7. Get Match Datas by match ids
    match_data = riot_api_client.get_match_data_by_match_ids(match_ids[0], **_DEFAULT_SEARCH_CONFIG)

    logger.info(
        f"""
            Example Output
            - LeagueList DTO
                {challenger_league_data}
            =============================
            - Summoner IDs
                {summoner_ids[0]}
                ...
            =============================
            - Summoner Data
                {summoner_data[0]}
                ...
            =============================
            - Match Ids
                {match_ids[0]}
            =============================
            - Match Data
                {match_data[0]}
        """
    )


if __name__ == "__main__":
    main()
