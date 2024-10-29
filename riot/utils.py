import enum


class GameType(enum.StrEnum):
    TFT = "tft"
    LOL = "lol"
    VAL = "valorant"


class QueryType(enum.StrEnum):
    LEAGUE = "league"
    SUMMONER = "summoner"
    MATCH = "match"


class VersionType(enum.StrEnum):
    V1 = "v1"


class TierType(enum.StrEnum):
    CHALLENGER = "challenger"
    GRANDMASTER = "grandmaster"
    MASTER = "master"
