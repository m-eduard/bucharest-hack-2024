#!/bin/bash

PORT=$1
URL=$2
NR_BLOCKS=$3

# Check if the port number is provided
if [[ -z "$PORT" ]]; then
    echo "Error: No port specified."
    exit 1
fi

# Check if the URL and block number are provided
if [[ -z "$URL" ]] || [[ -z "$NR_BLOCKS" ]]; then
    echo "Error: URL and block number must be specified."
    exit 1
fi

# Find the process using the specified port and kill it
PID=$(lsof -ti:$PORT)
if [[ ! -z "$PID" ]]; then
    kill -9 $PID
fi

# Run the hardhat node command in the background
npx hardhat node --port $PORT --fork $URL --fork-block-number $NR_BLOCKS &