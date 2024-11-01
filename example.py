"""
TFT Riot API example script

Usage:
python example.py \
--tier gold
--start_date 2024-10-31
"""

import datetime
import os

from absl import app
from absl import flags
import dotenv
from loguru import logger
import tqdm

from riot import client
from riot import platform_and_region
from riot.utils import types

flags.DEFINE_string("tier", None, "[IRON, BRONZE, SILVER, GOLD, ...]")
flags.DEFINE_string(
    "division", types.DivisionType.I, "Inner rank inside tier, node that (grand)master, challenger has only one tier"
)
flags.DEFINE_string(
    "start_date",
    None,
    "datetime.date format, write in format YYYY-MM-DD",
)
flags.DEFINE_string(
    "end_date",
    datetime.datetime.now().strftime("%Y-%m-%d"),
    "datetime.date format, write in format YYYY-MM-DD",
)

FLAGS = flags.FLAGS


# TODO(ty.son): temporary usage example
def main(_):
    # TODO(ty.son): temporally get api key from .env
    dotenv.load_dotenv("./riot/.env")

    default_search_config = {
        "game_type": types.GameType.TFT,
        "query_type": types.QueryType.LEAGUE,
        "version_type": types.VersionType.V1,
        "region": platform_and_region.Region.ASIA,
        "platform": platform_and_region.Platform.KR,
        "start": 0,
        "start_time": int(datetime.datetime.fromisoformat(FLAGS.start_date).timestamp()),
        "end_time": int(datetime.datetime.fromisoformat(FLAGS.end_date).timestamp()),
    }

    # 0. Log some info
    logger.info(
        f"Scraping tft data for tier: {FLAGS.tier.upper()}:{FLAGS.division}"
        f"for {FLAGS.start_date} ~ {FLAGS.end_date}"
    )

    # 1. Initialize client
    riot_api_client = client.RiotApiClient(api_key=os.getenv("RIOT_API_KEY"))

    # 2. Get challenger-tier league entries.
    tier_entries = riot_api_client.get_league_entries_by_tier(
        tier=FLAGS.tier, division=FLAGS.division, **default_search_config
    )

    # 3. Collect summoner ids of active users
    summoner_ids = []
    for entry in tqdm.tqdm(tier_entries):
        if not entry.inactive:
            summoner_ids.append(entry.summoner_id)

    # 4. Get summoner data by summoner ids
    logger.info(f"Getting number of {len(summoner_ids)} summoner data...")
    summoner_data = riot_api_client.get_summoner_data_by_summoner_ids(summoner_ids, **default_search_config)

    # 5. Collect puuids from summoner data
    puuids = [d.puuid for d in summoner_data]

    # 6. Get Match Ids by puuids.
    match_ids = riot_api_client.get_match_ids_by_puuids(puuids, **default_search_config)

    # 7. Get Match Datas by match ids
    match_data = riot_api_client.get_match_data_by_match_ids(match_ids[0], **default_search_config)

    logger.info(
        f"""
            Example Output
            - Tier Entries
                {tier_entries}
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
    flags.mark_flags_as_required(["tier", "start_date"])
    app.run(main)
