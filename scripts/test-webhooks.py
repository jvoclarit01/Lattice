import http.server
import json
import threading
import urllib.request
import urllib.error
import time

HOST = "localhost"
PORT = 8089
BASE_URL = f"http://{HOST}:{PORT}"

# 1. Helper function for sorted keys validation
def flatten_keys(obj, prefix=""):
    keys = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            pre = f"{prefix}." if prefix else ""
            keys.update(flatten_keys(v, f"{pre}{k}"))
    elif isinstance(obj, list):
        for idx, item in enumerate(obj[:1]):
            pre = f"{prefix}[]"
            keys.update(flatten_keys(item, pre))
    else:
        keys[prefix] = type(obj).__name__
    return keys

def get_signature(payload):
    flattened = flatten_keys(payload)
    sorted_keys = sorted(f"{k}:{v}" for k, v in flattened.items())
    return ",".join(sorted_keys)


# 2. Local Database / State Simulator for Idempotency
IDEMPOTENCY_STORE = set()

# 3. HTTP Server Handler simulating webhook inputs
class WebhookServerHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass # Suppress standard HTTP logs to keep output clean

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        payload = {}
        try:
            payload = json.loads(post_data.decode('utf-8'))
        except Exception:
            pass

        # Path-based routing
        path = self.path

        # Case A: Loop Depth Guard Ingestion Gate
        if path == "/webhook-depth":
            depth = int(self.headers.get('X-Workflow-Depth', 1))
            if depth > 5:
                self.send_response(429)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"Workflow loop aborted! Depth limit exceeded.")
                return
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"OK - depth {depth}".encode())
            return

        # Case B: Sorted Keys Schema Drift Checker Gate
        elif path == "/webhook-drift":
            expected_sig = "user.active:bool,user.age:int,user.name:str"
            actual_sig = get_signature(payload)
            if actual_sig != expected_sig:
                self.send_response(400)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"Schema drift detected!")
                return
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"OK - schema verified")
            return

        # Case C: Last-Mile Idempotency Constraint Gate
        elif path == "/webhook-idempotency":
            event_id = payload.get("event_id")
            if not event_id:
                self.send_response(400)
                self.end_headers()
                return

            if event_id in IDEMPOTENCY_STORE:
                # Mock return HTTP 200 for duplicate request
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "duplicate_ignored"}).encode())
                return

            # Simulate writing / commit latency
            time.sleep(0.05)
            IDEMPOTENCY_STORE.add(event_id)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "inserted"}).encode())
            return

        self.send_response(404)
        self.end_headers()


def run_server():
    server = http.server.HTTPServer((HOST, PORT), WebhookServerHandler)
    server.serve_forever()


def test_depth_gate():
    # Attempt 1: Safe depth (3)
    req = urllib.request.Request(f"{BASE_URL}/webhook-depth", method="POST")
    req.add_header("X-Workflow-Depth", "3")
    with urllib.request.urlopen(req) as res:
        assert res.status == 200
        assert b"OK - depth 3" in res.read()
    
    # Attempt 2: Runaway depth (6)
    req = urllib.request.Request(f"{BASE_URL}/webhook-depth", method="POST")
    req.add_header("X-Workflow-Depth", "6")
    try:
        urllib.request.urlopen(req)
        assert False, "Depth gate failed to reject loop depth of 6"
    except urllib.error.HTTPError as e:
        assert e.code == 429
        assert b"Depth limit exceeded" in e.read()
    print("OK: Loop Depth Guard verified successfully.")


def test_drift_gate():
    # Attempt 1: Expected payload structure
    valid_payload = json.dumps({"user": {"name": "Alice", "age": 28, "active": True}}).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/webhook-drift", data=valid_payload, method="POST")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as res:
        assert res.status == 200
        assert b"schema verified" in res.read()

    # Attempt 2: Drifted payload structure (missing age, extra country field)
    drifted_payload = json.dumps({"user": {"name": "Alice", "active": True, "country": "US"}}).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/webhook-drift", data=drifted_payload, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        urllib.request.urlopen(req)
        assert False, "Drift gate failed to reject invalid schema"
    except urllib.error.HTTPError as e:
        assert e.code == 400
        assert b"Schema drift detected" in e.read()
    print("OK: Sorted Keys Schema Drift Checker verified successfully.")


def test_idempotency_gate():
    payload = json.dumps({"event_id": "evt_998877"}).encode('utf-8')
    
    # Write 1: Inserts new event
    req = urllib.request.Request(f"{BASE_URL}/webhook-idempotency", data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode())
        assert res.status == 200
        assert data["status"] == "inserted"

    # Write 2: Duplicate event (should return status: duplicate_ignored)
    req = urllib.request.Request(f"{BASE_URL}/webhook-idempotency", data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode())
        assert res.status == 200
        assert data["status"] == "duplicate_ignored"
    print("OK: Last-Mile Idempotency checker verified successfully.")


def main():
    print(f"Starting mock webhook server on {HOST}:{PORT}...")
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    
    # Wait for server startup
    time.sleep(0.5)

    print("Running webhook integration tests...")
    test_depth_gate()
    test_drift_gate()
    test_idempotency_gate()
    print("All webhook tests PASSED.")

if __name__ == "__main__":
    main()
