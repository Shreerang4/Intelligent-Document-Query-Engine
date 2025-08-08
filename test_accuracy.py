#!/usr/bin/env python3
import requests
import json
import time

def test_accuracy_focused():
    """Test with only the first 3 questions for high accuracy"""
    url = "https://bajajhack-production-cf2c.up.railway.app/hackrx/run"
    
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer b67c9abf3c4db8e30556bc012a00cdb3f4072ccd6502a59372dc1aa1cc24f14d",
        "Content-Type": "application/json"
    }
    
    # Focus on first 3 questions for high accuracy
    data = {
        "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
        "questions": [
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
            "What is the waiting period for pre-existing diseases (PED) to be covered?",
            "What are the coverage limits for different types of medical expenses under this policy?"
        ]
    }
    
    print("=== Testing RAG API with Accuracy Focus ===")
    print(f"URL: {url}")
    print(f"Questions: {len(data['questions'])} (focusing on accuracy)")
    print(f"Document: {data['documents']}")
    
    try:
        start_time = time.time()
        response = requests.post(url, headers=headers, json=data, timeout=300)  # 5 minutes timeout
        
        if response.status_code == 200:
            result = response.json()
            total_time = time.time() - start_time
            print("✅ Success!")
            print(f"Total processing time: {total_time:.2f} seconds")
            print(f"Average time per question: {total_time/len(data['questions']):.2f} seconds")
            print("\n=== ANSWERS ===")
            for i, answer in enumerate(result['answers'], 1):
                print(f"\nQuestion {i}: {data['questions'][i-1]}")
                print(f"Answer: {answer}")
                print("-" * 80)
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out (5 minutes)")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - server might be down")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_health_check():
    """Test the health endpoint"""
    url = "https://bajajhack-production-cf2c.up.railway.app/health"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

if __name__ == "__main__":
    print("=== Accuracy-Focused RAG API Testing ===")
    
    print("\n1. Testing health endpoint...")
    test_health_check()
    
    print("\n2. Testing with 3 questions for accuracy...")
    test_accuracy_focused() 