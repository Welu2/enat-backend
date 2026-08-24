-- Migration 003: Add ANC contact scheduling fields and check-in summary text

alter table check_ins
  add column if not exists summary_text_am text,
  add column if not exists summary_text_en text;

alter table appointments
  add column if not exists anc_contact_number int default 1,
  add column if not exists anc_contact_title text,
  add column if not exists anc_contact_title_am text,
  add column if not exists target_gestational_weeks int,
  add column if not exists previous_appointment_date date;

alter table summaries
  add column if not exists anc_contact_number int,
  add column if not exists anc_contact_title text,
  add column if not exists anc_contact_title_am text,
  add column if not exists target_gestational_weeks int;
