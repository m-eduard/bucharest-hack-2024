import sys
import subprocess
from time import sleep
from faker import Faker

contract_address = "0x5fbdb2315678afecb367f032d93f642f64180aa3"
nr_servers = 10
contract = "Counter"
fake = Faker()

nodes_state = dict(
    (i, 0) for i in range(nr_servers)
)

network = dict(
    (i, f'local{i + 1}') for i in range(nr_servers)
)

network_ip = dict(
    (i, f'http://127.0.0.1:{i + 8545}') for i in range(nr_servers)
)

initialised_nodes = dict(
    (i, False) for i in range(nr_servers)
)

most_recent_updated_node = 0

create_contract = "CONTRACT={} npx hardhat run scripts/deploy.js  --network {}"
send_transaction = "STORAGE_ADDRESS={} npx hardhat run scripts/sendTransaction.js --network {}"
get_data = "STORAGE_ADDRESS={} npx hardhat run scripts/ethCall.js --network {}"
# fork_data = "FORK_URL={} FORK_BLOCK_NUMBER={} npx hardhat run scripts/forkingNode.js --network {}"
fork_data = "./kill_and_fork.sh {} {} {}"

if __name__ == "__main__":
    create_contract_cmd = create_contract.format(contract, network[0])
    subprocess.run(create_contract_cmd, shell=True)
    nodes_state[0] += 1
    # initialised_nodes[0] = True

    sleep(1)

    for i in range(1, nr_servers // 2 + 1):
        fork_data_cmd = fork_data.format(i + 8545,  network_ip[0], nodes_state[0])
        subprocess.run(fork_data_cmd, shell=True)
        nodes_state[i] = nodes_state[0]
        # initialised_nodes[i] = True
    
    cvorum_level = 1
    print(f"Reached cvorum level {cvorum_level}")
    while True:
        ok = True
        for i in range(nr_servers):
            if nodes_state[i] != nodes_state[most_recent_updated_node]:
                ok = False
                break
        
        random_node = fake.random_int(min=0, max=nr_servers - 1)
        if not ok:
            while nodes_state[random_node] == nodes_state[most_recent_updated_node]:
                random_node = fake.random_int(min=0, max=nr_servers - 1)

            fork_data_cmd = fork_data.format(random_node + 8545, network_ip[most_recent_updated_node], nodes_state[random_node] + 1)
            subprocess.run(fork_data_cmd, shell=True)

            nodes_state[random_node] += 1
        else:
            most_recent_updated_node = random_node
            inc_value = 3
            for i in range(inc_value):
                nodes_state[random_node] += 1
                send_transaction_cmd = send_transaction.format(contract_address, network[random_node])
                subprocess.run(send_transaction_cmd, shell=True)


        print(f"Updated node {random_node} to level {nodes_state[random_node]}")

        cnt_dict = dict()
        new_cvorum = False
        for i in range(nr_servers):
            cnt_dict[nodes_state[i]] = cnt_dict.get(nodes_state[i], 0) + 1
            if cnt_dict[nodes_state[i]] > nr_servers // 2 and cvorum_level < nodes_state[i]:
                cvorum_level = nodes_state[i]
                new_cvorum = True
                break

        if new_cvorum:
            print(f"Reached cvorum level {cvorum_level}")
        
            for i in range(nr_servers):
                if nodes_state[i] != cvorum_level:
                    fork_data_cmd = fork_data.format(i + 8545, network_ip[most_recent_updated_node], cvorum_level)
                    subprocess.run(fork_data_cmd, shell=True)
                    nodes_state[i] = cvorum_level
                    # initialised_nodes[i] = True
            
