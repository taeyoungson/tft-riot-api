from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class MiniSeriesDTO:
    losses: int
    progress: str
    target: int
    wins: int

    @classmethod
    def from_dict(cls, d: dict[str, str]) -> MiniSeriesDTO:
        return cls(
            losses=int(d["losses"]),
            progress=d["progress"],
            target=int(d["target"]),
            wins=int(d["wins"]),
        )


@dataclasses.dataclass
class LeagueEntryDTO:
    puuid: str
    league_id: str
    summoner_id: str
    queue_type: str
    tier: str
    rank: str
    league_points: int
    wins: int
    losses: int
    hot_streak: bool
    veteran: bool
    fresh_blood: bool
    inactive: bool
    mini_series: list[MiniSeriesDTO]

    @classmethod
    def from_dict(cls, d: dict[str, str]) -> LeagueEntryDTO:
        return cls(
            puuid=d["puuid"],
            league_id=d["leagueId"],
            summoner_id=d["summonerId"],
            queue_type=d["queueType"],
            tier=d["tier"],
            rank=d["rank"],
            league_points=int(d["leaguePoints"]),
            wins=int(d["wins"]),
            losses=int(d["losses"]),
            hot_streak=bool(d["hotStreak"]),
            veteran=bool(d["veteran"]),
            fresh_blood=bool(d["freshBlood"]),
            inactive=bool(d["inactive"]),
            mini_series=[MiniSeriesDTO.from_dict(m_s) for m_s in d.get("miniSeries", [])],
        )

    def __repr__(self):
        return f"""
            PUUID: {self.puuid}
            League ID: {self.league_id}
            Summon ID: {self.summoner_id}
            Queue Type: {self.queue_type}
            Tier: {self.tier}
            Rank: {self.rank}
            League Points: {self.league_points}
            Wins: {self.wins}
            Losses: {self.losses}
            Hot Streak: {self.hot_streak}
            Veteran: {self.veteran}
            Fresh Blood: {self.fresh_blood}
            Inactive: {self.inactive}
            Mini Series: {len(self.mini_series)} number of mini-serires.
        """


@dataclasses.dataclass
class LeagueItemDTO:
    fresh_blood: bool
    wins: int
    mini_series: list[MiniSeriesDTO]
    inactive: bool
    veteran: bool
    hot_streak: bool
    rank: str
    league_points: int
    losses: int
    summoner_id: str

    @classmethod
    def from_dict(cls, d: dict[str, str]) -> LeagueItemDTO:
        return cls(
            fresh_blood=bool(d["freshBlood"]),
            wins=int(d["wins"]),
            mini_series=[MiniSeriesDTO.from_dict(m_s) for m_s in d.get("miniSeries", [])],
            inactive=bool(d["inactive"]),
            veteran=bool(d["veteran"]),
            hot_streak=bool(d["hotStreak"]),
            rank=d["rank"],
            league_points=int(d["leaguePoints"]),
            losses=int(d["losses"]),
            summoner_id=d["summonerId"],
        )

    def __repr__(self) -> str:
        return f"""
            Fresh Blood: {self.fresh_blood}
            Wins: {self.wins}
            Inactive: {self.inactive}
            Veteran: {self.veteran}
            Hot Streak: {self.hot_streak}
            Rank: {self.rank}
            League Points: {self.league_points}
            Losses: {self.losses}
            Summer ID: {self.summoner_id}
            miniseries: {len(self.mini_series)} number of miniseries.
        """


@dataclasses.dataclass
class LeagueListDTO:
    league_id: str
    entries: list[LeagueItemDTO]
    tier: str
    name: str
    queue: str

    @classmethod
    def from_dict(cls, d: dict[str, str]) -> LeagueListDTO:
        return cls(
            league_id=d["leagueId"],
            entries=[LeagueItemDTO.from_dict(entry) for entry in d["entries"]],
            tier=d["tier"],
            name=d["name"],
            queue=d["queue"],
        )

    def __repr__(self) -> str:
        return f"""
            League Id: {self.league_id}
            Tier: {self.tier}
            Name: {self.name}
            Queue: {self.queue}
            Entries: {len(self.entries)} number of entries.
        """
