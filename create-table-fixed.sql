-- Nomago Bike History Table - Fixed for Supabase
-- Run this in Supabase SQL Editor

CREATE TABLE IF NOT EXISTS bike_history (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    available_bikes INTEGER NOT NULL,
    available_stands INTEGER NOT NULL,
    total_stands INTEGER NOT NULL,
    station_id BIGINT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_bike_history_timestamp ON bike_history(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_bike_history_station ON bike_history(station_id);

-- Enable Row Level Security
ALTER TABLE bike_history ENABLE ROW LEVEL SECURITY;

-- Drop policies if they exist (to avoid errors)
DROP POLICY IF EXISTS "Allow public read access" ON bike_history;
DROP POLICY IF EXISTS "Allow service role insert" ON bike_history;

-- Create policies
CREATE POLICY "Allow public read access"
    ON bike_history
    FOR SELECT
    TO anon, authenticated
    USING (true);

CREATE POLICY "Allow service role insert"
    ON bike_history
    FOR INSERT
    TO service_role
    WITH CHECK (true);
