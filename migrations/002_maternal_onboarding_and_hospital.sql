-- Migration 002: Add maternal onboarding fields, gestational age metrics, and hospital tracking to users table

alter table users
  add column if not exists age int,
  add column if not exists area text, -- 'urban' or 'rural'
  add column if not exists pregnancy_counting_method text, -- 'lnmp', 'ultrasound', 'manual'
  add column if not exists lnmp_date date,
  add column if not exists ultrasound_date date,
  add column if not exists ultrasound_weeks int,
  add column if not exists gestational_age_weeks int,
  add column if not exists gestational_age_days int,
  add column if not exists is_gestational_age_manual boolean default false,
  add column if not exists effective_lnmp_date date,
  add column if not exists estimated_due_date date,
  add column if not exists trimester text, -- 'first_trimester', 'second_trimester', 'third_trimester'
  add column if not exists total_pregnancies int,
  add column if not exists live_births int,
  add column if not exists had_c_section boolean,
  add column if not exists child_passed_away boolean,
  add column if not exists past_pregnancy_complications jsonb default '[]'::jsonb,
  add column if not exists known_medical_conditions jsonb default '[]'::jsonb,
  add column if not exists custom_medical_condition text,
  add column if not exists malaria_endemic_area boolean,
  add column if not exists current_medications text,
  add column if not exists hospital text,
  add column if not exists onboarding_completed boolean default false;
