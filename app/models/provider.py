"""Validated Addis wire payloads; unknown vendor metadata never reaches callers."""

from pydantic import BaseModel, ConfigDict, Field


class ProviderFields(BaseModel):
    model_config = ConfigDict(strict=True, extra="ignore")
    text: str | None = None
    transcription: str | None = None
    response_text: str | None = None
    response: str | None = None
    content: str | None = None
    audio_base64: str | None = None
    audio_content: str | None = None
    audio: str | None = None

    def generated_text(self) -> str:
        return self.response_text or self.response or self.text or self.content or ""


class ProviderChoice(ProviderFields):
    message: ProviderFields | None = None


class ProviderEnvelope(ProviderFields):
    data: ProviderFields | str | None = None
    choices: list[ProviderChoice] = Field(default_factory=list, max_length=10)
