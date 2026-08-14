# EnatAI Backend

FastAPI backend for the voice-based Amharic clinical intake app.

## Setup

1. Create a Supabase project and run [`migrations/001_initial_schema.sql`](migrations/001_initial_schema.sql).
2. Create a public storage bucket named `summary-qr-codes`.
3. Copy `.env.example` to `.env` and fill in credentials.
4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run the server:

```bash
uvicorn app.main:app --reload --app-dir backend
```

## Dev ASR Test

Set `ENABLE_DEV_ROUTES=true` and POST audio to `POST /dev/asr-test`.

## Tests

```bash
pytest backend/tests
```
