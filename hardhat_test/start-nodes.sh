#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <number_of_nodes>"
  exit 1
fi

num_nodes=$1
starting_port=8545

for (( i=1; i<=num_nodes; i++ ))
do
  port=$(($starting_port + i - 1))
  echo "Starting node on port $port"
  npx hardhat node --port $port &
done

echo "All nodes started in background."