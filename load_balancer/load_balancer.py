import multiprocessing
import time
from typing import Dict
from flask import Flask, request, jsonify

import requests

app = Flask(__name__)

cvorum_level = 0

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

    while True:
        print("Load balancing ...")
        item = q.get()

        for i in range(item):
            available_nodes.append(q.get())

        i

        

def nodes_monitor(q, node_pool: Dict[str, str]):
    global_max_num_nodes = 0
    
    node_levels = {}
    while True:
        nodes_num_blocks = {}
        
        for node, node_ip in node_pool.items():
            node_data_request = {
                "jsonrpc": "2.0",
                "method": "eth_blockNumber",
                "params": [],
                "id": 1,
            }

            resp = requests.post(
                node_ip,
                headers={"Content-Type": "application/json"},
                json=node_data_request,
            )

            print(resp.text)
            print(resp)

            nodes_num_blocks[node] = resp.text
            node_levels[resp.data] += 1

        cvorum_lvl = compute_cvorum_level(node_levels, len(node_pool))

        ls = []
        if cvorum_level != -1:
            for node_id in node_pool:
                if nodes_num_blocks[node_id] >= len(node_pool) // 2:
                    ls.append(node_id)

            q.put(len(ls))

            for node_id in ls:
                q.put(node_id)

        print("Monitoring ...")
        time.sleep(12)


def compute_cvorum_level(node_levels, num_nodes):
    for node_level in node_levels:
        if node_levels[node_level] > num_nodes // 2:
            return node_level
        
    return -1


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


@app.route('/rpc', methods=['POST'])
def load_balance():
    data = request.get_json()




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


# We're using a shared queue, where the process which polls over
# the nodes in our network notifies a change in the number of blocks
# for a specific node

if __name__ == "__main__":
    nodes = {0:"127.0.0.1:8545"}

    lb = LoadBalancer(nodes)

    for proc in lb.procs:
        proc.start()

    for proc in lb.procs:
        proc.join()
