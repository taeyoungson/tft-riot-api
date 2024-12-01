import pydantic_settings


class PostgresSQlSettings(pydantic_settings.BaseSettings):
    host: str
    port: int
    user: str
    password: str

    model_config = pydantic_settings.SettingsConfigDict(
        env_prefix="DB_",
        env_file=".env.postgres",
    )


def load_settings() -> PostgresSQlSettings:
    return PostgresSQlSettings()  # pylint: disable=no-value-for-parameter
