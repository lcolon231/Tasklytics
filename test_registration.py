#!/usr/bin/env python3
"""
Test script to debug registration endpoint
"""

import requests
import json


def test_registration():
    url = "http://localhost:8000/auth/register"

    # Test data
    test_user = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "supersecret123",
        "age": 30
    }

    print("🧪 Testing user registration...")
    print(f"📤 Sending POST to: {url}")
    print(f"📋 Data: {json.dumps(test_user, indent=2)}")

    try:
        response = requests.post(url, json=test_user)

        print(f"\n📊 Response Status: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")

        try:
            response_json = response.json()
            print(f"📃 Response Body: {json.dumps(response_json, indent=2)}")
        except:
            print(f"📃 Response Body (raw): {response.text}")

        if response.status_code == 201:
            print("✅ Registration successful!")
        elif response.status_code == 400:
            print("❌ Registration failed - Bad Request (400)")
            print("This could be:")
            print("  - Validation error in request data")
            print("  - Email already exists")
            print("  - Missing required fields")
        else:
            print(f"❌ Registration failed with status {response.status_code}")

        return response.status_code, response_json if 'response_json' in locals() else response.text

    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Is it running on localhost:8000?")
        return None, "Connection error"
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return None, str(e)


def test_health():
    """Test health endpoint first"""
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"🏥 Health check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except:
        print("❌ Health check failed - server not running?")
        return False


def test_existing_user():
    """Test with a user that might already exist"""
    url = "http://localhost:8000/auth/register"

    # Different test data
    test_user = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "password": "anothersecret456",
        "age": 25
    }

    print(f"\n🧪 Testing with different email: {test_user['email']}")

    try:
        response = requests.post(url, json=test_user)
        print(f"📊 Status: {response.status_code}")

        try:
            response_json = response.json()
            print(f"📃 Response: {json.dumps(response_json, indent=2)}")
        except:
            print(f"📃 Response (raw): {response.text}")

        return response.status_code

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


if __name__ == "__main__":
    print("🚀 Starting API tests...\n")

    if test_health():
        print("✅ Server is running, testing registration...\n")
        status1, response1 = test_registration()

        # If first registration failed, try with different email
        if status1 == 400:
            print("\n" + "=" * 50)
            print("First registration failed, trying with different email...")
            status2 = test_existing_user()

            if status2 == 201:
                print("✅ Second registration worked! The first email might already be in use.")
            elif status2 == 400:
                print("❌ Both registrations failed. There might be a validation or server issue.")

    else:
        print("❌ Server not accessible. Please start it with: uvicorn app.main:app --reload")