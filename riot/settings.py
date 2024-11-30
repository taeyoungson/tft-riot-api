import pydantic_settings


class RiotApiSettings(pydantic_settings.BaseSettings):
    api_key: str

    model_config = pydantic_settings.SettingsConfigDict(
        env_prefix="RIOT_",
        env_file=".env.riot",
    )


def load_settings() -> RiotApiSettings:
    return RiotApiSettings()  # pylint: disable=no-value-for-parameter
