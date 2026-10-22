-- Apply as the migration owner. Provision the enat_app LOGIN/password separately.
-- Never grant enat_app to anon, authenticated, or service_role.
begin;
do $$ begin
  if not exists (select 1 from pg_roles where rolname='enat_app') then
    create role enat_app nologin nosuperuser nobypassrls;
  end if;
  if not exists (select 1 from pg_roles where rolname='enat_worker') then
    create role enat_worker nologin nosuperuser nobypassrls;
  end if;
end $$;
alter role enat_app nosuperuser nobypassrls;
alter role enat_worker nosuperuser nobypassrls;
revoke create on schema public from public;
grant usage on schema public to enat_app, enat_worker;

alter table users add column if not exists telegram_id text,
  add column if not exists first_name text,
  add column if not exists username text,
  add column if not exists disabled_at timestamptz;
create unique index if not exists users_telegram_id_unique on users(telegram_id) where telegram_id is not null;
create table user_identities (
  provider text not null check (provider in ('supabase','telegram')),
  subject text not null,
  user_id uuid not null references users(id) on delete cascade,
  primary key(provider, subject), unique(user_id, provider)
);
-- Existing email ownership is re-verified by Auth on each login/request.
insert into user_identities select 'supabase', id::text, id from users where email is not null;
insert into user_identities select 'telegram', telegram_id, id from users where telegram_id is not null;
create table app_sessions (
  token_hash text primary key, source_hash text not null unique,
  user_id uuid not null references users(id) on delete cascade,
  expires_at timestamptz not null, revoked_at timestamptz
);
create table auth_invalid_before (subject text primary key, invalid_before timestamptz not null);
create table auth_revocations (session_id uuid primary key, expires_at timestamptz not null);
create table push_tokens (
  id uuid primary key default gen_random_uuid(), user_id uuid not null references users(id) on delete cascade,
  token text not null unique, platform text not null check(platform in ('web','android','ios')),
  updated_at timestamptz not null default now()
);
create table summary_shares (
  id uuid primary key default gen_random_uuid(), summary_id uuid not null references summaries(id),
  user_id uuid not null references users(id), token_hash text not null unique,
  scope text not null check(scope='structured-v1'), consent_at timestamptz not null default now(),
  expires_at timestamptz not null, revoked_at timestamptz,
  created_at timestamptz not null default now(),
  check(expires_at > created_at and expires_at <= created_at + interval '7 days')
);
create index summary_shares_owner on summary_shares(user_id, summary_id);
-- Invalidate legacy public credentials. They are never accepted by the new resolver.
alter table summaries alter column share_link_slug drop not null;
update summaries set share_link_slug=null, qr_code_url=null;

create function enat_user_id() returns uuid language sql stable security definer
set search_path=pg_catalog,public as $$
 select id from public.users where id=nullif(current_setting('app.user_id',true),'')::uuid and disabled_at is null
$$;
create function enat_resolve_identity(p_provider text,p_subject text,p_email text,p_first text,p_username text)
returns jsonb language plpgsql security definer set search_path=pg_catalog,public as $$
declare uid uuid; result jsonb;
begin
 if p_provider not in ('supabase','telegram') or length(p_subject)>128 then raise exception 'Invalid identity'; end if;
 perform pg_advisory_xact_lock(hashtextextended(p_provider || ':' || p_subject,0));
 select user_id into uid from public.user_identities where provider=p_provider and subject=p_subject;
 if uid is null then
   uid := case when p_provider='supabase' then p_subject::uuid else gen_random_uuid() end;
   -- Preserve existing IDs but never attach a provider to another provider's UUID.
   if exists(select 1 from public.users where id=uid) then raise exception 'Identity conflict'; end if;
   insert into public.users(id,email,telegram_id,first_name,username)
   values(uid,p_email,case when p_provider='telegram' then p_subject end,p_first,p_username);
   insert into public.user_identities values(p_provider,p_subject,uid);
 end if;
 select to_jsonb(u) into result from public.users u where id=uid and disabled_at is null;
 return result;
end $$;
create function enat_link_identity(p_provider text,p_subject text) returns boolean
language plpgsql security definer set search_path=pg_catalog,public as $$
declare uid uuid := public.enat_user_id(); existing uuid;
begin
 if uid is null or p_provider not in ('supabase','telegram') then return false; end if;
 perform pg_advisory_xact_lock(hashtextextended(p_provider || ':' || p_subject,0));
 select user_id into existing from public.user_identities where provider=p_provider and subject=p_subject;
 if existing is not null then return existing=uid; end if;
 if exists(select 1 from public.user_identities where user_id=uid and provider=p_provider) then return false; end if;
 insert into public.user_identities values(p_provider,p_subject,uid);
 return true;
end $$;
create function enat_telegram_session(p_subject text,p_first text,p_username text,p_token text,p_source text,p_expiry timestamptz)
returns jsonb language plpgsql security definer set search_path=pg_catalog,public as $$
declare u jsonb;
begin
 if p_expiry>now()+interval '16 minutes' or p_expiry<=now() then raise exception 'Invalid expiry'; end if;
 u := public.enat_resolve_identity('telegram',p_subject,null,p_first,p_username);
 if u is null then return null; end if;
 insert into public.app_sessions values(p_token,p_source,(u->>'id')::uuid,p_expiry,null) on conflict(source_hash) do nothing;
 if not found then return null; end if;
 return u;
end $$;
create function enat_get_session(p_token text) returns jsonb language sql security definer
set search_path=pg_catalog,public as $$
 select to_jsonb(u) from public.app_sessions s join public.users u on u.id=s.user_id
 where s.token_hash=p_token and s.expires_at>now() and s.revoked_at is null and u.disabled_at is null
$$;
create function enat_revoke_session(p_token text) returns void language sql security definer
set search_path=pg_catalog,public as $$ update public.app_sessions set revoked_at=now() where token_hash=p_token $$;
create function enat_auth_revoked(p_session uuid,p_subject text default null,p_iat double precision default null) returns boolean language sql security definer
set search_path=pg_catalog,public as $$ select exists(select 1 from public.auth_revocations where session_id=p_session and expires_at>now()) or exists(select 1 from public.auth_invalid_before where subject=p_subject and (p_iat is null or to_timestamp(p_iat)<=invalid_before)) $$;
create function enat_revoke_user_auth(p_subject text) returns void language sql security definer
set search_path=pg_catalog,public as $$ insert into public.auth_invalid_before values(p_subject,now()) on conflict(subject) do update set invalid_before=excluded.invalid_before $$;
create function enat_revoke_auth(p_session uuid,p_expiry timestamptz) returns void language sql security definer
set search_path=pg_catalog,public as $$ insert into public.auth_revocations values(p_session,p_expiry) on conflict(session_id) do update set expires_at=greatest(auth_revocations.expires_at,excluded.expires_at) $$;
create function enat_read_share(p_hash text) returns jsonb language sql security definer
set search_path=pg_catalog,public as $$
 select jsonb_build_object('period_start',s.period_start,'period_end',s.period_end,'generated_at',s.generated_at,'content_json',s.content_json)
 from public.summary_shares sh join public.summaries s on s.id=sh.summary_id and s.user_id=sh.user_id
 join public.users u on u.id=sh.user_id
 where sh.token_hash=p_hash and sh.expires_at>now() and sh.revoked_at is null and u.disabled_at is null and sh.scope='structured-v1'
$$;

-- Remove direct access by Supabase client roles, including the service credential.
do $$ declare t text; r text; begin
 foreach t in array array['users','supplements','appointments','check_ins','summaries','check_in_sessions','reminders','push_tokens','summary_shares','user_identities','app_sessions','auth_revocations','auth_invalid_before','stage_audio_prompts'] loop
   execute format('alter table public.%I enable row level security',t);
   execute format('revoke all on public.%I from public',t);
   foreach r in array array['anon','authenticated','service_role'] loop
     if exists(select 1 from pg_roles where rolname=r) then execute format('revoke all on public.%I from %I',t,r); end if;
   end loop;
 end loop;
 foreach t in array array['supplements','appointments','check_ins','check_in_sessions','reminders','push_tokens','summary_shares'] loop
   execute format('grant select,insert,update,delete on public.%I to enat_app',t);
   execute format('create policy owner_access on public.%I to enat_app using(user_id=public.enat_user_id()) with check(user_id=public.enat_user_id())',t);
 end loop;
end $$;
grant select,insert on summaries to enat_app;
create policy summary_owner on summaries to enat_app using(user_id=enat_user_id()) with check(user_id=enat_user_id());
grant select on users to enat_app;
grant update(email,first_name,username,age,area,pregnancy_counting_method,lnmp_date,ultrasound_date,ultrasound_weeks,gestational_age_weeks,gestational_age_days,is_gestational_age_manual,effective_lnmp_date,estimated_due_date,trimester,total_pregnancies,live_births,had_c_section,child_passed_away,past_pregnancy_complications,known_medical_conditions,custom_medical_condition,malaria_endemic_area,current_medications,hospital,onboarding_completed) on users to enat_app;
create policy user_owner on users to enat_app using(id=enat_user_id()) with check(id=enat_user_id());
-- A share cannot claim another owner's summary even when its user_id is correct.
create function enat_share_owner() returns trigger language plpgsql set search_path=pg_catalog,public as $$
begin
 if not exists(select 1 from public.summaries where id=new.summary_id and user_id=new.user_id) then raise exception 'Invalid summary owner'; end if;
 return new;
end $$;
create trigger summary_share_owner before insert or update on summary_shares for each row execute function enat_share_owner();
grant select on stage_audio_prompts to enat_app;
create policy generic_prompt_read on stage_audio_prompts for select to enat_app using(true);
-- Workers receive no patient-history or identity permissions in this phase.
grant select,insert,update on reminders to enat_worker;
create policy reminder_worker on reminders to enat_worker using(true) with check(true);

-- No client may invoke privileged functions through PostgREST.
do $$ declare f regprocedure; r text; begin
 for f in select p.oid::regprocedure from pg_proc p join pg_namespace n on n.oid=p.pronamespace where n.nspname='public' and p.proname like 'enat_%' loop
   execute format('revoke all on function %s from public',f);
   foreach r in array array['anon','authenticated','service_role'] loop
     if exists(select 1 from pg_roles where rolname=r) then execute format('revoke all on function %s from %I',f,r); end if;
   end loop;
   execute format('grant execute on function %s to enat_app',f);
 end loop;
end $$;
do $$ begin
 if to_regclass('storage.buckets') is not null then
   update storage.buckets set public=false where id='summary-qr-codes';
 end if;
 if to_regclass('storage.objects') is not null then
   execute 'create policy enat_generic_audio_no_insert on storage.objects as restrictive for insert to public with check (bucket_id <> ''audio-prompts'')';
   execute 'create policy enat_generic_audio_no_update on storage.objects as restrictive for update to public using (bucket_id <> ''audio-prompts'') with check (bucket_id <> ''audio-prompts'')';
   execute 'create policy enat_generic_audio_no_delete on storage.objects as restrictive for delete to public using (bucket_id <> ''audio-prompts'')';
   execute 'create policy enat_private_patient_qr on storage.objects as restrictive for all to public using (bucket_id <> ''summary-qr-codes'') with check (bucket_id <> ''summary-qr-codes'')';
 end if;
end $$;
commit;
