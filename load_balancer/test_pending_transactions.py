import requests

# Ethereum node URL
# node_url = "https://mainnet.infura.io/v3/f7f75d77301145a1afd39ffa831b3c10"
node_url = "https://docs-demo.quiknode.pro"
def create_pending_transaction_filter(node_url):
    try:
        # Create JSON-RPC request payload to create new pending transaction filter
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_newPendingTransactionFilter",
            "params": [],
            "id": 1
        }

        # Send JSON-RPC request to Ethereum node
        response = requests.post(node_url, json=payload)

        # Check if request was successful (status code 200)
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()

            print(f"data : {data}")

            # Check if result exists in response
            if "result" in data:
                # Return filter ID
                return data["result"]
            else:
                print(f"Error: Result not found in response1 {data}")
        else:
            print(f"Error: HTTP status code {response.status_code}")

    except Exception as e:
        print(f"Error: {e}")

    return None

def get_filter_changes(node_url, filter_id):
    try:
        # Create JSON-RPC request payload to get filter changes
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getFilterChanges",
            "params": [filter_id],
            "id": 1
        }

        # Send JSON-RPC request to Ethereum node
        response = requests.post(node_url, json=payload)

        # Check if request was successful (status code 200)
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()

            # Check if result exists in response
            if "result" in data:
                # Return list of pending transactions
                return data["result"]
            else:
                print("Error: Result not found in response2")
        else:
            print(f"Error: HTTP status code {response.status_code}")

    except Exception as e:
        print(f"Error: {e}")

    return None


def get_peer_count(node_url):
    try:
        # Create JSON-RPC request payload
        payload = {
            "jsonrpc": "2.0",
            "method": "net_peerCount",
            "params": [],
            "id": 1
        }

        headers = {}

        # Send JSON-RPC request to Ethereum node
        response = requests.post(node_url, json=payload, headers=headers)

        # Check if request was successful (status code 200)
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()

            # Check if result exists in response
            if "result" in data:
                # Convert hex string to integer
                peer_count = int(data["result"], 16)
                return peer_count
            else:
                print("Error: Result not found in response")
        else:
            print(f"Error: HTTP status code {response.status_code}")

    except Exception as e:
        print(f"Error: {e}")

    return None



def get_gas_price_for_transaction(node_url, tx_hash):
    try:
        # Create JSON-RPC request payload
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getTransactionByHash",
            "params": [tx_hash],
            "id": 1
        }

        headers = {}

        # Send JSON-RPC request to Ethereum node
        response = requests.post(node_url, json=payload, headers=headers)

        # Check if request was successful (status code 200)
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()

            # Check if result exists in response
            if "result" in data:
                # Retrieve gas price from result
                gas_price = int(data["result"]["gasPrice"], 16)
                return gas_price
            else:
                print("Error: Result not found in response")
        else:
            print(f"Error: HTTP status code {response.status_code}")

    except Exception as e:
        print(f"Error: {e}")

    return None

def is_syncing(node_url):
    try:
        # Create JSON-RPC request payload
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_syncing",
            "params": [],
            "id": 1
        }

        headers = {}

        # Send JSON-RPC request to Ethereum node
        response = requests.post(node_url, json=payload, headers=headers)

        # Check if request was successful (status code 200)
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()

            # Check if result exists in response
            if "result" in data:
                # If syncing, result is a syncing object; otherwise, result is False
                return data["result"]
            else:
                print("Error: Result not found in response")
        else:
            print(f"Error: HTTP status code {response.status_code}")

    except Exception as e:
        print(f"Error: {e}")

    return None

def get_latest_block_number(node_url):
    try:
        # Create JSON-RPC request payload
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_blockNumber",
            "params": [],
            "id": 1
        }

        headers = {}

        # Send JSON-RPC request to Ethereum node
        response = requests.post(node_url, json=payload, headers=headers)

        # Check if request was successful (status code 200)
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()

            # Check if result exists in response
            if "result" in data:
                # Convert hex string to integer
                latest_block_number = int(data["result"], 16)
                return latest_block_number
            else:
                print("Error: Result not found in response")
        else:
            print(f"Error: HTTP status code {response.status_code}")

    except Exception as e:
        print(f"Error: {e}")

    return None


def calculate_mean_second_half(numbers):
    sum_second_half = sum(numbers[len(numbers)//2:])
    
    num_elements_second_half = len(numbers) - len(numbers) // 2
    
    mean_second_half = sum_second_half / num_elements_second_half
    
    return mean_second_half



if __name__ == "__main__":
    # Create pending transaction filter
    filter_id = create_pending_transaction_filter(node_url)

    if filter_id is not None:
        print(f"Pending transaction filter created. Filter ID: {filter_id}")

        # Get filter changes (pending transactions)
        pending_transactions = get_filter_changes(node_url, filter_id)

        print(len(pending_transactions))

        if pending_transactions is not None:
            
            # Always returns 50 for some reason
            peer_count = get_peer_count(node_url)
            print(f"PeerCount: {peer_count}")

            syncing = is_syncing(node_url)
            print(f"Syncing: {syncing}")

            latest_block = get_latest_block_number(node_url)
            print(f"Latest block: {latest_block}")

            gas_prices = []

            print("Pending Transactions:")
            for tx in pending_transactions:

                # current_gas_price = get_gas_price_for_transaction(node_url, tx)
                # print(f"GasPrice: {current_gas_price}")
                # gas_prices.append(current_gas_price)
                # mean_value_second_half = calculate_mean_second_half(gas_prices)


                print(f"Hash: {tx}")


