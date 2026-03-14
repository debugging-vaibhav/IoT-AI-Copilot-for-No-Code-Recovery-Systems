import requests

BASE_URL = "http://localhost:8000/api"

def test_endpoints():
    print("--- Starting Backend Finalization Tests ---\n")
    
    endpoints_to_test = [
        ("GET", f"{BASE_URL}/"),
        ("GET", f"{BASE_URL}/status"),
        ("POST", f"{BASE_URL}/describe-robot", {"description": "Turn ON the fan connected to pin 17"}),
        ("POST", f"{BASE_URL}/generate-logic", {"description": "Turn ON the fan connected to pin 17"}),
        ("POST", f"{BASE_URL}/validate", {
            "sensor": "temperature",
            "pin": 17,
            "action": "ON",
            "rule": "IF temp > 30 THEN ON"
        }),
        ("POST", f"{BASE_URL}/recover", {
            "logic": {
                "sensor": "temperature",
                "pin": 17,
                "action": "ON",
                "rule": "IF temp > 30 THEN ON"
            }
        }),
        ("GET", f"{BASE_URL}/logs")
    ]

    for method, url, *payload in endpoints_to_test:
        try:
            kwargs = {"json": payload[0]} if payload else {}
            if method == "GET":
                r = requests.get(url, **kwargs)
            else:
                r = requests.post(url, **kwargs)
                
            print(f"[{method}] {url.split(BASE_URL)[1] or '/'} : Status {r.status_code}")
            if r.status_code >= 400:
                print(f"   -> Detail: {r.text[:200]}")
        except Exception as e:
            print(f"[{method}] {url} : Failed to connect - {e}")

if __name__ == "__main__":
    test_endpoints()
