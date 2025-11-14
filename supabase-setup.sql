-- Nomago Bike History Table for Supabase
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

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_bike_history_timestamp ON bike_history(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_bike_history_station ON bike_history(station_id);

-- Enable Row Level Security (optional - for production)
ALTER TABLE bike_history ENABLE ROW LEVEL SECURITY;

-- Allow anon/authenticated users to read
CREATE POLICY "Allow public read access"
    ON bike_history
    FOR SELECT
    TO anon, authenticated
    USING (true);

-- Allow service role to insert (for Edge Function)
CREATE POLICY "Allow service role insert"
    ON bike_history
    FOR INSERT
    TO service_role
    WITH CHECK (true);

-- Verify table
SELECT * FROM bike_history LIMIT 5;
