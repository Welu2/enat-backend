from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, File, Form, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, checkin, notifications, reminders, summary, tts, users
from app.config import get_settings
from app.services.speech import get_asr_client
from app.services.reminders import ReminderService

from typing import Any
import time

scheduler = BackgroundScheduler()


def _run_reminder_job() -> None:
    ReminderService().run_daily_job()


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings = get_settings()
    scheduler.add_job(
        _run_reminder_job,
        trigger="cron",
        hour=settings.reminder_cron_hour,
        minute=0,
        id="daily_reminders",
        replace_existing=True,
    )
    scheduler.start()
    yield
    scheduler.shutdown(wait=False)


app = FastAPI(
    title="EnatAI Clinical Intake Backend",
    version="0.1.0",
    lifespan=lifespan,
)

settings = get_settings()

# Whitelist production web, development, and Telegram Web clients
allowed_origins = list(
    {
        *settings.cors_origin_list,
        "https://enat-tena.onrender.com",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://web.telegram.org",
        "https://webk.telegram.org",
        "https://webz.telegram.org",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(checkin.router)
app.include_router(summary.router)
app.include_router(reminders.router)
app.include_router(notifications.router)
app.include_router(tts.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


if settings.enable_dev_routes:

    @app.post("/dev/asr-test")
    async def dev_asr_test(
        audio: UploadFile = File(...),
        model: str = Form("addisai"),
        model_query: str | None = Query(None, alias="model"),
    ) -> dict[str, str]:
        selected_model = model_query or model or "addisai"
        audio_bytes = await audio.read()
        client = get_asr_client(selected_model)
        transcript = await client.transcribe(
            audio_bytes,
            audio.filename or "audio.wav",
            audio.content_type or "audio/wav",
        )
        return {"transcript": transcript, "model": selected_model}

    @app.post("/dev/benchmark-stt")
    async def dev_benchmark_stt(
        files: list[UploadFile] = File(...),
        language_code: str | None = Form(None),
        language_query: str | None = Query(None, alias="language_code"),
        stage_label: str | None = Form(None),
        stage_query: str | None = Query(None, alias="stage_label"),
        models: str | None = Form(None),
        models_query: str | None = Query(None, alias="models"),
        gemini_model: str | None = Form(None),
        gemini_model_query: str | None = Query(None, alias="gemini_model"),
    ) -> dict[str, Any]:
        """Dev-only benchmark endpoint comparing STT models sequentially on an audio batch.

        - Amharic: Sahara, Addis AI, Gemini
        - English: Sahara, Deepgram, Gemini
        """
        from app.services.addis_ai import AddisAIClient
        from app.services.deepgram import DeepgramClient
        from app.services.gemini import GeminiTranscribeClient
        from app.services.sahara import SaharaVoiceClient

        raw_lang = language_query or language_code or "am"
        clean_lang = "en" if str(raw_lang).strip().lower().startswith("en") else "am"
        effective_stage = (stage_query or stage_label or "").strip() or "symptoms"

        sahara_client = SaharaVoiceClient()
        gemini_client = GeminiTranscribeClient()

        if clean_lang == "en":
            deepgram_client = DeepgramClient()
            model_pipeline = [
                ("sahara", sahara_client),
                ("deepgram", deepgram_client),
                ("gemini", gemini_client),
            ]
        else:
            addis_client = AddisAIClient()
            model_pipeline = [
                ("sahara", sahara_client),
                ("addis_ai", addis_client),
                ("gemini", gemini_client),
            ]

        raw_models = models_query or models
        if raw_models:
            requested = [m.strip().lower() for m in raw_models.split(",") if m.strip()]
            if requested:
                model_pipeline = [p for p in model_pipeline if p[0] in requested]

        results = []
        for file in files:
            filename = file.filename or "audio.wav"
            content_type = file.content_type or "audio/wav"
            audio_bytes = await file.read()

            models_output: dict[str, Any] = {}
            for model_name, client in model_pipeline:
                start_time = time.perf_counter()
                try:
                    kwargs: dict[str, Any] = {
                        "filename": filename,
                        "content_type": content_type,
                        "language": clean_lang,
                    }
                    if model_name == "gemini":
                        effective_gemini_model = gemini_model_query or gemini_model
                        if effective_gemini_model:
                            kwargs["model"] = effective_gemini_model

                    transcript = await client.transcribe(
                        audio_bytes,
                        **kwargs,
                    )
                    latency = round(time.perf_counter() - start_time, 2)
                    models_output[model_name] = {
                        "hypothesis_text": transcript,
                        "latency_seconds": latency,
                    }
                except Exception as exc:
                    latency = round(time.perf_counter() - start_time, 2)
                    models_output[model_name] = {
                        "error": str(exc),
                        "latency_seconds": latency,
                    }

            results.append({
                "filename": filename,
                "stage_label": effective_stage,
                "models": models_output,
            })

        return {"results": results}