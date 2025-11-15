#!/bin/bash
# Test Public API Endpoint

ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJhYXZyY3NncWVla2hqcGp4emx0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU1OTUyMzMsImV4cCI6MjA3MTE3MTIzM30.bgYTTOJIdeNSBTeA0KAluic328VzHCMzqlmqk9qw_UQ"
API_URL="https://raavrcsgqeekhjpjxzlt.supabase.co/functions/v1/get-bike-data"

echo "🧪 Testing Public API Endpoint"
echo "======================================================================"

# Test 1: Basic request
echo ""
echo "TEST 1: Basic Request (latest 5 records)"
echo "----------------------------------------------------------------------"
curl -s "${API_URL}?limit=5" \
  -H "Authorization: Bearer ${ANON_KEY}" | python3 -m json.tool

# Test 2: Current status only
echo ""
echo "======================================================================"
echo "TEST 2: Current Status Only"
echo "----------------------------------------------------------------------"
curl -s "${API_URL}?limit=1" \
  -H "Authorization: Bearer ${ANON_KEY}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('success'):
    current = data['current']
    print(f\"✅ Station: {data['station']['name']}\")
    print(f\"   Bikes: {current['bikes']}/{current['total']}\")
    print(f\"   Stands: {current['stands']}/{current['total']}\")
    print(f\"   Status: {current['status'].upper()}\")
else:
    print('❌ Error:', data.get('error'))
"

# Test 3: Without auth (should fail)
echo ""
echo "======================================================================"
echo "TEST 3: Without Authentication (should fail)"
echo "----------------------------------------------------------------------"
curl -s "${API_URL}?limit=1" | python3 -m json.tool

echo ""
echo "======================================================================"
echo "✅ Public API Tests Complete"
echo "======================================================================"
echo ""
echo "📖 Full documentation: API_DOCUMENTATION.md"
echo "🌐 Endpoint: ${API_URL}"
echo ""
