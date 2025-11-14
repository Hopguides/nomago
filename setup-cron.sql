-- Nomago Monitor - Avtomatski Cron Job
-- Izvede funkcijo vsakih 10 minut

-- KORAK 1: Omogoči pg_cron extension (če še ni)
CREATE EXTENSION IF NOT EXISTS pg_cron;

-- KORAK 2: Omogoči pg_net extension (za HTTP requests)
CREATE EXTENSION IF NOT EXISTS pg_net;

-- KORAK 3: Ustvari cron job
-- POMEMBNO: Zamenjaj 'YOUR_ANON_KEY' s pravim ANON KEY iz:
-- Settings → API → Project API keys → anon/public

SELECT cron.schedule(
    'nomago-monitor-job',           -- Ime job-a
    '*/10 * * * *',                 -- Vsakih 10 minut
    $$
    SELECT net.http_post(
        url:='https://raavrcsgqeekhjpjxzlt.supabase.co/functions/v1/nomago-monitor',
        headers:=jsonb_build_object(
            'Content-Type', 'application/json',
            'Authorization', 'Bearer YOUR_ANON_KEY'
        )
    ) as request_id;
    $$
);

-- KORAK 4: Preveri da je cron job ustvarjen
SELECT * FROM cron.job;

-- KORAK 5 (Opcijsko): Poglej zgodovino izvajanj
SELECT * FROM cron.job_run_details
WHERE jobname = 'nomago-monitor-job'
ORDER BY start_time DESC
LIMIT 10;

-- Če želiš izbrisati cron job:
-- SELECT cron.unschedule('nomago-monitor-job');
