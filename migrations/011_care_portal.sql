-- Patient-approved access. Existing patient-table RLS remains unchanged.
create table clinician_profiles (
 user_id uuid primary key references users(id), display_name text not null check(length(display_name) between 1 and 200),
 active boolean not null default true, created_at timestamptz not null default now(), updated_at timestamptz not null default now()
);
create table care_connections (
 id uuid primary key default gen_random_uuid(), patient_id uuid not null references users(id),
 recipient_id uuid not null references users(id), relationship text not null check(relationship in ('clinician','trusted_person')),
 status text not null default 'pending' check(status in ('pending','active','revoked','expired')),
 consent_version text not null default 'care-v1', consented_at timestamptz not null default now(),
 created_at timestamptz not null default now(), accepted_at timestamptz, revoked_at timestamptz,
 expires_at timestamptz not null default now()+interval '48 hours',
 invite_token_hash text not null unique check(invite_token_hash ~ '^[0-9a-f]{64}$'),
 check(patient_id<>recipient_id), check(expires_at>created_at),
 check(status<>'active' or accepted_at is not null), check((status='revoked')=(revoked_at is not null))
);
create unique index care_trusted_slot on care_connections(patient_id) where relationship='trusted_person' and status in ('pending','active');
create unique index care_connection_slot on care_connections(patient_id,recipient_id,relationship) where status in ('pending','active');
create index care_recipient on care_connections(recipient_id,patient_id) where status='active';
create index care_owner on care_connections(patient_id,id);
alter table check_ins add constraint checkin_id_owner unique(id,user_id);
create table emergency_alerts (
 id uuid primary key default gen_random_uuid(), patient_id uuid not null references users(id),
 check_in_id uuid not null unique, categories text[] not null check(cardinality(categories)>0),
 recorded_at timestamptz not null, received_at timestamptz not null, created_at timestamptz not null default now(),
 policy_version text not null, status text not null default 'unacknowledged' check(status in ('unacknowledged','acknowledged')),
 acknowledged_at timestamptz, acknowledged_by uuid references users(id),
 foreign key(check_in_id,patient_id) references check_ins(id,user_id),
 check((status='acknowledged')=(acknowledged_at is not null)),
 check((status='acknowledged')=(acknowledged_by is not null))
);
create index alert_patient_time on emergency_alerts(patient_id,created_at desc,id desc);
create table care_access_events (
 id uuid primary key default gen_random_uuid(), patient_id uuid not null references users(id),
 actor_id uuid not null references users(id), connection_id uuid references care_connections(id),
 action text not null check(action in ('invited','accepted','revoked','expired','read','acknowledged')),
 resource text not null check(resource in ('connection','patients','patient','check_ins','summary','appointment','alerts')),
 resource_id uuid, row_count integer check(row_count between 0 and 100), occurred_at timestamptz not null default now()
);
create index care_audit_owner on care_access_events(patient_id,id);
create trigger care_audit_immutable before update or delete on care_access_events
 for each row execute function enat_privacy_audit_immutable();
alter table clinician_profiles enable row level security;
alter table care_connections enable row level security;
alter table emergency_alerts enable row level security;
alter table care_access_events enable row level security;
revoke all on clinician_profiles,care_connections,emergency_alerts,care_access_events from public;
grant select on care_connections,emergency_alerts,care_access_events to enat_app;
grant insert on emergency_alerts to enat_app;
create policy care_owner on care_connections to enat_app using(patient_id=enat_user_id());
create policy alert_owner on emergency_alerts to enat_app using(patient_id=enat_user_id()) with check(patient_id=enat_user_id() and status='unacknowledged');
create policy care_audit_owner on care_access_events to enat_app using(patient_id=enat_user_id());
do $$ begin
 if not exists(select 1 from pg_roles where rolname='enat_care_operator') then
  create role enat_care_operator nologin nosuperuser nobypassrls;
 end if;
end $$;
grant usage on schema public to enat_care_operator;
grant select,insert,update on clinician_profiles to enat_care_operator;
create policy clinician_operator on clinician_profiles to enat_care_operator using(true) with check(true);

-- Internal helpers are never executable by the application or client roles.
create function _enat_care_metadata(c care_connections) returns jsonb language sql stable
set search_path=pg_catalog,public as $$
 select jsonb_build_object('id',c.id,'recipient_id',c.recipient_id,'relationship',c.relationship,
 'status',case when c.status='pending' and c.expires_at<=now() then 'expired' else c.status end,
 'consent_version',c.consent_version,'consented_at',c.consented_at,'created_at',c.created_at,
 'accepted_at',c.accepted_at,'revoked_at',c.revoked_at,'expires_at',c.expires_at,
 'recipient_display_name',coalesce((select display_name from public.clinician_profiles where user_id=c.recipient_id and c.relationship='clinician'),(select first_name from public.users where id=c.recipient_id),'Account'))
$$;
create function _enat_care_connection(p_patient uuid,p_clinical boolean default false) returns care_connections
language sql stable security definer set search_path=pg_catalog,public as $$
 select c from public.care_connections c
 join public.users p on p.id=c.patient_id and p.disabled_at is null
 where c.patient_id=p_patient and c.recipient_id=public.enat_user_id() and c.status='active'
 and (c.relationship<>'clinician' or exists(select 1 from public.clinician_profiles cp where cp.user_id=c.recipient_id and cp.active))
 and (not p_clinical or c.relationship='clinician')
 order by (c.relationship='clinician') desc,c.id limit 1
$$;
create function _enat_care_audit(p_patient uuid,p_connection uuid,p_action text,p_resource text,p_id uuid,p_count integer default null)
returns void language sql security definer set search_path=pg_catalog,public as $$
 insert into public.care_access_events(patient_id,actor_id,connection_id,action,resource,resource_id,row_count)
 values(p_patient,public.enat_user_id(),p_connection,p_action,p_resource,p_id,p_count)
$$;

create function enat_care_invite(p_recipient uuid,p_relationship text,p_hash text) returns jsonb
language plpgsql security definer set search_path=pg_catalog,public as $$
declare uid uuid:=public.enat_user_id(); c public.care_connections;
begin
 if uid is null or uid=p_recipient or p_relationship not in ('clinician','trusted_person')
 or not exists(select 1 from public.users where id=p_recipient and disabled_at is null)
 or (p_relationship='clinician' and not exists(select 1 from public.clinician_profiles where user_id=p_recipient and active)) then return null; end if;
 perform pg_advisory_xact_lock(hashtextextended('care:'||uid::text,0));
 for c in update public.care_connections set status='expired' where patient_id=uid and status='pending' and expires_at<=now() returning * loop
  perform public._enat_care_audit(uid,c.id,'expired','connection',c.id);
 end loop;
 if exists(select 1 from public.care_connections where patient_id=uid and status in ('pending','active')
 and relationship=p_relationship and (recipient_id=p_recipient or p_relationship='trusted_person')) then return '{"conflict":true}'::jsonb; end if;
 insert into public.care_connections(patient_id,recipient_id,relationship,invite_token_hash) values(uid,p_recipient,p_relationship,p_hash) returning * into c;
 perform public._enat_care_audit(uid,c.id,'invited','connection',c.id);
 return public._enat_care_metadata(c);
end $$;
create function enat_care_connections(p_limit integer,p_after uuid default null) returns jsonb
language plpgsql security definer set search_path=pg_catalog,public as $$
declare uid uuid:=public.enat_user_id(); result jsonb;
begin
 if uid is null or p_limit is null or p_limit not between 1 and 100 then return null; end if;
 select coalesce(jsonb_agg(public._enat_care_metadata(c) order by c.id),'[]'::jsonb) into result
 from (select * from public.care_connections where patient_id=uid and (p_after is null or id>p_after) order by id limit p_limit+1) c;
 return result;
end $$;
create function enat_care_accept(p_hash text) returns jsonb
language plpgsql security definer set search_path=pg_catalog,public as $$
declare uid uuid:=public.enat_user_id(); c public.care_connections;
begin
 if uid is null then return null; end if;
 select * into c from public.care_connections where invite_token_hash=p_hash and recipient_id=uid for update;
 if c.id is null or c.status not in ('pending','active')
 or not exists(select 1 from public.users where id=c.patient_id and disabled_at is null)
 or (c.relationship='clinician' and not exists(select 1 from public.clinician_profiles where user_id=uid and active)) then return null; end if;
 if c.status='pending' and c.expires_at<=now() then
  update public.care_connections set status='expired' where id=c.id;
  perform public._enat_care_audit(c.patient_id,c.id,'expired','connection',c.id);
  return null;
 end if;
 if c.status='pending' then
  update public.care_connections set status='active',accepted_at=now() where id=c.id returning * into c;
  perform public._enat_care_audit(c.patient_id,c.id,'accepted','connection',c.id);
 end if;
 return jsonb_build_object('id',c.id,'relationship',c.relationship,'status',c.status);
end $$;
create function enat_care_revoke(p_id uuid) returns boolean
language plpgsql security definer set search_path=pg_catalog,public as $$
declare uid uuid:=public.enat_user_id(); c public.care_connections;
begin
 select * into c from public.care_connections where id=p_id and patient_id=uid for update;
 if c.id is null then return false; end if;
 if c.status<>'revoked' then
  update public.care_connections set status='revoked',revoked_at=now() where id=c.id;
  perform public._enat_care_audit(uid,c.id,'revoked','connection',c.id);
 end if;
 return true;
end $$;
create function enat_portal_me() returns jsonb language sql security definer set search_path=pg_catalog,public as $$
 select jsonb_build_object('id',u.id,'display_name',coalesce((select display_name from public.clinician_profiles where user_id=u.id and active),u.first_name,'Account'),
 'is_clinician',exists(select 1 from public.clinician_profiles where user_id=u.id and active))
 from public.users u where u.id=public.enat_user_id()
$$;
create function _enat_portal_appointment(p_patient uuid) returns jsonb language sql stable
security definer set search_path=pg_catalog,public as $$
 select jsonb_build_object('appointment_date',a.appointment_date,'hospital',u.hospital,
 'anc_contact_title',a.anc_contact_title,'anc_contact_title_am',a.anc_contact_title_am,'status',a.status,'version',a.version)
 from public.appointments a join public.users u on u.id=a.user_id
 where a.user_id=p_patient and a.status='scheduled' and a.appointment_date>=(now() at time zone 'Africa/Addis_Ababa')::date
$$;
create function enat_portal_patients(p_limit integer,p_after uuid default null) returns jsonb
language plpgsql security definer set search_path=pg_catalog,public as $$
declare c public.care_connections; p record; result jsonb:='[]'::jsonb; n integer:=0;
begin
 if public.enat_user_id() is null or p_limit is null or p_limit not between 1 and 100 then return null; end if;
 for p in select distinct patient_id from public.care_connections
 where recipient_id=public.enat_user_id() and status='active' and (p_after is null or patient_id>p_after)
 and (public._enat_care_connection(patient_id)).id is not null order by patient_id limit p_limit+1 loop
  c:=public._enat_care_connection(p.patient_id);
  result:=result||jsonb_build_array(jsonb_build_object('id',c.patient_id,
   'display_name',coalesce((select first_name from public.users where id=c.patient_id),'Patient'),
   'relationship',c.relationship,'appointment',public._enat_portal_appointment(c.patient_id),
   'unacknowledged_alert_count',(select count(*) from public.emergency_alerts where patient_id=c.patient_id and status='unacknowledged' and (c.relationship='clinician' or created_at>=c.accepted_at))));
  n:=n+1;
  if n<=p_limit then perform public._enat_care_audit(c.patient_id,c.id,'read','patients',c.patient_id,1); end if;
 end loop;
 return result;
end $$;

-- Static projections: no dynamic table names, arbitrary fields, or actor parameters.
create function enat_portal_read(p_patient uuid,p_resource text,p_limit integer default 50,p_stamp timestamptz default null,p_id uuid default null,p_status text default null)
returns jsonb language plpgsql security definer set search_path=pg_catalog,public as $$
declare c public.care_connections; result jsonb; n integer:=1;
begin
 if p_resource is null or p_resource not in ('patient','check_ins','summary','appointment','alerts')
 or p_limit is null or p_limit not between 1 and 100 or (p_stamp is null)<>(p_id is null)
 or (p_status is not null and p_status not in ('unacknowledged','acknowledged')) then return null; end if;
 c:=public._enat_care_connection(p_patient,p_resource in ('patient','check_ins','summary'));
 if c.id is null then return null; end if;
 if p_resource='patient' then
  select jsonb_build_object('id',u.id,'display_name',coalesce(u.first_name,'Patient'),'hospital',u.hospital,
   'estimated_due_date',u.estimated_due_date,'gestational_age_weeks',u.gestational_age_weeks,
   'gestational_age_days',u.gestational_age_days,'pregnancy_as_of',null,'overview_retrieved_at',now(),
   'latest_check_in_received_at',(select max(timestamp) from public.check_ins where user_id=u.id)) into result from public.users u where u.id=p_patient;
 elsif p_resource='appointment' then result:=public._enat_portal_appointment(p_patient);
 elsif p_resource='summary' then
  select jsonb_build_object('id',s.id,'period_start',s.period_start,'period_end',s.period_end,
   'generated_at',s.generated_at,'content_json',s.content_json) into result
  from public.summaries s where s.user_id=p_patient order by s.generated_at desc,s.id desc limit 1;
 elsif p_resource='check_ins' then
  select coalesce(jsonb_agg(jsonb_build_object('id',r.id,'timestamp',r.timestamp,
   'recorded_at',coalesce(to_jsonb(r)->'recorded_at',to_jsonb(r)->'timestamp'),
   'received_at',coalesce(to_jsonb(r)->'received_at',to_jsonb(r)->'timestamp'),
   'client_confirmed_at',to_jsonb(r)->'client_confirmed_at','capture_source',coalesce(to_jsonb(r)->>'capture_source','online'),
   'symptoms',r.symptoms,'food_log',r.food_log,'supplement_check',r.supplement_check,
   'closing_mentions',r.closing_mentions,'danger_sign_triggered',r.danger_sign_triggered,
   'summary_text_am',r.summary_text_am,'summary_text_en',r.summary_text_en) order by r.timestamp desc,r.id desc),'[]'::jsonb) into result
  from (select * from public.check_ins ci where ci.user_id=p_patient and (p_stamp is null or (ci.timestamp,ci.id)<(p_stamp,p_id))
   and not exists(select 1 from jsonb_array_elements(ci.symptoms||ci.food_log||ci.supplement_check||ci.closing_mentions) i where i->'confirmed' is distinct from 'true'::jsonb)
   order by ci.timestamp desc,ci.id desc limit p_limit+1) r;
  n:=least(jsonb_array_length(result),p_limit);
 else
  select coalesce(jsonb_agg(jsonb_build_object('id',a.id,'categories',a.categories,'recorded_at',a.recorded_at,
   'received_at',a.received_at,'created_at',a.created_at,'status',a.status,'acknowledged_at',a.acknowledged_at)
   order by a.created_at desc,a.id desc),'[]'::jsonb) into result
  from (select * from public.emergency_alerts where patient_id=p_patient
   and (c.relationship='clinician' or created_at>=c.accepted_at)
   and (p_status is null or status=p_status) and (p_stamp is null or (created_at,id)<(p_stamp,p_id))
   order by created_at desc,id desc limit p_limit+1) a;
  n:=least(jsonb_array_length(result),p_limit);
 end if;
 perform public._enat_care_audit(p_patient,c.id,'read',p_resource,p_patient,case when result is null then 0 else n end);
 return jsonb_build_object('data',result);
end $$;
create function enat_portal_acknowledge(p_patient uuid,p_alert uuid) returns jsonb
language plpgsql security definer set search_path=pg_catalog,public as $$
declare c public.care_connections; a public.emergency_alerts;
begin
 c:=public._enat_care_connection(p_patient,true);
 if c.id is null then return null; end if;
 select * into a from public.emergency_alerts where id=p_alert and patient_id=p_patient for update;
 if a.id is null then return null; end if;
 if a.status='unacknowledged' then
  update public.emergency_alerts set status='acknowledged',acknowledged_at=now(),acknowledged_by=public.enat_user_id()
   where id=a.id returning * into a;
  perform public._enat_care_audit(p_patient,c.id,'acknowledged','alerts',a.id);
 end if;
 return jsonb_build_object('id',a.id,'categories',a.categories,'recorded_at',a.recorded_at,'received_at',a.received_at,
 'created_at',a.created_at,'status',a.status,'acknowledged_at',a.acknowledged_at);
end $$;

alter table privacy_events drop constraint privacy_events_resource_check;
alter table privacy_events add constraint privacy_events_resource_check check(resource in
 ('profile','supplements','appointments','appointment_events','check_ins','drafts','summaries','reminders','shares','requests','audit','care_connections','emergency_alerts','care_audit'));
do $$ declare f regprocedure; r text; t text; begin
 for f in select oid::regprocedure from pg_proc where pronamespace='public'::regnamespace
 and (proname like 'enat_care_%' or proname like 'enat_portal_%' or proname like '\_enat\_care\_%' or proname like '\_enat\_portal\_%') loop
  execute format('revoke all on function %s from public,enat_app,enat_worker',f);
  foreach r in array array['anon','authenticated','service_role'] loop
   if exists(select 1 from pg_roles where rolname=r) then execute format('revoke all on function %s from %I',f,r); end if;
  end loop;
 end loop;
 foreach t in array array['clinician_profiles','care_connections','emergency_alerts','care_access_events'] loop
  foreach r in array array['anon','authenticated','service_role'] loop
   if exists(select 1 from pg_roles where rolname=r) then execute format('revoke all on %I from %I',t,r); end if;
  end loop;
 end loop;
end $$;
grant execute on function enat_care_invite(uuid,text,text),enat_care_connections(integer,uuid),enat_care_accept(text),enat_care_revoke(uuid),
 enat_portal_me(),enat_portal_patients(integer,uuid),enat_portal_read(uuid,text,integer,timestamptz,uuid,text),enat_portal_acknowledge(uuid,uuid) to enat_app;
