"""
Simple test script to verify your API endpoints are working correctly
Run this after starting your FastAPI server with: uvicorn app.main:app --reload
"""

import httpx
import asyncio
from datetime import datetime, timedelta
import json

BASE_URL = "http://localhost:8000"


class APITester:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.access_token = None
        self.user_id = None

    async def test_health_check(self):
        """Test health check endpoint"""
        print("🔍 Testing health check...")
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/health")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            print("✅ Health check passed!\n")

    async def test_user_registration(self):
        """Test user registration"""
        print("👤 Testing user registration...")
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "supersecret123",
            "age": 30
        }

        async with httpx.AsyncClient() as client:
            response = await client.post