# TFT Riot API


## Setting up

1. Install poetry
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. In repository root, execute following
```bash
poetry shell
poetry install
```
You are set!

If you added another python package, add it to pyproject.toml under [tool.poetry.dependencies]. and regenerate lock file using
```bash
poetry lock
```

## Running example script
To test current state of code,

```bash
python example.py
--tier challenger
--start_date 2024-10-31
```

Example output is following:

```bash
Example Output
    - LeagueList DTO
    League Id: 4e57fec2-f77a-3045-a35f-193af9e08963
    Tier: CHALLENGER
    Name: Syndra's Corruptors
    Queue: RANKED_TFT
    Entries: 300 number of entries.

    =============================
    
    - Summoner IDs
        jcO5Tkhu_Y82HRt8AOTSiCPC2QN204S7bSA39rsHdUYU3HTFid0hF5HxZA
        ...
    =============================
    
    - Summoner Data
    PUUID: CkFzkJ3KGUz3RnbBNhJ75NBM8SbSf2aNg9E7IjlsqUI3axhaWfQ4H0uF4PLyKnG1PR3dFuHAtBBIYw
    League ID: 4e57fec2-f77a-3045-a35f-193af9e08963
    Summon ID: jcO5Tkhu_Y82HRt8AOTSiCPC2QN204S7bSA39rsHdUYU3HTFid0hF5HxZA
    Queue Type: RANKED_TFT
    Tier: CHALLENGER
    Rank: I
    League Points: 1835
    Wins: 260
    Losses: 142
    Hot Streak: False
    Veteran: True
    Fresh Blood: False
    Inactive: False
    Mini Series: 0 number of mini-series.
    ==============================
    
    - Match Ids
    - Match Datas
    ...
```



Document references [here](https://developer.riotgames.com/)