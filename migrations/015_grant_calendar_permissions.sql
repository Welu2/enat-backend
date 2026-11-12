-- Migration 015: Grant calendar_items permissions to service_role and authenticated
GRANT ALL ON public.calendar_items TO service_role;
GRANT ALL ON public.calendar_items TO authenticated;
