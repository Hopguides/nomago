#!/bin/bash
# Final Nomago Test - After table creation

export SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJhYXZyY3NncWVla2hqcGp4emx0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU1OTUyMzMsImV4cCI6MjA3MTE3MTIzM30.bgYTTOJIdeNSBTeA0KAluic328VzHCMzqlmqk9qw_UQ"

echo "🚲 NOMAGO FINAL TEST"
echo "======================================================================"

# Test 1: Database
echo ""
echo "TEST 1: Database Table"
python3 test-database.py
echo ""

# Test 2: Edge Function
echo "======================================================================"
echo "TEST 2: Edge Function (Invoke & Save)"
python3 test-edge-function.py
echo ""

# Test 3: Verify data saved
echo "======================================================================"
echo "TEST 3: Verify Data Saved"
sleep 2
curl -s \
  "https://raavrcsgqeekhjpjxzlt.supabase.co/rest/v1/bike_history?select=*&order=timestamp.desc&limit=1" \
  -H "apikey: $SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $SUPABASE_ANON_KEY" | python3 -m json.tool

echo ""
echo "======================================================================"
echo "✅ ALL TESTS COMPLETE!"
echo "======================================================================"
