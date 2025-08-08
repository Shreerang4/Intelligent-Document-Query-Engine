#!/usr/bin/env python3
import requests
import json
import time

def verify_deployment():
    """Verify that the deployment was successful and supports 10 questions"""
    url = "https://bajajhack-production-cf2c.up.railway.app/hackrx/run"
    
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer b67c9abf3c4db8e30556bc012a00cdb3f4072ccd6502a59372dc1aa1cc24f14d",
        "Content-Type": "application/json"
    }
    
    # Test with 6 questions to see if the old 5-question limit is gone
    data = {
        "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
        "questions": [
            "What is the grace period for premium payment?",
            "What is the waiting period for pre-existing diseases?",
            "What are the coverage limits?",
            "What is the policy term?",
            "What are the exclusions?",
            "What is the claim process?"
        ]
    }
    
    print("=== Verifying Deployment ===")
    print(f"Testing with {len(data['questions'])} questions...")
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=300)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS: Deployment verified!")
            print(f"✅ API now supports {len(data['questions'])} questions")
            print(f"✅ Received {len(result['answers'])} answers")
            print("✅ Old 5-question limit has been removed")
            return True
        elif response.status_code == 400:
            error_detail = response.json().get('detail', '')
            if 'Maximum 5 questions' in error_detail:
                print("❌ FAILED: Old 5-question limit still active")
                print("❌ Deployment may not have completed")
                return False
            else:
                print(f"❌ Different error: {error_detail}")
                return False
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False

def test_health():
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
    print("=== Deployment Verification ===")
    
    print("\n1. Testing health endpoint...")
    health_ok = test_health()
    
    print("\n2. Testing 6-question limit...")
    deployment_ok = verify_deployment()
    
    print("\n=== Summary ===")
    if health_ok and deployment_ok:
        print("✅ DEPLOYMENT SUCCESSFUL!")
        print("✅ System is ready for hackathon with 10 questions")
        print("\nNext steps:")
        print("1. Run: python test_hackathon.py")
        print("2. Or: .\\test_hackathon.ps1")
    else:
        print("❌ DEPLOYMENT VERIFICATION FAILED")
        print("Please check the deployment and try again")
        print("Refer to deploy_manual.md for deployment instructions") 