from __future__ import annotations
import ast
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
