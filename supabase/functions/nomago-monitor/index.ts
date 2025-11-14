// Nomago Bike Monitor - Supabase Edge Function
// Monitors Four Points by Sheraton bike station

import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const NOMAGO_API = "https://api.ontime.si/api/v1/nomago-bike/"
const STATION_ID = 458645919 // Four Points by Sheraton

interface NomagoStation {
  station_id: number
  location_name: string
  created_date: string
  lat: number
  lng: number
  available_bikes: number
  available_stands: number
  total_stands: number
}

interface BikeHistory {
  timestamp: string
  available_bikes: number
  available_stands: number
  total_stands: number
  station_id: number
}

serve(async (req) => {
  try {
    console.log("🚲 Nomago Monitor - Starting...")

    // Fetch data from Nomago API
    const response = await fetch(NOMAGO_API)
    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`)
    }

    const data = await response.json()
    const stations: NomagoStation[] = data.results || []

    // Find Four Points station
    const station = stations.find(s => s.station_id === STATION_ID)

    if (!station) {
      throw new Error(`Station ${STATION_ID} not found`)
    }

    console.log(`📊 Found station: ${station.location_name}`)
    console.log(`🚲 Bikes: ${station.available_bikes}/${station.total_stands}`)

    // Initialize Supabase client
    const supabaseUrl = Deno.env.get('SUPABASE_URL')!
    const supabaseKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
    const supabase = createClient(supabaseUrl, supabaseKey)

    // Prepare data
    const historyData: BikeHistory = {
      timestamp: new Date().toISOString(),
      available_bikes: station.available_bikes,
      available_stands: station.available_stands,
      total_stands: station.total_stands,
      station_id: station.station_id
    }

    // Insert into database
    const { data: inserted, error } = await supabase
      .from('bike_history')
      .insert(historyData)
      .select()

    if (error) {
      throw error
    }

    console.log(`✅ Saved to database: ${station.available_bikes}/${station.total_stands} bikes`)

    return new Response(
      JSON.stringify({
        success: true,
        station: station.location_name,
        bikes: station.available_bikes,
        stands: station.available_stands,
        total: station.total_stands,
        timestamp: historyData.timestamp,
        saved: inserted
      }),
      {
        headers: { "Content-Type": "application/json" },
        status: 200,
      },
    )

  } catch (error) {
    console.error("❌ Error:", error)

    return new Response(
      JSON.stringify({
        success: false,
        error: error.message
      }),
      {
        headers: { "Content-Type": "application/json" },
        status: 500,
      },
    )
  }
})
