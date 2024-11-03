from __future__ import annotations

import pydantic


class MiniSeriesDTO(pydantic.BaseModel):
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


class LeagueEntryDTO(pydantic.BaseModel):
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
            Summoner ID: {self.summoner_id}
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


class LeagueItemDTO(pydantic.BaseModel):
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


class LeagueListDTO(pydantic.BaseModel):
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


class MetadataDTO(pydantic.BaseModel):
    data_version: str
    match_id: str
    participants_puuids: list[str]

    @classmethod
    def from_dict(cls, d: dict[str, str | list[str]]) -> MetadataDTO:
        return cls(
            data_version=d["data_version"],
            match_id=d["match_id"],
            participants_puuids=d["participants"],
        )


class TraitDTO(pydantic.BaseModel):
    name: str
    num_units: int
    style: int
    tier_current: int
    tier_total: int

    @classmethod
    def from_dict(cls, d: dict[str, str]) -> TraitDTO:
        return cls(
            name=d["name"],
            num_units=int(d["num_units"]),
            style=int(d["style"]),
            tier_current=int(d["tier_current"]),
            tier_total=int(d["tier_total"]),
        )


class UnitDTO(pydantic.BaseModel):
    items: list[int]
    item_names: list[str]
    character_id: str
    chosen: str | None
    name: str
    rarity: int
    tier: int

    @classmethod
    def from_dict(cls, d: dict[str, str, list]) -> UnitDTO:
        return cls(
            items=d.get("items", []),
            item_names=d["itemNames"],
            character_id=d["character_id"],
            chosen=d.get("chosen", None),
            name=d["name"],
            rarity=int(d["rarity"]),
            tier=int(d["tier"]),
        )


class ParticipantDTO(pydantic.BaseModel):
    augments: list[str]
    gold_left: int
    last_round: int
    level: int
    placement: int
    players_eliminated: int
    puuid: str
    riot_id_game_name: str | None
    riot_id_tag_line: str | None
    time_eliminated: float
    total_damage_to_players: int
    traits: list[TraitDTO]
    units: list[UnitDTO]

    @classmethod
    def from_dict(cls, d: dict[str, str | dict | list]) -> ParticipantDTO:
        return cls(
            augments=d["augments"],
            gold_left=int(d["gold_left"]),
            last_round=int(d["last_round"]),
            level=int(d["level"]),
            placement=int(d["placement"]),
            players_eliminated=int(d["players_eliminated"]),
            puuid=d["puuid"],
            riot_id_game_name=d.get("riotIdGameName", None),
            riot_id_tag_line=d.get("riotIdTagline", None),
            time_eliminated=float(d["time_eliminated"]),
            total_damage_to_players=int(d["total_damage_to_players"]),
            traits=[TraitDTO.from_dict(t) for t in d["traits"]],
            units=[UnitDTO.from_dict(u) for u in d["units"]],
        )


class InfoDTO(pydantic.BaseModel):
    game_datetime: float
    game_length: float
    game_version: str
    game_variation: str | None
    participants: list[ParticipantDTO]
    queue_id: int
    tft_set_number: int

    @classmethod
    def from_dict(cls, d: dict[str, str | dict]) -> InfoDTO:
        return cls(
            game_datetime=float(d["game_datetime"]),
            game_length=float(d["game_length"]),
            game_variation=d.get("game_variation", None),
            game_version=d["game_version"],
            participants=[ParticipantDTO.from_dict(p) for p in d["participants"]],
            queue_id=int(d["queue_id"]),
            tft_set_number=int(d["tft_set_number"]),
        )


class MatchDTO(pydantic.BaseModel):
    metadata: MetadataDTO
    info: InfoDTO

    @classmethod
    def from_dict(cls, d: dict[str, str | dict]) -> MatchDTO:
        return cls(
            metadata=MetadataDTO.from_dict(d["metadata"]),
            info=InfoDTO.from_dict(d["info"]),
        )
