-- Migration 014: Add name column to users table
alter table users add column if not exists name text;
