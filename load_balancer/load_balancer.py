import multiprocessing
import time
from typing import Dict

import requests

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

    while True:
        print("Load balancing ...")
        time.sleep(12)


def nodes_monitor(q, node_pool: Dict[str, str]):
    global_max_num_nodes = 0

    while True:
        for node, node_ip in node_pool.items():
            rpc_json_load = {
                "jsonrpc": "2.0",
                "method": "eth_blockNumber",
                "params": [],
                "id": 1,
            }

            resp = requests.post(
                node_ip,
                headers={"Content-Type": "application/json"},
                json=rpc_json_load,
            )
            print(resp.text)

        print("Monitoring ...")
        time.sleep(12)


class LoadBalancer:
    def __init__(self, node_pool: Dict[str, str]):
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


# We're using a shared queue, where the process which polls over
# the nodes in our network notifies a change in the number of blocks
# for a specific node

if __name__ == "__main__":
    nodes = []
    lb = LoadBalancer(nodes)

    for proc in lb.procs:
        proc.start()

    for proc in lb.procs:
        proc.join()
