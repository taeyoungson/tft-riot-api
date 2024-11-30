import datetime

import pytest
from pytest_mock import MockerFixture

from riot import client
from riot.utils import platform_and_region
from riot.utils import types


@pytest.fixture(name="riot_client")
def setup_client() -> client.RiotApiClient:
    """Fixture to set up client instance and test configuration."""
    return client.RiotApiClient(api_key="this-is-a-api-key")


@pytest.fixture(name="test_config")
def setup_config() -> dict[str, str]:
    return {
        "game_type": types.GameType.TFT,
        "query_type": types.QueryType.LEAGUE,
        "version_type": types.VersionType.V1,
        "region": platform_and_region.Region.ASIA,
        "platform": platform_and_region.Platform.KR,
        "start": 0,
        "count": 1,
    }


@pytest.mark.parametrize("match_ids", [["KR_7348987032"]])
def test_get_match_data_by_match_ids(
    mocker: MockerFixture, riot_client: client.RiotApiClient, test_config: dict[str, str], match_ids: list[str]
):
    # Mock the method
    mock_get_match_data = mocker.patch.object(riot_client, "get_match_data_by_match_ids")

    # Call the method
    riot_client.get_match_data_by_match_ids(match_ids=match_ids, **test_config)

    # Verify the call
    mock_get_match_data.assert_called_once_with(match_ids=match_ids, **test_config)


@pytest.mark.parametrize("summoner_ids", [["MAIkveeoM-x5qjW1OLt3G4tD1Q-7T5A2H_QZXv54CDKR3Nu7"]])
def test_get_summoner_data_by_summoner_ids(
    mocker: MockerFixture, riot_client: client.RiotApiClient, test_config: dict[str, str], summoner_ids: list[str]
):
    # Mock the method
    mock_get_summoner_data = mocker.patch.object(riot_client, "get_summoner_data_by_summoner_ids")

    # Call the method
    riot_client.get_summoner_data_by_summoner_ids(summoner_ids=summoner_ids, **test_config)

    # Verify the call
    mock_get_summoner_data.assert_called_once_with(summoner_ids=summoner_ids, **test_config)


@pytest.mark.parametrize(
    "puuids, start_time, end_time",
    [
        (
            ["hF_PCQfUjhsbb5puY2UvSChhJmISAQ9ki-jmBn_ro1u8oweRMA4YTD4rBseUCj8Tsh2TaegkJIdwHA"],
            int(datetime.datetime.fromisoformat("2024-11-01").timestamp()),
            int(datetime.datetime.fromisoformat("2024-11-02").timestamp()),
        )
    ],
)
def test_get_match_ids_by_puuids(
    mocker: MockerFixture,
    riot_client: client.RiotApiClient,
    test_config: dict[str, str],
    puuids: list[str],
    start_time: int,
    end_time: int,
):
    # Mock the method
    mock_get_match_ids = mocker.patch.object(riot_client, "get_match_ids_by_puuids")

    # Call the method
    riot_client.get_match_ids_by_puuids(puuids=puuids, start_time=start_time, end_time=end_time, **test_config)

    # Verify the call
    mock_get_match_ids.assert_called_once_with(puuids=puuids, start_time=start_time, end_time=end_time, **test_config)


@pytest.mark.parametrize(
    "tier, division",
    [
        (types.TierType.CHALLENGER, types.DivisionType.I),
        (types.TierType.BRONZE, types.DivisionType.II),
    ],
)
def test_get_league_entries_by_tier(
    mocker: MockerFixture,
    riot_client: client.RiotApiClient,
    test_config: dict[str, str],
    tier: types.TierType,
    division: types.DivisionType,
):
    # Mock the method
    mock_get_league_entries = mocker.patch.object(riot_client, "get_league_entries_by_tier")

    # Call the method
    riot_client.get_league_entries_by_tier(tier=tier, division=division, **test_config)

    # Verify the call
    mock_get_league_entries.assert_called_once_with(tier=tier, division=division, **test_config)
