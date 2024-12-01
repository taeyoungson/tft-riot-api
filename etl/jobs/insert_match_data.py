import datetime

from absl import app
from absl import flags
from loguru import logger
from psycopg.types.json import Json
import tqdm

from etl.postgresql import client as postgresql_client
from riot import client as riot_client
from riot.utils import search
from riot.utils import types

_TABLE_NAME = "match"

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


def main(_):
    riot_api_client = riot_client.RiotApiClient()
    postgresql_db = postgresql_client.PostgresDB()
    search_overrides = {
        "start_time": int(datetime.datetime.fromisoformat(FLAGS.start_date).timestamp()),
        "end_time": int(datetime.datetime.fromisoformat(FLAGS.end_date).timestamp()),
    }
    default_search_config = search.SearchConfig.load_default_config(**search_overrides)

    tier_entries = riot_api_client.get_league_entries_by_tier(
        tier=FLAGS.tier, division=FLAGS.division, **default_search_config.as_dict()
    )

    summoner_ids = []
    for entry in tier_entries:
        if not entry.inactive:
            summoner_ids.append(entry.summoner_id)

    summoner_data = riot_api_client.get_summoner_data_by_summoner_ids(
        summoner_ids=summoner_ids, **default_search_config.as_dict()
    )

    puuids = [data.puuid for data in summoner_data]
    match_ids = riot_api_client.get_match_ids_by_puuids(puuids=puuids, **default_search_config.as_dict())
    for match_id in tqdm.tqdm(match_ids, desc="Inserting match data into DB..."):
        match_data = riot_api_client.get_match_data_by_match_ids(match_id, **default_search_config.as_dict())
        for data in match_data:
            for match_data_dict in data.as_lists_of_dict():
                match_data_dict = {k: Json(v) if isinstance(v, dict) else v for k, v in match_data_dict.items()}
                match_data_dict["tier"] = FLAGS.tier
                postgresql_db.insert(table=_TABLE_NAME, data=match_data_dict)
    logger.info("Insertion complete")


if __name__ == "__main__":
    app.run(main)
