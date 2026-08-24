-- Migration 004: Table to store pre-generated audio for static check-in stage prompts

create table if not exists stage_audio_prompts (
  stage text primary key,
  prompt_am text not null,
  prompt_en text not null,
  category_am text not null,
  category_en text not null,
  audio_bytes bytea,
  audio_url text,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);
