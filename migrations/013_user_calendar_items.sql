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

grant all on calendar_items to service_role;
grant select, insert, update, delete on calendar_items to authenticated;

do $$ begin
  if not exists (
    select 1 from pg_policies where tablename = 'calendar_items' and policyname = 'calendar_items_owner_policy'
  ) then
    create policy calendar_items_owner_policy on calendar_items
      for all
      to authenticated
      using (user_id = auth.uid())
      with check (user_id = auth.uid());
  end if;
end $$;
