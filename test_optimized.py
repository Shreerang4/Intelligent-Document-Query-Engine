#!/usr/bin/env python3
import requests
import json
import time

def test_with_policy_pdf():
    """Test with the original policy PDF but with fewer questions"""
    url = "https://bajajhack-production-cf2c.up.railway.app/hackrx/run"
    
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer b67c9abf3c4db8e30556bc012a00cdb3f4072ccd6502a59372dc1aa1cc24f14d",
        "Content-Type": "application/json"
    }
    
    # Use the original policy PDF but with only 2 questions
    data = {
        "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
        "questions": [
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
            "What is the waiting period for pre-existing diseases (PED) to be covered?"
        ]
    }
    
    print("Testing with policy PDF (2 questions)...")
    print(f"URL: {url}")
    print(f"Questions: {len(data['questions'])}")
    
    try:
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

if __name__ == "__main__":
    print("=== Testing RAG API with Policy PDF (Optimized) ===")
    test_with_policy_pdf() 