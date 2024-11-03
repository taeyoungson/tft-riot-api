from __future__ import annotations

import datetime

import pydantic

from riot.utils import platform_and_region
from riot.utils import types


class SearchConfig(pydantic.BaseModel):
    game_type: types.GameType
    query_type: types.QueryType
    version_type: types.VersionType
    region: platform_and_region.Region
    platform: platform_and_region.Platform
    start: int
    start_time: int
    end_time: int
    count: int

    @classmethod
    def _load_default_config(cls) -> SearchConfig:
        return cls(
            game_type=types.GameType.TFT,
            query_type=types.QueryType.LEAGUE,
            version_type=types.VersionType.V1,
            region=platform_and_region.Region.ASIA,
            platform=platform_and_region.Platform.KR,
            start=0,
            start_time=int((datetime.datetime.now() - datetime.timedelta(days=7)).timestamp()),
            end_time=int(datetime.datetime.now().timestamp()),
            count=20,
        )

    @classmethod
    def load_default_config(cls, **overrides) -> SearchConfig:
        """Load default config for tft league search with overrides.

        Args:
            **overrides: Overrides for default config.

        Returns:
            SearchConfig: Default search config for tft league search with overrides.
        """
        return cls._load_default_config().copy(update=overrides)  # pylint: disable=protected-access

    def as_dict(self) -> dict:
        return {
            "game_type": self.game_type,
            "query_type": self.query_type,
            "version_type": self.version_type,
            "region": self.region,
            "platform": self.platform,
            "start": self.start,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "count": self.count,
        }
