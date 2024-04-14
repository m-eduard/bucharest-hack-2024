import requests
import json
import time

def send_json_rpc(url, payload):
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: HTTP status code {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example JSON-RPC payload
json_rpc_payload = {
    "jsonrpc": "2.0",
    "method": "eth_call",
    "params": {
        "from": "test",
		"to": "dest",
		"gas": "1200",
        },
    "id": 1
}

# URL of the balancer
url = "http://localhost:3000/rpc"

# Number of requests to send
num_requests = 100

# Interval between requests (in seconds)
interval = 1 / 100  # 100 requests per second

# Send requests
for i in range(num_requests):
    start_time = time.time()
    
    # Send JSON-RPC request
    response = send_json_rpc(url, json_rpc_payload)
    
    # Calculate elapsed time and sleep if needed
    elapsed_time = time.time() - start_time
    if elapsed_time < interval:
        time.sleep(interval - elapsed_time)

    # Print response
    if response:
        print(f"Response {i+1}: {response}")

print("All requests sent.")
