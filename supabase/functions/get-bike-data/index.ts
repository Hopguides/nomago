// Get Bike Data - Public API Endpoint
// Returns bike history data in JSON format

import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const url = new URL(req.url)
    const limit = parseInt(url.searchParams.get('limit') || '100')
    const offset = parseInt(url.searchParams.get('offset') || '0')
    const since = url.searchParams.get('since') // ISO timestamp

    // Initialize Supabase client
    const supabaseUrl = Deno.env.get('SUPABASE_URL')!
    const supabaseKey = Deno.env.get('SUPABASE_ANON_KEY')!
    const supabase = createClient(supabaseUrl, supabaseKey)

    // Build query
    let query = supabase
      .from('bike_history')
      .select('*')
      .order('timestamp', { ascending: false })
      .limit(limit)
      .range(offset, offset + limit - 1)

    // Filter by date if provided
    if (since) {
      query = query.gte('timestamp', since)
    }

    const { data, error, count } = await query

    if (error) throw error

    // Get statistics
    const { data: stats } = await supabase
      .from('bike_history')
      .select('available_bikes, available_stands, total_stands')
      .order('timestamp', { ascending: false })
      .limit(1)
      .single()

    const current = stats || { available_bikes: 0, available_stands: 0, total_stands: 2 }

    return new Response(
      JSON.stringify({
        success: true,
        station: {
          id: 458645919,
          name: "Four Points by Sheraton Ljubljana Mons",
          location: {
            lat: 46.052252,
            lng: 14.45303
          }
        },
        current: {
          bikes: current.available_bikes,
          stands: current.available_stands,
          total: current.total_stands,
          status: current.available_bikes === 0 ? 'empty' :
                  current.available_stands === 0 ? 'full' : 'available'
        },
        data: data,
        pagination: {
          limit: limit,
          offset: offset,
          total: count || data?.length || 0
        },
        timestamp: new Date().toISOString()
      }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 200,
      },
    )

  } catch (error) {
    console.error('Error:', error)

    return new Response(
      JSON.stringify({
        success: false,
        error: error.message
      }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 500,
      },
    )
  }
})
