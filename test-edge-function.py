#!/usr/bin/env python3
"""
Test Nomago Edge Function
Tests the deployed Supabase Edge Function
"""

import requests
import json
import sys

# Configuration
FUNCTION_URL = "https://raavrcsgqeekhjpjxzlt.supabase.co/functions/v1/nomago-monitor"

def test_function_with_service_role():
    """Test with service role key (bypass auth)"""
    print("🧪 Testing Nomago Edge Function")
    print("=" * 60)

    # Note: Service role key should be in environment or dashboard
    # For security, we'll test without auth first to see the error
    print("\n1️⃣ Testing without auth (should fail):")

    try:
        response = requests.post(FUNCTION_URL, timeout=30)
        print(f"   Status: {response.status_code}")

        if response.status_code == 401:
            print("   ✅ Auth required (expected)")

        try:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
        except:
            print(f"   Response: {response.text}")

    except Exception as e:
        print(f"   ❌ Error: {e}")

    print("\n" + "=" * 60)
    print("\n📋 Next Steps:")
    print("1. Get ANON KEY from Supabase Dashboard:")
    print("   Settings → API → Project API keys → anon/public")
    print("\n2. Test with key:")
    print(f"   curl -X POST '{FUNCTION_URL}' \\")
    print("     -H 'Authorization: Bearer YOUR_ANON_KEY'")
    print("\n3. Or run this script with key:")
    print("   SUPABASE_ANON_KEY=your_key python3 test-edge-function.py")

if __name__ == "__main__":
    import os

    anon_key = os.environ.get('SUPABASE_ANON_KEY')

    if anon_key:
        print("🔑 Using SUPABASE_ANON_KEY from environment")
        print("=" * 60)

        try:
            response = requests.post(
                FUNCTION_URL,
                headers={
                    'Authorization': f'Bearer {anon_key}',
                    'Content-Type': 'application/json'
                },
                timeout=30
            )

            print(f"\n📊 Status: {response.status_code}")

            try:
                data = response.json()
                print(f"\n✅ Response:")
                print(json.dumps(data, indent=2))

                if data.get('success'):
                    print(f"\n🎉 SUCCESS!")
                    print(f"   Station: {data.get('station')}")
                    print(f"   Bikes: {data.get('bikes')}/{data.get('total')}")
                    print(f"   Timestamp: {data.get('timestamp')}")
                else:
                    print(f"\n❌ Function returned error:")
                    print(f"   {data.get('error')}")

            except Exception as e:
                print(f"\n❌ JSON parse error: {e}")
                print(f"   Raw response: {response.text}")

        except Exception as e:
            print(f"\n❌ Request error: {e}")
    else:
        test_function_with_service_role()
