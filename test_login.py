#!/usr/bin/env python3
"""
Test login functionality
"""

import requests
import json


def test_login():
    """Test user login"""
    url = "http://localhost:8000/auth/token"

    # Login data (form-encoded for OAuth2)
    login_data = {
        "username": "john.doe@example.com",  # OAuth2 uses 'username' field for email
        "password": "supersecret123"
    }

    print("🔐 Testing user login...")
    print(f"📤 Sending POST to: {url}")
    print(f"📋 Credentials: {login_data['username']} / {'*' * len(login_data['password'])}")

    try:
        # OAuth2 expects form data, not JSON
        response = requests.post(url, data=login_data)

        print(f"\n📊 Response Status: {response.status_code}")

        if response.status_code == 200:
            response_json = response.json()
            print(f"📃 Response: {json.dumps(response_json, indent=2)}")

            access_token = response_json.get('access_token')
            if access_token:
                print("✅ Login successful!")
                print(f"🔑 Access token: {access_token[:30]}...")
                return access_token
            else:
                print("❌ No access token in response")
                return None

        else:
            print(f"❌ Login failed with status {response.status_code}")
            try:
                error_response = response.json()
                print(f"📃 Error: {json.dumps(error_response, indent=2)}")
            except:
                print(f"📃 Error (raw): {response.text}")
            return None

    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return None


def test_protected_endpoint(access_token):
    """Test accessing a protected endpoint"""
    url = "http://localhost:8000/auth/me"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    print(f"\n🔒 Testing protected endpoint: {url}")

    try:
        response = requests.get(url, headers=headers)

        print(f"📊 Response Status: {response.status_code}")

        if response.status_code == 200:
            user_info = response.json()
            print(f"📃 User Info: {json.dumps(user_info, indent=2)}")
            print("✅ Protected endpoint access successful!")
            return True
        else:
            print(f"❌ Protected endpoint failed with status {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Protected endpoint error: {str(e)}")
        return False


if __name__ == "__main__":
    print("🚀 Testing login functionality...\n")

    # Test login
    token = test_login()

    if token:
        # Test protected endpoint
        test_protected_endpoint(token)
        print("\n🎉 All authentication tests passed!")
    else:
        print("\n❌ Login failed, cannot test protected endpoints")
        print("\nTroubleshooting:")
        print("1. Make sure the user 'john.doe@example.com' exists (run test_registration.py first)")
        print("2. Check that the password is correct: 'supersecret123'")
        print("3. Verify your JWT_SECRET is set in .env")