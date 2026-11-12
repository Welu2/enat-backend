-- Additive operations schema; no patient records are removed.
grant usage on schema enat_ops to enat_app,enat_worker;
grant select on enat_ops.migrations to enat_app,enat_worker;
do $$ declare r text; begin
 foreach r in array array['anon','authenticated','service_role'] loop
  if exists(select 1 from pg_roles where rolname=r) then
   execute format('revoke all on schema enat_ops from %I',r);
   execute format('revoke all on enat_ops.migrations from %I',r);
  end if;
 end loop;
end $$;
create index checkin_history_cursor on check_ins(user_id,timestamp desc,id desc);
create index reminder_pending_cursor on reminders(user_id,due_at,id) where not dismissed;
create index session_expiry on check_in_sessions(expires_at,id) where status='in_progress';
create index app_session_expiry on app_sessions(expires_at);
create index share_expiry on summary_shares(expires_at);
create index jobs_user on background_jobs(user_id);
create index outbox_user on domain_outbox(user_id);
create index provider_lease_expiry on provider_leases(expires_at);

-- One bounded maintenance batch. Keep clinical records and idempotency evidence;
-- their deletion requires an approved retention policy and a separate audited job.
create or replace function enat_cleanup_security_state() returns void
language plpgsql security definer set search_path=pg_catalog,public as $$ begin
 delete from public.request_limits where bucket in
  (select bucket from public.request_limits where expires_at<now()-interval '1 day' order by expires_at limit 500);
 delete from public.provider_leases where id in
  (select id from public.provider_leases where expires_at<now() order by expires_at limit 500);
 delete from public.app_sessions where token_hash in
  (select token_hash from public.app_sessions where expires_at<now()-interval '1 day' order by expires_at limit 500);
 delete from public.auth_revocations where session_id in
  (select session_id from public.auth_revocations where expires_at<now() order by expires_at limit 500);
 -- Expiry is already enforced at read time; remove unusable bearer credentials.
 delete from public.summary_shares where id in
  (select id from public.summary_shares where expires_at<now()-interval '30 days' order by expires_at limit 500);
 update public.check_in_sessions set status='expired' where id in
  (select id from public.check_in_sessions where status='in_progress' and expires_at<now() order by expires_at,id limit 500);
end $$;
revoke all on function enat_cleanup_security_state() from public;
grant execute on function enat_cleanup_security_state() to enat_worker;
