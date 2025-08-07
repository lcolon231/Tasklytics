#!/usr/bin/env python3
"""
Test task management functionality
"""

import requests
import json
from datetime import datetime, timedelta


def get_auth_token():
    """Get authentication token"""
    url = "http://localhost:8000/auth/token"
    login_data = {
        "username": "john.doe@example.com",
        "password": "supersecret123"
    }

    try:
        response = requests.post(url, data=login_data)
        if response.status_code == 200:
            return response.json().get('access_token')
    except:
        pass
    return None


def test_create_task(token):
    """Test creating a task"""
    url = "http://localhost:8000/tasks/"

    # Task data
    due_date = (datetime.utcnow() + timedelta(days=1)).isoformat() + "Z"
    task_data = {
        "title": "Complete API Testing",
        "description": "Test all endpoints to make sure they work correctly",
        "due_at": due_date,
        "user_email": "john.doe@example.com"
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print("📝 Testing task creation...")
    print(f"📤 Sending POST to: {url}")
    print(f"📋 Task: {task_data['title']}")
    print(f"⏰ Due: {due_date}")

    try:
        response = requests.post(url, json=task_data, headers=headers)

        print(f"\n📊 Response Status: {response.status_code}")

        if response.status_code == 201:
            task_response = response.json()
            print(f"📃 Created Task: {json.dumps(task_response, indent=2)}")
            print("✅ Task creation successful!")
            return task_response.get('id')
        else:
            print(f"❌ Task creation failed with status {response.status_code}")
            try:
                error = response.json()
                print(f"📃 Error: {json.dumps(error, indent=2)}")
            except:
                print(f"📃 Error (raw): {response.text}")
            return None

    except Exception as e:
        print(f"❌ Task creation error: {str(e)}")
        return None


def test_get_tasks(token):
    """Test getting user's tasks"""
    url = "http://localhost:8000/tasks/"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    print(f"\n📋 Testing get tasks: {url}")

    try:
        response = requests.get(url, headers=headers)

        print(f"📊 Response Status: {response.status_code}")

        if response.status_code == 200:
            tasks = response.json()
            print(f"📃 User Tasks ({len(tasks)} found):")
            for task in tasks:
                print(f"  - {task['title']} (ID: {task['id']}) - Due: {task['due_at']}")
            print("✅ Get tasks successful!")
            return tasks
        else:
            print(f"❌ Get tasks failed with status {response.status_code}")
            return []

    except Exception as e:
        print(f"❌ Get tasks error: {str(e)}")
        return []


if __name__ == "__main__":
    print("🚀 Testing task management...\n")

    # Get authentication token
    print("🔐 Getting authentication token...")
    token = get_auth_token()

    if not token:
        print("❌ Could not get authentication token")
        print("Make sure to run test_registration.py first to create a user")
        exit(1)

    print("✅ Authentication token obtained")

    # Test creating a task
    task_id = test_create_task(token)

    # Test getting tasks
    tasks = test_get_tasks(token)

    if task_id and tasks:
        print("\n🎉 All task management tests passed!")
        print(f"✅ Created task with ID: {task_id}")
        print(f"✅ Retrieved {len(tasks)} tasks")
    else:
        print("\n⚠️ Some task tests failed, but basic functionality might still work")