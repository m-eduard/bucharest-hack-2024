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
  echo "Stopping node on port $port"

  pid=$(lsof -ti:$port)
  if [ ! -z "$pid" ]; then
    kill $pid
    echo "Process on port $port stopped."
  else
    echo "No process found on port $port."
  fi
done

echo "All specified nodes have been stopped."