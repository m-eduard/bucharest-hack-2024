import multiprocessing
import time
from typing import Dict
from collections import defaultdict
from datetime import datetime as dt

import requests
import json

s = requests.Session()

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

interval = 1 / 50

def modify_request_for_block_number(original_request, block_number):
    # Start the timer
    start_time = time.perf_counter() * 1000  # Convert seconds to milliseconds

    # Modify the request for the specific block number

    # Split the RPC requests in 2 categories:
    # - requests which can modify the blockchain (should use the latest state)
    # - requests used for reading the current state of the blockchain (can view an older view)
    if "_send" in original_request["method"]:
        return original_request

    # Deep copy the original request to avoid modifying it directly
    modified_request = original_request.copy()
    
    # Modify the request to specify the block number
    if "latest" in original_request["params"]:
        modified_request["params"][
            original_request["params"].index("latest")] = f"0x{block_number:x}"
        
    # Stop the timer
    end_time = time.perf_counter() * 1000  # Convert seconds to milliseconds

    # Calculate the elapsed time in milliseconds
    time_taken_ms = end_time - start_time

    # Print the modified request and time taken
    # print(f"modified_request: {modified_request}")
    # print(f"Time taken: {time_taken_ms:.6f} milliseconds")

    return modified_request


# We aim to send the requests to almost all of the nodes in the network]
# (meaning the nodes which have a block height greater than the cvorum of the network)
# IMPORTANT: This way, we don't lose throughput, because we don't exclude the
#            nodes which have a higher state, but  we rollback the arguments
#            which are specified to 'latest' to the number of blocks of the cvorum
# But, we lose latency, because we have to go a couple of blocks back in order
# to execute a request in the context of an older block

# We have to measure the efficiency needed to decodify and rehashh the new args
# for the read operations

# Send requests to the RPC Server of the dev network


def load_balance(q, node_pool: Dict[str, str]):
    nodes_health = {node: "Healthy" for node in node_pool}

    available_nodes = []
    current_idx = 0
    cvorum_level = 0

    while True:
        print("Load balancing ...")
        available_nodes_sz = q.get()

        if available_nodes_sz != 0:
            available_nodes.clear()
            cvorum_level = q.get()

        for i in range(available_nodes_sz):
            available_nodes.append(q.get())
        
        current_idx = (current_idx + 1) % len(available_nodes)

        # example of RPC requests forwarded through our balancer
        transactions_from = "0xf39fd6e51aad88f6f4ce6ab8827279cfffb92266"
        request_from_client = {
            "jsonrpc":"2.0",
            "method":"eth_getTransactionCount",
            "params":[
                transactions_from,
                "latest"
            ],
            "id":1
        }
        request_from_client = modify_request_for_block_number(request_from_client, cvorum_level)

        resp = s.post(
                f"http://{node_pool[available_nodes[current_idx]]}",
                headers={"Content-Type": "application/json", 'Accept': 'text/plain'},
                data=json.dumps(request_from_client),
            )

        resp_json = resp.json()
        # resp_json["result"] = int(resp_json["result"], 0)

        current_time = dt.now()
        print(current_time, f"Response from node {available_nodes[current_idx]}\n",
              json.dumps(resp_json, indent=4))


def nodes_monitor(q, node_pool: Dict[str, str]):
    cvorum_lvl = 0
    prev_cvorum_lvl = 0

    nodes_num_blocks = {}

    latest_change_idx = -1
    latest_change_idxes = []

    iter_no = 0

    while True:
        node_levels = defaultdict(int)
        status_node_msg = ""
        
        for node, node_ip in node_pool.items():
            node_data_request = {
                "jsonrpc": "2.0",
                "method": "eth_blockNumber",
                "params": [],
                "id": 1,
            }

            resp = requests.post(
                f"http://{node_ip}",
                headers={"Content-Type": "application/json", 'Accept': 'text/plain'},
                data=json.dumps(node_data_request),
            )

            resp_json = resp.json()
            num_blocks = int(resp_json["result"], 0)

            old_num_blocks = nodes_num_blocks[node] if node in nodes_num_blocks else 0
            if old_num_blocks != num_blocks:
                latest_change_idx = node
                latest_change_idxes.append(node)
                if (len(latest_change_idxes) > 10):
                    latest_change_idxes.pop(0)

            nodes_num_blocks[node] = num_blocks
            node_levels[num_blocks] += 1
            
            nice_format = ""
            for elem in latest_change_idxes:
                nice_format += "   " if elem != node else "(+)"

            idx_of_current_node_in_change_context = latest_change_idxes.index(node) if node in latest_change_idxes else -1
            if idx_of_current_node_in_change_context == -1 or iter_no < 10:
                nice_format = ""

            status_node_msg += f"\tNode {node} has {nodes_num_blocks[node]} blocks {nice_format}\n"

            
            # status_node_msg += f"\tNode {node} has {num_blocks} blocks {'(+)' if node == latest_change_idx else ''}\n"
            iter_no += 1
            
        prev_cvorum_lvl = cvorum_lvl
        cvorum_lvl = compute_cvorum_level(node_levels, len(node_pool))

        if cvorum_lvl != prev_cvorum_lvl:
            ls = []
            for node_id in node_pool:
                if nodes_num_blocks[node_id] >= cvorum_lvl:
                    ls.append(node_id)

            q.put(len(ls))
            q.put(cvorum_lvl)

            for node_id in ls:
                q.put(node_id)
        else:
            q.put(0)

        
        current_time = dt.now()
        print("\n" + str(current_time), "\n" + "Node Monitor Status Report","\n"+ 
            status_node_msg +
            f"Cvorum level is: {cvorum_lvl}" + "\n" +
            f"{len(ls)} available servers with >= {cvorum_lvl} blocks" + "\n" +
            " ".join(map(str, range(1,11))) + "\n" +
            " ".join(map(lambda x:(str(x + 1) if nodes_num_blocks[x] >= cvorum_lvl else " "), range(0,10))) + "\n"
        )
        time.sleep(0.1)


def compute_cvorum_level(node_levels, num_nodes):
    max_nodes = max(node_levels.keys())

    while True:
        candidates = 0

        for node_level in node_levels:
            if node_level >= max_nodes:
                candidates += node_levels[node_level]

        if candidates > num_nodes // 2:
            return max_nodes
        max_nodes -= 1


class LoadBalancer:
    def __init__(self, node_pool: Dict[int, str]):
        """Each node has the IP address of the RPC server associated"""
        self.node_pool = node_pool

        self.q = multiprocessing.Queue()

        self.load_balancing_proc = multiprocessing.Process(
            target=load_balance, args=(self.q, self.node_pool)
        )
        self.nodes_monitor_proc = multiprocessing.Process(
            target=nodes_monitor, args=(self.q, self.node_pool)
        )

        self.procs = [self.load_balancing_proc, self.nodes_monitor_proc]


class RPCFactory:
    def __init__(self, node_address: str, method_hash: str) -> None:
        """node_address - address of the node where the RPC will be executed
        method_hash - hash of the method signature to be executed, and the encoded params
        """
        self.request_dict = {
            "method": "eth_call",
            "params": [
                {
                    "from": None,
                    "to": node_address,
                    "data": method_hash,
                },
                "latest",
            ],
            "id": 1,
            "jsonrpc": "2.0",
        }


def send_json_rpc():

    while True:
        start_time = time.time()
        # Calculate elapsed time and sleep if needed
        elapsed_time = time.time() - start_time
        if elapsed_time < interval:
            time.sleep(interval - elapsed_time)


# We're using a shared queue, where the process which polls over
# the nodes in our network notifies a change in the number of blocks
# for a specific node

if __name__ == "__main__":
    nodes = {}

    for node in range(0, 10):
        nodes[node] = f"127.0.0.1:{8545 + node}"

    lb = LoadBalancer(nodes)

    for proc in lb.procs:
        proc.start()

    for proc in lb.procs:
        proc.join()
