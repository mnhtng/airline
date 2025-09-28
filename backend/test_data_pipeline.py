#!/usr/bin/env python3
"""
Test script để kiểm tra complete data pipeline
Theo dõi quá trình từ import Excel đến clean data
"""

import sys
import os
import requests
import json
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

def test_processing_summary():
    """Test lấy processing summary"""
    print("📊 Testing processing summary...")
    
    try:
        response = requests.get(f"{BASE_URL}/data-processing/processing-summary")
        if response.status_code == 200:
            result = response.json()
            if result["success"]:
                summary = result["data"]
                print(f"✅ Processing Summary:")
                print(f"   Raw records: {summary.get('raw_records', 0)}")
                print(f"   Processed records: {summary.get('processed_records', 0)}")
                print(f"   Error records: {summary.get('error_records', 0)}")
                print(f"   Missing actypes: {summary.get('missing_actypes', 0)}")
                print(f"   Missing routes: {summary.get('missing_routes', 0)}")
                return True
            else:
                print(f"❌ API returned error: {result.get('message', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_data_cleaning():
    """Test data cleaning stored procedure"""
    print("\n🧹 Testing data cleaning...")
    
    try:
        response = requests.post(f"{BASE_URL}/data-processing/run-data-cleaning")
        if response.status_code == 200:
            result = response.json()
            if result["success"]:
                print(f"✅ Data cleaning completed: {result['message']}")
                return True
            else:
                print(f"❌ Data cleaning failed: {result.get('message', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_revalidate_errors():
    """Test revalidating error data"""
    print("\n🔄 Testing error data revalidation...")
    
    try:
        response = requests.post(f"{BASE_URL}/data-processing/revalidate-error-data")
        if response.status_code == 200:
            result = response.json()
            if result["success"]:
                print(f"✅ Error revalidation completed: {result['message']}")
                return True
            else:
                print(f"❌ Error revalidation failed: {result.get('message', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_flight_data_api():
    """Test flight data API"""
    print("\n📄 Testing flight data API...")
    
    try:
        response = requests.get(f"{BASE_URL}/data-processing/flight-data?limit=5")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Flight data API working - returned {len(result)} records")
            if result:
                print(f"   Sample record: Flight {result[0].get('flightno', 'N/A')} on route {result[0].get('route', 'N/A')}")
            return True
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_missing_dimensions():
    """Test missing dimensions API"""
    print("\n❓ Testing missing dimensions API...")
    
    try:
        response = requests.get(f"{BASE_URL}/data-processing/missing-dimensions")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Missing dimensions API working - found {len(result)} missing dimensions")
            
            # Group by type
            actype_count = len([x for x in result if x.get('type') == 'Actype'])
            route_count = len([x for x in result if x.get('type') == 'Route'])
            
            print(f"   Missing actypes: {actype_count}")
            print(f"   Missing routes: {route_count}")
            
            return True
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_aircrafts_api():
    """Test aircrafts API"""
    print("\n✈️ Testing aircrafts API...")
    
    try:
        response = requests.get(f"{BASE_URL}/aircrafts")
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                aircrafts = result.get("data", [])
                print(f"✅ Aircrafts API working - found {len(aircrafts)} aircrafts")
                return True
            else:
                print(f"❌ API returned error: {result.get('message', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_aircraft_drafts_api():
    """Test aircraft drafts API"""
    print("\n📝 Testing aircraft drafts API...")
    
    try:
        response = requests.get(f"{BASE_URL}/aircraft-drafts")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Aircraft drafts API working - found {len(result)} drafts")
            return True
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Data Pipeline Test")
    print("=" * 50)
    
    tests = [
        ("Processing Summary", test_processing_summary),
        ("Flight Data API", test_flight_data_api),
        ("Missing Dimensions API", test_missing_dimensions),
        ("Aircrafts API", test_aircrafts_api),
        ("Aircraft Drafts API", test_aircraft_drafts_api),
        ("Data Cleaning", test_data_cleaning),
        ("Error Revalidation", test_revalidate_errors),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed!")
    
    print("\n" + "="*50)
    print(f"📋 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Data pipeline is working correctly.")
    else:
        print(f"⚠️ {total - passed} tests failed. Please check the logs above.")
    
    # Final processing summary
    print("\n📊 Final Processing Summary:")
    test_processing_summary()

if __name__ == "__main__":
    main()