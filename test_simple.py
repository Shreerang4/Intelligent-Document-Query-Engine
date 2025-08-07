#!/usr/bin/env python3
import requests
import json
import time

def test_with_simple_pdf():
    """Test with a simple, small PDF to see if the system works"""
    url = "https://bajajhack-production-cf2c.up.railway.app/hackrx/run"
    
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer b67c9abf3c4db8e30556bc012a00cdb3f4072ccd6502a59372dc1aa1cc24f14d",
        "Content-Type": "application/json"
    }
    
    # Use a simple, small PDF for testing
    data = {
        "documents": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
        "questions": [
            "What is this document about?"
        ]
    }
    
    print("Testing with a simple, small PDF...")
    print(f"URL: {url}")
    print(f"PDF: {data['documents']}")
    print(f"Questions: {len(data['questions'])}")
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=120)  # 2 minutes timeout
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(f"Response: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out (2 minutes)")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - server might be down")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("=== Testing RAG API with Simple PDF ===")
    test_with_simple_pdf() 