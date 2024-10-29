import os

import dotenv
from loguru import logger

from riot import client
from riot import objects
from riot import platform_and_region
from riot import utils


# TODO(ty.son): temporary usage example
def main():
    # TODO(ty.son): temporally get api key from .env
    dotenv.load_dotenv("./riot/.env")

    default_search_config = {
        "game_type": utils.GameType.TFT,
        "query_type": utils.QueryType.LEAGUE,
        "version_type": utils.VersionType.V1,
        "platform_or_region": platform_and_region.Platform.KR,
    }

    riot_api_client = client.RiotApiClient(api_key=os.getenv("RIOT_API_KEY"))

    challenger_league_data = riot_api_client.fetch(
        **default_search_config, extra_url=utils.TierType.CHALLENGER, params={"queue": "RANKED_TFT"}
    )
    challenger_league_data = objects.LeagueListDTO.from_dict(challenger_league_data)
    summoner_ids = [e.summoner_id for e in challenger_league_data.entries]

    summoner_data = []
    # TODO(ty.son) fix rate limit exceeding
    for summoner_id in summoner_ids:
        summoner_datum = riot_api_client.fetch(
            **default_search_config,
            extra_url=f"entries/by-summoner/{summoner_id}",
        )
        summoner_data.append(summoner_datum)
        break

    summoner_data = [objects.LeagueEntryDTO.from_dict(s[0]) for s in summoner_data]

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
        """
    )


if __name__ == "__main__":
    main()
