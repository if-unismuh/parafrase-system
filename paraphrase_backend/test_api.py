#!/usr/bin/env python3
"""
API Testing Script for Paraphrase Backend
Comprehensive test suite for the FastAPI backend
"""
import requests
import json
import time
import sys
from typing import Dict, Any

BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

def print_test_header(test_name: str):
    """Print formatted test header"""
    print(f"\n{'='*60}")
    print(f"🧪 {test_name}")
    print(f"{'='*60}")

def print_result(endpoint: str, success: bool, data: Dict[Any, Any] = None, error: str = None):
    """Print test result"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} {endpoint}")
    
    if success and data:
        if 'message' in data:
            print(f"   Message: {data['message']}")
        if 'data' in data and isinstance(data['data'], dict):
            # Print key metrics from data
            if 'method' in data['data']:
                print(f"   Method: {data['data']['method']}")
            if 'similarity' in data['data']:
                print(f"   Similarity: {data['data']['similarity']}%")
            if 'processing_time_ms' in data['data']:
                print(f"   Processing Time: {data['data']['processing_time_ms']}ms")
    elif error:
        print(f"   Error: {error}")

def test_root_endpoint():
    """Test root endpoint"""
    print_test_header("Root Endpoint Test")
    
    try:
        response = requests.get(BASE_URL, timeout=10)
        success = response.status_code == 200
        data = response.json() if response.headers.get('content-type', '').startswith('application/json') else None
        print_result("GET /", success, data)
        return success
    except Exception as e:
        print_result("GET /", False, error=str(e))
        return False

def test_health_endpoints():
    """Test health check endpoints"""
    print_test_header("Health Check Endpoints")
    
    endpoints = [
        "/health/",
        "/health/detailed",
        "/health/ready",
        "/health/live"
    ]
    
    results = []
    for endpoint in endpoints:
        try:
            response = requests.get(f"{API_BASE}{endpoint}", timeout=10)
            success = response.status_code == 200
            data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {"status": "ok"}
            print_result(f"GET {endpoint}", success, data)
            results.append(success)
        except Exception as e:
            print_result(f"GET {endpoint}", False, error=str(e))
            results.append(False)
    
    return all(results)

def test_paraphrase_single():
    """Test single text paraphrasing"""
    print_test_header("Single Text Paraphrasing")
    
    test_cases = [
        {
            "name": "Academic Text (Indonesian)",
            "text": "Penelitian ini bertujuan untuk menganalisis dampak teknologi AI terhadap pendidikan modern.",
            "use_search": True
        },
        {
            "name": "Short Text (No Search)",
            "text": "Teknologi AI sangat membantu dalam kehidupan sehari-hari.",
            "use_search": False
        },
        {
            "name": "Business Text (With Search)",
            "text": "Perusahaan teknologi harus beradaptasi dengan perkembangan artificial intelligence.",
            "use_search": True
        }
    ]
    
    results = []
    for case in test_cases:
        print(f"\n📝 Test Case: {case['name']}")
        
        payload = {
            "text": case["text"],
            "use_search": case["use_search"],
            "quality_level": "medium"
        }
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{API_BASE}/paraphrase/text",
                json=payload,
                timeout=30
            )
            end_time = time.time()
            
            success = response.status_code == 200
            data = response.json() if response.headers.get('content-type', '').startswith('application/json') else None
            
            if success and data:
                print(f"   Original: {case['text']}")
                print(f"   Paraphrased: {data['data']['paraphrased_text']}")
                print(f"   Method: {data['data']['metadata']['method']}")
                print(f"   Similarity: {data['data']['metadata']['similarity']}%")
                print(f"   Total Time: {int((end_time - start_time) * 1000)}ms")
                if data['data']['metadata'].get('search_context'):
                    print(f"   Search Context: {data['data']['metadata']['search_context'][:50]}...")
            
            print_result(f"POST /paraphrase/text ({case['name']})", success, data)
            results.append(success)
            
        except Exception as e:
            print_result(f"POST /paraphrase/text ({case['name']})", False, error=str(e))
            results.append(False)
    
    return all(results)

def test_paraphrase_batch():
    """Test batch paraphrasing"""
    print_test_header("Batch Text Paraphrasing")
    
    payload = {
        "texts": [
            "Artificial Intelligence adalah teknologi masa depan.",
            "Machine Learning membantu dalam analisis data besar.",
            "Deep Learning menggunakan neural networks untuk pembelajaran."
        ],
        "use_search": True,
        "quality_level": "medium"
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{API_BASE}/paraphrase/batch",
            json=payload,
            timeout=60
        )
        end_time = time.time()
        
        success = response.status_code == 200
        data = response.json() if response.headers.get('content-type', '').startswith('application/json') else None
        
        if success and data:
            summary = data['data']['summary']
            print(f"\n📊 Batch Summary:")
            print(f"   Total texts: {summary['total_texts']}")
            print(f"   Successful: {summary['successful']}")
            print(f"   Failed: {summary['failed']}")
            print(f"   Average similarity reduction: {summary['average_similarity_reduction']}%")
            print(f"   Total processing time: {summary['total_processing_time_ms']}ms")
            print(f"   API response time: {int((end_time - start_time) * 1000)}ms")
            
            print(f"\n📝 Individual Results:")
            for i, result in enumerate(data['data']['results']):
                print(f"   {i+1}. {result['metadata']['method']} - {result['metadata']['similarity']}% similarity")
        
        print_result("POST /paraphrase/batch", success, data)
        return success
        
    except Exception as e:
        print_result("POST /paraphrase/batch", False, error=str(e))
        return False

def test_paraphrase_stats():
    """Test paraphrase statistics endpoint"""
    print_test_header("Paraphrase Statistics")
    
    try:
        response = requests.get(f"{API_BASE}/paraphrase/stats", timeout=10)
        success = response.status_code == 200
        data = response.json() if response.headers.get('content-type', '').startswith('application/json') else None
        
        if success and data:
            stats = data['data']
            print(f"\n📈 Service Statistics:")
            print(f"   Paraphraser available: {stats['paraphraser_available']}")
            print(f"   DDGS enabled: {stats['ddgs_enabled']}")
            print(f"   AI service configured: {stats['ai_service_configured']}")
            print(f"   Synonym database loaded: {stats['synonym_database_loaded']}")
            print(f"   Max text length: {stats['settings']['max_text_length']:,}")
            print(f"   Max batch size: {stats['settings']['max_batch_size']}")
        
        print_result("GET /paraphrase/stats", success, data)
        return success
        
    except Exception as e:
        print_result("GET /paraphrase/stats", False, error=str(e))
        return False

def test_paraphrase_methods():
    """Test paraphrase methods endpoint"""
    print_test_header("Paraphrase Methods Information")
    
    try:
        response = requests.get(f"{API_BASE}/paraphrase/methods", timeout=10)
        success = response.status_code == 200
        data = response.json() if response.headers.get('content-type', '').startswith('application/json') else None
        
        if success and data:
            methods = data['data']['methods']
            print(f"\n🔧 Available Methods:")
            for method_name, method_info in methods.items():
                print(f"   • {method_info['name']}: {method_info['description']}")
        
        print_result("GET /paraphrase/methods", success, data)
        return success
        
    except Exception as e:
        print_result("GET /paraphrase/methods", False, error=str(e))
        return False

def test_error_handling():
    """Test error handling"""
    print_test_header("Error Handling Tests")
    
    test_cases = [
        {
            "name": "Empty text",
            "payload": {"text": ""},
            "expected_status": 422
        },
        {
            "name": "Text too short",
            "payload": {"text": "Hi"},
            "expected_status": 422
        },
        {
            "name": "Text too long",
            "payload": {"text": "A" * 15000},
            "expected_status": 400
        },
        {
            "name": "Invalid quality level",
            "payload": {"text": "Valid text here", "quality_level": "invalid"},
            "expected_status": 422
        }
    ]
    
    results = []
    for case in test_cases:
        try:
            response = requests.post(
                f"{API_BASE}/paraphrase/text",
                json=case["payload"],
                timeout=10
            )
            
            success = response.status_code == case["expected_status"]
            error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else None
            
            if success:
                print(f"✅ {case['name']}: Correctly returned {response.status_code}")
            else:
                print(f"❌ {case['name']}: Expected {case['expected_status']}, got {response.status_code}")
            
            results.append(success)
            
        except Exception as e:
            print(f"❌ {case['name']}: Exception - {str(e)}")
            results.append(False)
    
    return all(results)

def run_performance_test():
    """Run basic performance tests"""
    print_test_header("Performance Tests")
    
    # Test concurrent requests
    import concurrent.futures
    import threading
    
    def make_request():
        payload = {"text": "Teknologi AI mengubah dunia modern dengan berbagai inovasi."}
        try:
            start = time.time()
            response = requests.post(f"{API_BASE}/paraphrase/text", json=payload, timeout=30)
            end = time.time()
            return response.status_code == 200, int((end - start) * 1000)
        except:
            return False, 0
    
    print("🚀 Testing concurrent requests (5 simultaneous)...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_request) for _ in range(5)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    successful = sum(1 for success, _ in results if success)
    times = [time_ms for success, time_ms in results if success]
    
    if times:
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"   Successful requests: {successful}/5")
        print(f"   Average response time: {avg_time:.0f}ms")
        print(f"   Min response time: {min_time}ms")
        print(f"   Max response time: {max_time}ms")
        
        return successful >= 4  # Allow 1 failure
    
    return False

def main():
    """Run all tests"""
    print("🚀 Starting API Test Suite for Paraphrase Backend")
    print(f"Base URL: {BASE_URL}")
    
    tests = [
        ("Root Endpoint", test_root_endpoint),
        ("Health Endpoints", test_health_endpoints),
        ("Single Text Paraphrasing", test_paraphrase_single),
        ("Batch Paraphrasing", test_paraphrase_batch),
        ("Statistics Endpoint", test_paraphrase_stats),
        ("Methods Information", test_paraphrase_methods),
        ("Error Handling", test_error_handling),
        ("Performance Test", run_performance_test)
    ]
    
    results = []
    start_time = time.time()
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    end_time = time.time()
    
    # Print summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    print(f"⏱️ Total time: {int(end_time - start_time)} seconds")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
        return 0
    else:
        print("⚠️ Some tests failed. Check the API implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())