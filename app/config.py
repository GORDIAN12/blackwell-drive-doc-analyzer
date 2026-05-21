from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    anthropic_api_key: str = Field(..., alias="ANTHROPIC_API_KEY")
    claude_model: str = Field(default="claude-sonnet-4-6", alias="CLAUDE_MODEL")

    google_credentials_file: str = Field(default="credentials.json", alias="GOOGLE_CREDENTIALS_FILE")
    google_token_file: str = Field(default="token.json", alias="GOOGLE_TOKEN_FILE")

    output_dir: str = Field(default="outputs", alias="OUTPUT_DIR")
    log_file: str = Field(default="logs/app.log", alias="LOG_FILE")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()