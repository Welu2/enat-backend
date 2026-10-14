import io

import qrcode
from qrcode.exceptions import DataOverflowError

from app.core.errors import ArtifactUnavailable


def generate_qr_png(url: str) -> bytes:
    try:
        return _render_png(url)
    except (OSError, ValueError, DataOverflowError) as exc:
        raise ArtifactUnavailable("QR rendering unavailable") from exc


def _render_png(url: str) -> bytes:
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()
