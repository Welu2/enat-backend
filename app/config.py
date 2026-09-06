from functools import lru_cache

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Prevents crashes if extra environment variables exist
    )

    supabase_url: str
    supabase_service_role_key: str
    supabase_jwt_secret: str
    addis_api_key: str
    addis_api_base_url: str = "https://api.addisassistant.com"
    intron_api_key: str = Field(
        default="",
        validation_alias=AliasChoices(
            "intron_api_key",
            "INTRON_API_KEY",
            "sahara_api_key",
            "SAHARA_API_KEY",
        ),
    )
    intron_api_base_url: str = Field(
        default="https://infer.voice.intron.io",
        validation_alias=AliasChoices(
            "intron_api_base_url",
            "INTRON_API_BASE_URL",
            "sahara_api_base_url",
            "SAHARA_API_BASE_URL",
        ),
    )
    gemini_api_key: str = Field(
        default="",
        validation_alias=AliasChoices("gemini_api_key", "GEMINI_API_KEY"),
    )
    gemini_api_base_url: str = Field(
        default="https://generativelanguage.googleapis.com",
        validation_alias=AliasChoices("gemini_api_base_url", "GEMINI_API_BASE_URL"),
    )
    gemini_transcribe_model: str = Field(
        default="gemini-3.5-transcribe",
        validation_alias=AliasChoices("gemini_transcribe_model", "GEMINI_TRANSCRIBE_MODEL"),
    )
    gemini_chat_model: str = Field(
        default="gemini-2.5-flash",
        validation_alias=AliasChoices("gemini_chat_model", "GEMINI_CHAT_MODEL"),
    )
    elevenlabs_api_key: str = Field(
        default="",
        validation_alias=AliasChoices(
            "elevenlabs_api_key",
            "ELEVENLABS_API_KEY",
            "xi_api_key",
            "XI_API_KEY",
        ),
    )
    elevenlabs_api_base_url: str = Field(
        default="https://api.elevenlabs.io",
        validation_alias=AliasChoices("elevenlabs_api_base_url", "ELEVENLABS_API_BASE_URL"),
    )
    elevenlabs_voice_id: str = Field(
        default="21m00Tcm4TlvDq8ikWAM",
        validation_alias=AliasChoices("elevenlabs_voice_id", "ELEVENLABS_VOICE_ID"),
    )
    elevenlabs_model_id: str = Field(
        default="eleven_multilingual_v2",
        validation_alias=AliasChoices("elevenlabs_model_id", "ELEVENLABS_MODEL_ID"),
    )
    elevenlabs_stt_model_id: str = Field(
        default="scribe_v1",
        validation_alias=AliasChoices("elevenlabs_stt_model_id", "ELEVENLABS_STT_MODEL_ID"),
    )
    deepgram_api_key: str = Field(
        default="",
        validation_alias=AliasChoices("deepgram_api_key", "DEEPGRAM_API_KEY"),
    )
    deepgram_api_base_url: str = Field(
        default="https://api.deepgram.com",
        validation_alias=AliasChoices("deepgram_api_base_url", "DEEPGRAM_API_BASE_URL"),
    )
    deepgram_stt_model: str = Field(
        default="nova-2",
        validation_alias=AliasChoices("deepgram_stt_model", "DEEPGRAM_STT_MODEL"),
    )
    deepgram_tts_model: str = Field(
        default="aura-asteria-en",
        validation_alias=AliasChoices("deepgram_tts_model", "DEEPGRAM_TTS_MODEL"),
    )
    public_base_url: str = "http://localhost:3000"
    cors_origins: str = "http://localhost:3000"
    enable_dev_routes: bool = True
    reminder_cron_hour: int = 6
    
    # Telegram Bot Token from @BotFather
    telegram_bot_token: str = ""

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


    @property
    def is_telegram_configured(self) -> bool:
        return bool(self.telegram_bot_token.strip())

    @property
    def sahara_api_key(self) -> str:
        return self.intron_api_key

    @property
    def sahara_api_base_url(self) -> str:
        return self.intron_api_base_url


@lru_cache
def get_settings() -> Settings:
    return Settings()