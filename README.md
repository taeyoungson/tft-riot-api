# TFT Riot API


## Setting up

0. Get Riot API Key from [here](https://developer.riotgames.com/) and write to `/riot/.env` like
```python
RIOT_API_KEY="RGAPI-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
```

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

API Document references [here](https://developer.riotgames.com/)
