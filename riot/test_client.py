import datetime
import os

from absl.testing import absltest
from absl.testing import parameterized
import dotenv

from riot import client
from riot import objects
from riot import platform_and_region
from riot.utils import types


class RiotApiClientTests(parameterized.TestCase):
    def setUp(self):
        dotenv.load_dotenv("./riot/.env")
        self._client = client.RiotApiClient(api_key=os.getenv("RIOT_API_KEY"))
        self._test_config = {
            "game_type": types.GameType.TFT,
            "query_type": types.QueryType.LEAGUE,
            "version_type": types.VersionType.V1,
            "region": platform_and_region.Region.ASIA,
            "platform": platform_and_region.Platform.KR,
            "start": 0,
            "count": 1,
        }

    @parameterized.parameters(
        [
            {"match_ids": ["KR_7348987032"]},
        ]
    )
    def test_get_match_data_by_match_ids(self, match_ids: list[str]):
        match_data = self._client.get_match_data_by_match_ids(
            match_ids=match_ids,
            **self._test_config,
        )
        self.assertNotEmpty(match_data)
        for data in match_data:
            self.assertIsNotNone(data)
            self.assertIsInstance(data, objects.MatchDTO)

    @parameterized.parameters(
        [
            {"summoner_ids": ["MAIkveeoM-x5qjW1OLt3G4tD1Q-7T5A2H_QZXv54CDKR3Nu7"]},
        ]
    )
    def test_get_summoner_data_by_summoner_ids(self, summoner_ids: list[str]):
        summoner_data = self._client.get_summoner_data_by_summoner_ids(
            summoner_ids=summoner_ids,
            **self._test_config,
        )
        self.assertNotEmpty(summoner_data)
        for data in summoner_data:
            self.assertIsNotNone(data)
            self.assertIsInstance(data, objects.LeagueEntryDTO)

    @parameterized.parameters(
        [
            {
                "puuids": [
                    "hF_PCQfUjhsbb5puY2UvSChhJmISAQ9ki-jmBn_ro1u8oweRMA4YTD4rBseUCj8Tsh2TaegkJIdwHA"
                ],  # pylint: disable=line-too-long
                "start_time": int(datetime.datetime.fromisoformat("2024-11-01").timestamp()),
                "end_time": int(datetime.datetime.fromisoformat("2024-11-02").timestamp()),
            }
        ]
    )
    def test_get_match_ids_by_puuids(self, puuids: list[str], start_time: int, end_time: int):
        match_ids = self._client.get_match_ids_by_puuids(
            puuids=puuids,
            start_time=start_time,
            end_time=end_time,
            **self._test_config,
        )
        self.assertNotEmpty(match_ids)
        for data in match_ids:
            self.assertNotEmpty(data)

    @parameterized.parameters(
        [
            {"tier": types.TierType.CHALLENGER, "division": types.DivisionType.I},
            {"tier": types.TierType.BRONZE, "division": types.DivisionType.II},
        ]
    )
    def test_get_league_entries_by_tier(self, tier: types.TierType, division: types.DivisionType):
        entries = self._client.get_league_entries_by_tier(
            tier=tier,
            division=division,
            **self._test_config,
        )
        self.assertNotEmpty(entries)
        for data in entries:
            self.assertIn(type(data), [objects.LeagueEntryDTO, objects.LeagueItemDTO])


if __name__ == "__main__":
    absltest.main()
