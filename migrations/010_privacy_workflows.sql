-- Additive privacy controls. No clinical retention period or purge is inferred.
create table privacy_requests (
 id uuid primary key default gen_random_uuid(),
 user_id uuid not null references users(id),
 kind text not null default 'deletion' check(kind='deletion'),
 status text not null default 'requested' check(status in ('requested','cancelled')),
 created_at timestamptz not null default now(), cancelled_at timestamptz,
 check((status='cancelled') = (cancelled_at is not null))
);
create unique index privacy_request_active on privacy_requests(user_id) where status='requested';
create index privacy_request_owner on privacy_requests(user_id,id);
create table privacy_events (
 id uuid primary key default gen_random_uuid(),
 user_id uuid not null references users(id),
 event text not null check(event in ('export_page','request_created','request_cancelled','share_created','share_revoked','share_read')),
 actor text not null check(actor in ('patient','share_recipient')),
 resource text not null check(resource in ('profile','supplements','appointments','appointment_events','check_ins','drafts','summaries','reminders','shares','requests','audit')),
 resource_id uuid, row_count integer check(row_count between 0 and 100),
 occurred_at timestamptz not null default now()
);
create index privacy_event_owner on privacy_events(user_id,id);
create index privacy_request_queue on privacy_requests(created_at,id) where status='requested';
alter table privacy_requests enable row level security;
alter table privacy_events enable row level security;
revoke all on privacy_requests,privacy_events from public;
grant select on privacy_requests,privacy_events to enat_app;
create policy privacy_request_owner on privacy_requests to enat_app using(user_id=enat_user_id());
create policy privacy_event_owner on privacy_events to enat_app using(user_id=enat_user_id());
do $$ begin
 if not exists(select 1 from pg_roles where rolname='enat_privacy_operator') then
  create role enat_privacy_operator nologin nosuperuser nobypassrls;
 end if;
end $$;
grant usage on schema public to enat_privacy_operator;
grant select on privacy_requests,privacy_events to enat_privacy_operator;
create policy privacy_request_operator on privacy_requests to enat_privacy_operator using(true);
create policy privacy_event_operator on privacy_events to enat_privacy_operator using(true);

create function enat_privacy_event(p_resource text,p_count integer) returns void
language plpgsql security definer set search_path=pg_catalog,public as $$
declare uid uuid := public.enat_user_id();
begin
 if uid is null then raise exception 'Verified identity required' using errcode='42501'; end if;
 insert into public.privacy_events(user_id,event,actor,resource,row_count)
 values(uid,'export_page','patient',p_resource,p_count);
end $$;
create function enat_privacy_request(p_cancel uuid default null) returns jsonb
language plpgsql security definer set search_path=pg_catalog,public as $$
declare uid uuid := public.enat_user_id(); result public.privacy_requests;
begin
 if uid is null then raise exception 'Verified identity required' using errcode='42501'; end if;
 perform pg_advisory_xact_lock(hashtextextended('privacy-request:' || uid::text,0));
 if p_cancel is null then
  select * into result from public.privacy_requests where user_id=uid and status='requested';
  if not found then
   insert into public.privacy_requests(user_id) values(uid) returning * into result;
  end if;
 else
  update public.privacy_requests set status='cancelled',cancelled_at=now()
   where id=p_cancel and user_id=uid and status='requested' returning * into result;
  if not found then
   select * into result from public.privacy_requests where id=p_cancel and user_id=uid;
  end if;
 end if;
 return case when result.id is null then null else to_jsonb(result) end;
end $$;
create function enat_privacy_request_audit() returns trigger language plpgsql
security definer set search_path=pg_catalog,public as $$ begin
 insert into public.privacy_events(user_id,event,actor,resource,resource_id)
 values(new.user_id,case when TG_OP='INSERT' then 'request_created' else 'request_cancelled' end,'patient','requests',new.id);
 return new;
end $$;
create trigger privacy_request_audit after insert or update on privacy_requests
 for each row execute function enat_privacy_request_audit();
create function enat_privacy_audit_immutable() returns trigger language plpgsql
set search_path=pg_catalog,public as $$ begin
 raise exception 'Audit events are immutable' using errcode='23514';
end $$;
create trigger privacy_audit_immutable before update or delete on privacy_events
 for each row execute function enat_privacy_audit_immutable();

create function enat_share_audit() returns trigger language plpgsql
security definer set search_path=pg_catalog,public as $$ begin
 if TG_OP='INSERT' or (old.revoked_at is null and new.revoked_at is not null) then
  insert into public.privacy_events(user_id,event,actor,resource,resource_id)
  values(new.user_id,case when TG_OP='INSERT' then 'share_created' else 'share_revoked' end,'patient','shares',new.id);
 end if;
 return new;
end $$;
create trigger share_audit after insert or update on summary_shares for each row execute function enat_share_audit();
create or replace function enat_read_share(p_hash text) returns jsonb language plpgsql security definer
set search_path=pg_catalog,public as $$
declare result jsonb; uid uuid; sid uuid;
begin
 select jsonb_build_object('period_start',s.period_start,'period_end',s.period_end,'generated_at',s.generated_at,'content_json',s.content_json),sh.user_id,s.id
 into result,uid,sid from public.summary_shares sh
 join public.summaries s on s.id=sh.summary_id and s.user_id=sh.user_id
 join public.users u on u.id=sh.user_id
 where sh.token_hash=p_hash and sh.expires_at>now() and sh.revoked_at is null
 and u.disabled_at is null and sh.scope='structured-v1';
 if result is not null then
  insert into public.privacy_events(user_id,event,actor,resource,resource_id)
  values(uid,'share_read','share_recipient','summaries',sid);
 end if;
 return result;
end $$;

-- Keep UUID cursor pages bounded by an owner index even for large histories.
create index checkin_export_owner on check_ins(user_id,id);
create index session_export_owner on check_in_sessions(user_id,id);
create index summary_export_owner on summaries(user_id,id);
create index reminder_export_owner on reminders(user_id,id);
create index supplement_export_owner on supplements(user_id,id);
create index appointment_event_export_owner on appointment_events(user_id,id);

revoke all on function enat_privacy_event(text,integer),enat_privacy_request(uuid),
 enat_privacy_request_audit(),enat_privacy_audit_immutable(),enat_share_audit() from public;
grant execute on function enat_privacy_event(text,integer),enat_privacy_request(uuid) to enat_app;
do $$ declare r text; begin
 foreach r in array array['anon','authenticated','service_role'] loop
  if exists(select 1 from pg_roles where rolname=r) then
   execute format('revoke all on privacy_requests,privacy_events from %I',r);
   execute format('revoke all on function enat_privacy_event(text,integer),enat_privacy_request(uuid),enat_privacy_request_audit(),enat_privacy_audit_immutable(),enat_share_audit() from %I',r);
  end if;
 end loop;
end $$;

-- Aggregate queue telemetry contains no user identifiers or clinical payloads.
create function enat_privacy_queue() returns jsonb language sql security definer
set search_path=pg_catalog,public as $$
 select jsonb_build_object('pending',count(*),'oldest_seconds',
 coalesce(extract(epoch from now()-min(created_at)),0))
 from public.privacy_requests where status='requested'
$$;
revoke all on function enat_privacy_queue() from public;
grant execute on function enat_privacy_queue() to enat_worker;
do $$ declare r text; begin
 foreach r in array array['anon','authenticated','service_role'] loop
  if exists(select 1 from pg_roles where rolname=r) then
   execute format('revoke all on function enat_privacy_queue() from %I',r);
  end if;
 end loop;
end $$;
