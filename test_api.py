#!/usr/bin/env python3
import requests
import json
import time

def test_api():
    url = "https://bajajhack-production-cf2c.up.railway.app/hackrx/run"
    
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer b67c9abf3c4db8e30556bc012a00cdb3f4072ccd6502a59372dc1aa1cc24f14d",
        "Content-Type": "application/json"
    }
    
    data = {
        "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
        "questions": [
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
            "What is the waiting period for pre-existing diseases (PED) to be covered?"
        ]
    }
    
    print("Testing API with 2 questions first...")
    print(f"URL: {url}")
    print(f"Questions: {len(data['questions'])}")
    
    try:
        # Test with longer timeout
        response = requests.post(url, headers=headers, json=data, timeout=300)  # 5 minutes timeout
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(f"Response: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out (5 minutes)")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - server might be down")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_health():
    url = "https://bajajhack-production-cf2c.up.railway.app/health"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

if __name__ == "__main__":
    print("=== Testing RAG API ===")
    
    print("\n1. Testing health endpoint...")
    test_health()
    
    print("\n2. Testing main API endpoint...")
    test_api() 