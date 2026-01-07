#!/usr/bin/env python3
import urllib.request
import json
import time

# Wait for server to be ready
time.sleep(1)

try:
    # Test basic connection
    r = urllib.request.urlopen('http://localhost:5000/', timeout=5)
    print(f"✓ GET /: Status {r.status}")
    
    # Test /api/db-stats (should return 401 since not authenticated)
    try:
        r = urllib.request.urlopen('http://localhost:5000/api/db-stats', timeout=5)
        print(f"✓ GET /api/db-stats: Status {r.status}")
    except urllib.error.HTTPError as e:
        print(f"✓ GET /api/db-stats: Status {e.code} (expected 401 Unauthorized)")
    
    # Test login endpoint
    data = json.dumps({'email': 'admin@teacher', 'pwd': 'system123', 'user_type': 'teacher'}).encode()
    req = urllib.request.Request('http://localhost:5000/api/login', data=data, headers={'Content-Type': 'application/json'}, method='POST')
    try:
        r = urllib.request.urlopen(req, timeout=5)
        response = json.loads(r.read().decode())
        print(f"✓ POST /api/login: Status {r.status}")
        print(f"  Response: {response}")
    except urllib.error.HTTPError as e:
        print(f"✓ POST /api/login: Status {e.code}")
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
