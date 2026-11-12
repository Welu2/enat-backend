from pydantic import BaseModel


class ErrorResponse(BaseModel):
    detail: str
    code: str | None = None
    draft_preserved: bool | None = None
    recovery: list[str] | None = None
