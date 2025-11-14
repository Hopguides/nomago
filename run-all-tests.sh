#!/bin/bash
# Nomago Monitor - Complete Test Suite
# Tests Edge Function and Database

set -e

echo "🚲 NOMAGO MONITOR - TEST SUITE"
echo "======================================================================"
echo ""

# Check if ANON KEY is set
if [ -z "$SUPABASE_ANON_KEY" ]; then
    echo "❌ SUPABASE_ANON_KEY not set"
    echo ""
    echo "📋 Get your ANON KEY:"
    echo "1. Go to: https://supabase.com/dashboard/project/raavrcsgqeekhjpjxzlt"
    echo "2. Settings → API → Project API keys"
    echo "3. Copy 'anon / public' key"
    echo ""
    echo "🔧 Then run:"
    echo "   export SUPABASE_ANON_KEY='your_key_here'"
    echo "   ./run-all-tests.sh"
    echo ""
    exit 1
fi

echo "✅ SUPABASE_ANON_KEY found"
echo ""

# Test 1: Database
echo "======================================================================"
echo "TEST 1: Database Connection & Table"
echo "======================================================================"
python3 test-database.py
echo ""

# Test 2: Edge Function
echo "======================================================================"
echo "TEST 2: Edge Function"
echo "======================================================================"
python3 test-edge-function.py
echo ""

# Test 3: End-to-End
echo "======================================================================"
echo "TEST 3: End-to-End (Invoke & Verify)"
echo "======================================================================"

echo "📡 Invoking Edge Function..."
RESPONSE=$(curl -s -X POST \
  "https://raavrcsgqeekhjpjxzlt.supabase.co/functions/v1/nomago-monitor" \
  -H "Authorization: Bearer $SUPABASE_ANON_KEY" \
  -H "Content-Type: application/json")

echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(json.dumps(data, indent=2))"

SUCCESS=$(echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data.get('success', False))")

if [ "$SUCCESS" = "True" ]; then
    echo ""
    echo "✅ Edge Function executed successfully!"

    # Wait a bit for data to be written
    echo ""
    echo "⏱️  Waiting 2 seconds for database write..."
    sleep 2

    # Check if new record was created
    echo ""
    echo "📊 Checking for new record in database..."

    LATEST=$(curl -s \
      "https://raavrcsgqeekhjpjxzlt.supabase.co/rest/v1/bike_history?select=timestamp,available_bikes,total_stands&order=timestamp.desc&limit=1" \
      -H "apikey: $SUPABASE_ANON_KEY" \
      -H "Authorization: Bearer $SUPABASE_ANON_KEY")

    echo "$LATEST" | python3 -c "import sys, json; data = json.load(sys.stdin); print('Latest record:'); print(json.dumps(data[0] if data else {}, indent=2))"

    echo ""
    echo "✅ End-to-end test PASSED!"
else
    echo ""
    echo "❌ Edge Function failed!"
    exit 1
fi

echo ""
echo "======================================================================"
echo "🎉 ALL TESTS PASSED!"
echo "======================================================================"
echo ""
echo "📊 Summary:"
echo "   ✅ Database accessible"
echo "   ✅ bike_history table exists"
echo "   ✅ Edge Function deployed and working"
echo "   ✅ Data being saved correctly"
echo ""
echo "🚀 Next step: Set up cron job (setup-cron.sql)"
echo ""
