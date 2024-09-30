#!/bin/sh


# commands to execute if condition is false
cp /root/.ethereum/_geth/nodekey_owner /root/.ethereum/geth/nodekey



geth --networkid=${NETWORK_ID} "$@"
