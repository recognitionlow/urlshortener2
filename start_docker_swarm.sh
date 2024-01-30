#!/bin/bash
USAGE="Usage: $0 IP1 IP2 IP3 ..."

if [ "$#" == "0" ]; then
	echo "$USAGE"
	exit 1
fi

COMMAND=$(ssh student@$1 docker swarm leave --force > /dev/null 2>&1; docker swarm init --advertise-addr $1 | grep "docker swarm" | head -n 1)
shift
while (( "$#" )); do
    ssh student@$1 "docker swarm leave --force; $COMMAND"
    shift
done