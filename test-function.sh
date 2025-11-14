#!/bin/bash
# Test Nomago Edge Function

echo "🧪 Testing Nomago Monitor Edge Function"
echo "========================================"
echo ""
echo "Potrebuješ ANON KEY iz Supabase Dashboard:"
echo "1. https://supabase.com/dashboard/project/raavrcsgqeekhjpjxzlt"
echo "2. Settings → API → Project API keys → anon/public"
echo ""
read -p "Vnesi ANON KEY: " ANON_KEY
echo ""
echo "Testing..."
echo ""

curl -s -X POST \
  "https://raavrcsgqeekhjpjxzlt.supabase.co/functions/v1/nomago-monitor" \
  -H "Authorization: Bearer $ANON_KEY" \
  -H "Content-Type: application/json" | python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin), indent=2))"

echo ""
echo "✅ Test complete!"
