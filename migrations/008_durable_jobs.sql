-- Worker credentials are provisioned separately; API credentials cannot run jobs.
create table background_jobs (
 id uuid primary key default gen_random_uuid(),
 user_id uuid not null references users(id) on delete cascade,
 kind text not null, dedupe_key text not null unique, payload jsonb not null default '{}',
 due_at timestamptz not null default now(), created_at timestamptz not null default now(),
 status text not null default 'pending' check(status in ('pending','running','succeeded','failed')),
 attempts integer not null default 0, max_attempts integer not null default 5,
 lease_token uuid, lease_until timestamptz, heartbeat_at timestamptz,
 finished_at timestamptz, last_error text, replay_count integer not null default 0,
 check(attempts >= 0 and max_attempts between 1 and 20)
);
create index jobs_due on background_jobs(due_at,id) where status='pending';
create index jobs_expired on background_jobs(lease_until) where status='running';
create index outbox_undelivered on domain_outbox(created_at,id) where delivered_at is null;
create table scheduler_state (
 name text primary key, occurrence date not null, cursor_id uuid,
 lease_token uuid, lease_until timestamptz, updated_at timestamptz not null default now()
);
alter table reminders add column occurrence_key text;
create unique index reminder_occurrence on reminders(user_id,occurrence_key) where occurrence_key is not null;
alter table background_jobs enable row level security;
alter table scheduler_state enable row level security;
revoke all on background_jobs,scheduler_state from public,enat_app;
grant select,insert,update on background_jobs to enat_worker;
create policy jobs_worker on background_jobs to enat_worker using(true) with check(true);
grant select on scheduler_state to enat_worker;
create policy scheduler_worker on scheduler_state for select to enat_worker using(true);
grant select,insert,update on domain_outbox to enat_worker;
create policy outbox_worker on domain_outbox to enat_worker using(true) with check(true);
grant execute on function enat_user_id() to enat_worker;
grant select on users,appointments,supplements,check_ins,summaries,mutation_results to enat_worker;
grant insert on summaries,mutation_results to enat_worker;
create policy worker_user on users for select to enat_worker using(id=enat_user_id());
create policy worker_appointment on appointments for select to enat_worker using(user_id=enat_user_id());
create policy worker_supplement on supplements for select to enat_worker using(user_id=enat_user_id());
create policy worker_checkin on check_ins for select to enat_worker using(user_id=enat_user_id());
create policy worker_summary on summaries to enat_worker using(user_id=enat_user_id()) with check(user_id=enat_user_id());
create policy worker_mutation on mutation_results to enat_worker using(user_id=enat_user_id()) with check(user_id=enat_user_id());
drop policy reminder_worker on reminders;
create policy reminder_worker on reminders to enat_worker using(user_id=enat_user_id()) with check(user_id=enat_user_id());

-- A page and its checkpoint commit together. Lease expiry permits takeover.
create function enat_schedule_page(p_token uuid, p_limit integer, p_hour integer)
returns integer language plpgsql security definer set search_path=pg_catalog,public as $$
declare s public.scheduler_state; r record; n integer:=0; local_now timestamp;
begin
 if p_limit not between 1 and 500 or p_hour not between 0 and 23 then
  raise exception 'Invalid scheduler bounds';
 end if;
 local_now:=clock_timestamp() at time zone 'Africa/Addis_Ababa';
 insert into public.scheduler_state(name,occurrence) values('daily',local_now::date)
 on conflict do nothing;
 select * into s from public.scheduler_state where name='daily' for update;
 if s.lease_until>clock_timestamp() and s.lease_token<>p_token then return 0; end if;
 update public.scheduler_state set lease_token=p_token,lease_until=clock_timestamp()+interval '30 seconds',updated_at=clock_timestamp() where name='daily';
 if s.occurrence+make_interval(hours=>p_hour)>local_now then return 0; end if;
 for r in select id from public.users where disabled_at is null
   and created_at < (s.occurrence+1)::timestamp at time zone 'Africa/Addis_Ababa'
   and (s.cursor_id is null or id>s.cursor_id) order by id limit p_limit loop
  insert into public.background_jobs(user_id,kind,dedupe_key,payload,due_at)
   values(r.id,'user.daily','daily:'||r.id||':'||s.occurrence,
    jsonb_build_object('occurrence',s.occurrence),
    (s.occurrence+make_interval(hours=>p_hour)) at time zone 'Africa/Addis_Ababa')
   on conflict(dedupe_key) do nothing;
  s.cursor_id:=r.id; n:=n+1;
 end loop;
 if n<p_limit then s.occurrence:=s.occurrence+1; s.cursor_id:=null; end if;
 update public.scheduler_state set occurrence=s.occurrence,cursor_id=s.cursor_id where name='daily';
 return n;
end $$;
revoke all on function enat_schedule_page(uuid,integer,integer) from public;
grant execute on function enat_schedule_page(uuid,integer,integer) to enat_worker;
do $$ declare r text; begin
 foreach r in array array['anon','authenticated','service_role'] loop
  if exists(select 1 from pg_roles where rolname=r) then
   execute format('revoke all on background_jobs,scheduler_state from %I',r);
   execute format('revoke all on function enat_schedule_page(uuid,integer,integer) from %I',r);
  end if;
 end loop;
end $$;
