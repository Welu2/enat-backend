-- Legacy unverified records may receive timestamp metadata, never fabricated confirmation.
drop trigger checkin_confirmation on check_ins;
create trigger checkin_confirmation before insert or update of symptoms,food_log,supplement_check,closing_mentions,policy_version
 on check_ins for each row execute function enat_confirmed_checkin();
alter table check_ins add column recorded_at timestamptz;
alter table check_ins add column received_at timestamptz;
alter table check_ins add column client_confirmed_at timestamptz;
alter table check_ins add column capture_source text not null default 'online' check(capture_source in ('online','offline_form'));
alter table check_ins add column client_submission_id uuid;
alter table check_ins add column submission_hash text;
update check_ins set recorded_at=timestamp,received_at=timestamp;
alter table check_ins alter column recorded_at set not null;
alter table check_ins alter column received_at set not null;
create unique index offline_submission_unique on check_ins(user_id,client_submission_id) where client_submission_id is not null;
create index checkin_observation_time on check_ins(user_id,recorded_at,id);
alter table check_ins add constraint offline_provenance check(
 (capture_source='online' and client_submission_id is null and submission_hash is null and client_confirmed_at is null)
 or (capture_source='offline_form' and client_submission_id is not null and submission_hash ~ '^[0-9a-f]{64}$'
 and submission_hash is not null and client_confirmed_at is not null and recorded_at<=client_confirmed_at
 and client_confirmed_at<=received_at+interval '5 minutes'));
-- Retain compatibility with existing SQL insert callers and the fallback image.
create function enat_checkin_times() returns trigger language plpgsql set search_path=pg_catalog,public as $$ begin
 new.received_at:=coalesce(new.received_at,new.timestamp);
 new.recorded_at:=coalesce(new.recorded_at,new.timestamp);
 if new.timestamp is distinct from new.received_at then raise exception 'Receipt timestamp mismatch' using errcode='23514'; end if;
 return new;
end $$;
create trigger checkin_times before insert or update of timestamp,received_at,recorded_at on check_ins
 for each row execute function enat_checkin_times();
revoke all on function enat_checkin_times() from public;
do $$ declare r text; begin
 foreach r in array array['anon','authenticated','service_role'] loop
  if exists(select 1 from pg_roles where rolname=r) then execute format('revoke all on function enat_checkin_times() from %I',r); end if;
 end loop;
end $$;
