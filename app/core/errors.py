class ApplicationError(RuntimeError):
    """Expected boundary failure; rendered by the single HTTP error mapper."""


class AuthenticationUnavailable(ApplicationError):
    pass


class ProviderUnavailable(ApplicationError):
    """Retry or switch to manual input; the patient's stored draft is intact."""


class DataUnavailable(ApplicationError):
    pass


class RateLimited(ApplicationError):
    pass


class Conflict(ApplicationError):
    """A stale version or conflicting reuse of an idempotency key."""


class NotFound(ApplicationError):
    """An owned resource was not found."""


class InvalidMutation(ApplicationError):
    """The requested state transition or clinical input is invalid."""


class ArtifactUnavailable(ApplicationError):
    """The requested generic audio or private QR artifact is unavailable."""


class FeatureUnavailable(ApplicationError):
    """An explicitly gated feature is disabled."""


class ConsentRequired(ApplicationError):
    """An operation requires explicit patient consent."""


class InvalidAudio(ApplicationError):
    """Unsupported, malformed, or undecodable uploaded audio."""


class PayloadTooLarge(ApplicationError):
    """A bounded upload exceeds its byte or duration budget."""
