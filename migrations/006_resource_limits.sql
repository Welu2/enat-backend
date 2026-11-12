begin;
create table request_limits (bucket text primary key, used bigint not null, expires_at timestamptz not null);
create index request_limits_expiry on request_limits(expires_at);
create table provider_leases (id uuid primary key, expires_at timestamptz not null);
alter table request_limits enable row level security;
alter table provider_leases enable row level security;
revoke all on request_limits,provider_leases from public;
create function enat_take_rate(p_bucket text,p_limit int,p_seconds int) returns boolean
language plpgsql security definer set search_path=pg_catalog,public as $$
declare amount bigint;
begin
 if p_limit<1 or p_seconds not between 1 and 86400 then return false; end if;
 insert into public.request_limits values(p_bucket,1,now()+make_interval(secs=>p_seconds))
 on conflict(bucket) do update set
 used=case when request_limits.expires_at<=now() then 1 else request_limits.used+1 end,
 expires_at=case when request_limits.expires_at<=now() then now()+make_interval(secs=>p_seconds) else request_limits.expires_at end
 returning used into amount;
 -- Bounded opportunistic cleanup; there is also a worker maintenance procedure.
 if amount%100=0 then
   delete from public.request_limits where bucket in (select bucket from public.request_limits where expires_at<now()-interval '1 day' limit 100);
 end if;
 return amount<=p_limit;
end $$;
create function enat_acquire_provider(p_limit int) returns uuid language plpgsql security definer
set search_path=pg_catalog,public as $$
declare lease uuid := gen_random_uuid();
begin
 perform pg_advisory_xact_lock(836916284);
 delete from public.provider_leases where expires_at<=now();
 if (select count(*) from public.provider_leases)>=p_limit then return null; end if;
 insert into public.provider_leases values(lease,now()+interval '90 seconds');
 return lease;
end $$;
create function enat_release_provider(p_id uuid) returns void language sql security definer
set search_path=pg_catalog,public as $$ delete from public.provider_leases where id=p_id $$;
create function enat_cleanup_security_state() returns void language plpgsql security definer
set search_path=pg_catalog,public as $$ begin
 delete from public.request_limits where expires_at<now()-interval '1 day';
 delete from public.provider_leases where expires_at<now();
 delete from public.app_sessions where expires_at<now()-interval '1 day';
 delete from public.auth_revocations where expires_at<now();
end $$;
revoke all on function enat_take_rate(text,int,int),enat_acquire_provider(int),enat_release_provider(uuid),enat_cleanup_security_state() from public;
grant execute on function enat_take_rate(text,int,int),enat_acquire_provider(int),enat_release_provider(uuid) to enat_app;
grant execute on function enat_cleanup_security_state() to enat_worker;
-- Revoke any Supabase default function/table grants as well.
do $$ declare r text; begin
 foreach r in array array['anon','authenticated','service_role'] loop
 if exists(select 1 from pg_roles where rolname=r) then
 execute format('revoke all on request_limits,provider_leases from %I',r);
 execute format('revoke all on function enat_take_rate(text,int,int),enat_acquire_provider(int),enat_release_provider(uuid),enat_cleanup_security_state() from %I',r);
 end if; end loop;
end $$;
commit;
