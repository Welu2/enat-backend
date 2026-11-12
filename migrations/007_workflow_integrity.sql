-- Coordinated client rollout: versions, canonical collections and durable results.
alter table check_in_sessions add column version bigint not null default 0 check(version >= 0);
alter table check_in_sessions add column stage_status text not null default 'awaiting_response'
  check(stage_status in ('awaiting_response','awaiting_confirmation','ready','completed'));
alter table check_in_sessions add column completed_stages jsonb not null default '{}';
alter table check_in_sessions add column terminal_result jsonb;
alter table check_in_sessions add constraint session_owner_unique unique(id,user_id);
update check_in_sessions set stage_status=case when status='completed' then 'completed'
  when jsonb_array_length(pending_items)>0 then 'awaiting_confirmation' else 'awaiting_response' end;

create function enat_item_collection(value jsonb) returns jsonb language sql immutable
set search_path=pg_catalog,public as $$
  with expanded as (
    select jsonb_array_elements(case when value is null or value='null'::jsonb then '[]'::jsonb
      when jsonb_typeof(value)='array' then value
      when jsonb_typeof(value)='object' then jsonb_build_array(value)
      else jsonb_build_array(jsonb_build_object('legacy_value',value)) end) as item
  )
  select coalesce(jsonb_agg(case
    when jsonb_typeof(item) <> 'object' then jsonb_build_object('legacy_value',item,'verification_status','legacy_unverified')
    when item->'confirmed' is distinct from 'true'::jsonb then item || '{"verification_status":"legacy_unverified"}'::jsonb
    else item end), '[]'::jsonb) from expanded
$$;
update check_ins set food_log=enat_item_collection(food_log), supplement_check=enat_item_collection(supplement_check),
 symptoms=enat_item_collection(symptoms),closing_mentions=enat_item_collection(closing_mentions);
update check_in_sessions set draft_data=jsonb_build_object(
 'symptoms',enat_item_collection(draft_data->'symptoms'),
 'food_log',enat_item_collection(draft_data->'food_log'),
 'supplement_check',enat_item_collection(draft_data->'supplement_check'),
 'closing_mentions',enat_item_collection(draft_data->'closing_mentions'));
drop function enat_item_collection(jsonb);
-- Old clients cannot safely resume under the new version/confirmation contract.
-- Retain drafts for inspection; require a new session rather than fabricating provenance.
update check_in_sessions set status='expired', expires_at=least(expires_at,now()) where status='in_progress';

alter table check_ins alter column symptoms set default '[]'::jsonb;
alter table check_ins alter column food_log set default '[]'::jsonb;
alter table check_ins alter column supplement_check set default '[]'::jsonb;
alter table check_ins alter column closing_mentions set default '[]'::jsonb;
alter table check_ins add column session_id uuid unique;
alter table check_ins add constraint checkin_session_owner foreign key(session_id,user_id) references check_in_sessions(id,user_id);
alter table check_ins add column policy_version text;
create function enat_confirmed_checkin() returns trigger language plpgsql
set search_path=pg_catalog,public as $$
declare field text; item jsonb;
begin
 foreach field in array array['symptoms','food_log','supplement_check','closing_mentions'] loop
  if jsonb_typeof(to_jsonb(new)->field) is distinct from 'array' then
   raise exception 'Clinical collections must be arrays' using errcode='23514';
  end if;
  for item in select jsonb_array_elements(to_jsonb(new)->field) loop
   if item->'confirmed' is distinct from 'true'::jsonb or
      coalesce(item->>'confirmed_at','')='' or coalesce(item->>'source_item_id','')='' or
      coalesce(item->>'policy_version','')='' then
    raise exception 'Explicit confirmation provenance required' using errcode='23514';
   end if;
  end loop;
 end loop;
 return new;
end $$;
create trigger checkin_confirmation before insert or update on check_ins for each row execute function enat_confirmed_checkin();

create table mutation_results (
 user_id uuid not null references users(id) on delete cascade,
 operation text not null, key text not null check(length(key) between 8 and 128),
 request_hash text not null, result jsonb not null, created_at timestamptz not null default now(),
 primary key(user_id,operation,key)
);
create table domain_outbox (
 id uuid primary key default gen_random_uuid(), user_id uuid not null references users(id) on delete cascade,
 event_type text not null, aggregate_id uuid not null, payload jsonb not null default '{}',
 created_at timestamptz not null default now(), delivered_at timestamptz,
 unique(event_type,aggregate_id)
);
alter table mutation_results enable row level security;
alter table domain_outbox enable row level security;
revoke all on mutation_results,domain_outbox from public;
grant select,insert on mutation_results,domain_outbox to enat_app;
create policy mutation_owner on mutation_results to enat_app using(user_id=enat_user_id()) with check(user_id=enat_user_id());
create policy outbox_owner on domain_outbox to enat_app using(user_id=enat_user_id()) with check(user_id=enat_user_id());
-- Worker consumption and leases are introduced in Phase 3, not the API process.

alter table summaries add column window_start timestamptz;
alter table summaries add column window_end timestamptz;
alter table summaries add constraint summary_window_order check(window_end > window_start);
alter table summaries add column generation_key text;
create unique index summaries_generation_unique on summaries(user_id,generation_key) where generation_key is not null;
create function enat_immutable_summary() returns trigger language plpgsql set search_path=pg_catalog,public as $$
begin raise exception 'Summary snapshots are immutable' using errcode='23514'; end $$;
create trigger summary_immutable before update on summaries for each row execute function enat_immutable_summary();

alter table appointments add column status text not null default 'scheduled' check(status in ('scheduled','completed','missed'));
alter table appointments add column version bigint not null default 0;
create table appointment_events (
 id uuid primary key default gen_random_uuid(), user_id uuid not null references users(id) on delete cascade,
 appointment_id uuid not null, action text not null check(action in ('completed','missed','rescheduled')),
 previous_date date not null, new_date date, created_at timestamptz not null default now()
);
alter table appointment_events enable row level security;
revoke all on appointment_events from public;
grant select,insert on appointment_events to enat_app;
create policy appointment_event_owner on appointment_events to enat_app using(user_id=enat_user_id()) with check(user_id=enat_user_id());
revoke all on function enat_confirmed_checkin(),enat_immutable_summary() from public;
-- Projects may define default grants; revoke these explicitly for new tables.
do $$ declare role_name text; begin
 foreach role_name in array array['anon','authenticated','service_role'] loop
  if exists(select 1 from pg_roles where rolname=role_name) then
   execute format('revoke all on mutation_results,domain_outbox,appointment_events from %I',role_name);
   execute format('revoke all on function enat_confirmed_checkin(),enat_immutable_summary() from %I',role_name);
  end if;
 end loop;
end $$;
