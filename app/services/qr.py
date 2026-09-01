import io
import os
import secrets

import qrcode

from app.config import get_settings
from app.db.client import get_supabase_client


def generate_qr_png(url: str) -> bytes:
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def upload_qr_code(slug: str, url: str) -> str:
    settings = get_settings()
    client = get_supabase_client()
    png_bytes = generate_qr_png(url)
    path = f"{slug}.png"

    client.storage.from_("summary-qr-codes").upload(
        path,
        png_bytes,
        file_options={"content-type": "image/png", "upsert": "true"},
    )

    public_url = client.storage.from_("summary-qr-codes").get_public_url(path)
    return public_url


def generate_share_slug() -> str:
    return secrets.token_urlsafe(12)


def build_share_url(slug: str) -> str:
    settings = get_settings()
    
    # 1. Check settings or environment variables
    base = getattr(settings, "public_base_url", None) or os.getenv("PUBLIC_BASE_URL") or os.getenv("FRONTEND_URL")
    
    # 2. Prevent baking localhost into production QR codes
    if not base or "localhost" in base:
        base = os.getenv("FRONTEND_URL", "https://enat-tena.onrender.com")
        
    base = base.rstrip("/")
    return f"{base}/summary/{slug}"