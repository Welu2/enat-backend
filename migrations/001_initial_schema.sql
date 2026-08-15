-- Initial schema for EnatAI backend

create extension if not exists "pgcrypto";

create table if not exists users (
  id uuid primary key,
  email text,
  created_at timestamptz not null default now()
);

create table if not exists supplements (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references users(id) on delete cascade,
  name text not null,
  active boolean not null default true,
  reminder_enabled boolean not null default true,
  reminder_time time,
  created_at timestamptz not null default now()
);

create table if not exists appointments (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references users(id) on delete cascade,
  appointment_date date not null,
  last_summary_generated_at timestamptz,
  reminder_lead_days int not null default 2,
  unique (user_id)
);

create table if not exists check_ins (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references users(id) on delete cascade,
  timestamp timestamptz not null default now(),
  symptoms jsonb,
  food_log jsonb,
  supplement_check jsonb,
  closing_mentions jsonb,
  danger_sign_triggered boolean not null default false
);

create table if not exists summaries (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references users(id) on delete cascade,
  period_start date not null,
  period_end date not null,
  generated_at timestamptz not null default now(),
  content_json jsonb not null,
  share_link_slug text not null unique,
  qr_code_url text
);

create table if not exists check_in_sessions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references users(id) on delete cascade,
  current_stage text not null,
  stage_order jsonb not null,
  draft_data jsonb not null default '{}'::jsonb,
  pending_items jsonb not null default '[]'::jsonb,
  status text not null default 'in_progress',
  created_at timestamptz not null default now(),
  expires_at timestamptz not null
);

create table if not exists reminders (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references users(id) on delete cascade,
  type text not null,
  message text not null,
  due_at timestamptz not null,
  dismissed boolean not null default false,
  created_at timestamptz not null default now()
);

create index if not exists idx_check_ins_user_timestamp on check_ins(user_id, timestamp desc);
create index if not exists idx_summaries_user_generated on summaries(user_id, generated_at desc);
create index if not exists idx_reminders_user_due on reminders(user_id, due_at);

alter table users enable row level security;
alter table supplements enable row level security;
alter table appointments enable row level security;
alter table check_ins enable row level security;
alter table summaries enable row level security;
alter table check_in_sessions enable row level security;
alter table reminders enable row level security;

-- Storage bucket for QR codes (run in Supabase dashboard or via API):
-- create bucket summary-qr-codes (public read)
