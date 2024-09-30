#!/bin/sh

IP=$(ifconfig eth0 | grep 'inet' | awk '{print $2}' | sed 's/addr://')
echo "IP: $IP"
INDEX=$(dig -x $IP +short | sed 's/[^0-9]*//g')
echo "INDEX: $INDEX"
ACCOUNT=$(jq -r '.clients' accounts.json | jq 'keys_unsorted' | jq -r "nth($((INDEX-1)))")
echo "ACCOUNT: $ACCOUNT"
PRIVATEKEY=$(jq -r '.clients' accounts.json | jq -r ".[\"$ACCOUNT\"]")
echo "PRIVATEKEY: $PRIVATEKEY"

IPADDRESSZKSYNC=$(dig zksync-local-node-l2-zksync-1 +short)

IPADDRESS=$(dig zksync-local-node-l2-geth-1 +short)


PROVIDER="${IPADDRESS}:8545"

PROVIDERZKSYNC="${IPADDRESSZKSYNC}:3050"

learning_rate=0.01

epochs=10



python client_register.py \
  --provider "http://$PROVIDERZKSYNC" \
  --abi /root/abi.json \
  --account $ACCOUNT \
  --passphrase $PRIVATEKEY \
  --contract $CONTRACT \






