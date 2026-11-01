-- Migration 013: User Calendar Items and Tasks
create table if not exists calendar_items (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references users(id) on delete cascade,
  title text not null,
  title_am text,
  type text not null check(type in ('event', 'task')),
  date date not null,
  time time,
  reminder_at timestamptz,
  completed boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists idx_calendar_items_user_date on calendar_items(user_id, date asc, time asc);

alter table calendar_items enable row level security;
revoke all on calendar_items from public;

do $$ declare r text; begin
  foreach r in array array['anon','authenticated','service_role'] loop
    if exists(select 1 from pg_roles where rolname=r) then execute format('revoke all on calendar_items from %I',r); end if;
  end loop;
  if exists(select 1 from pg_roles where rolname='enat_app') then
    grant select,insert,update,delete on calendar_items to enat_app;
    create policy owner_access on calendar_items to enat_app using(user_id=public.enat_user_id()) with check(user_id=public.enat_user_id());
  end if;
  if exists(select 1 from pg_roles where rolname='enat_worker') then
    grant select on calendar_items to enat_worker;
  end if;
end $$;
