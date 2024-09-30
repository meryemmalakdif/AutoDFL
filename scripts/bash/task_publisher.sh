#!/bin/sh
IP=$(ifconfig eth0 | grep 'inet' | awk '{print $2}' | sed 's/addr://')
echo "IP: $IP"
INDEX=$(dig -x $IP +short | sed 's/[^0-9]*//g')
echo "INDEX: $INDEX"
ACCOUNT=$(jq -r '.taskpublishers' accounts.json | jq 'keys_unsorted' | jq -r "nth($((INDEX-1)))")
echo "ACCOUNT: $ACCOUNT"
PRIVATEKEY=$(jq -r '.taskpublishers' accounts.json | jq -r ".[\"$ACCOUNT\"]")
echo "PRIVATEKEY: $PRIVATEKEY"

IPADDRESSZKSYNC=$(dig zksync-local-node-l2-zksync-1 +short)

IPADDRESS=$(dig zksync-local-node-l2-geth-1 +short)

# IPADDRESS=$(dig one_rpc-endpoint_1 +short)


# IPADDRESS=$(dig one-validator-3 +short)

echo $IPADDRESS

PROVIDER="${IPADDRESS}:8545"

PROVIDERZKSYNC="${IPADDRESSZKSYNC}:3050"


# ACCOUNT="0xB9aB26D58FDebB5aF7e28e2e67A3aE8A156d9289"
# # PRIVATEKEY="0xfcb9e5138243a3edb01e432284695da54094ac4b953d285dd36e646cd8b9ac2d"
# PRIVATEKEY="GEOlN70MkIZ2eGZ"

echo $PRIVATEKEY

python task_publisher.py \
  --provider "http://$PROVIDERZKSYNC" \
  --abi /root/abi.json \
  --ipfs $IPFS_API \
  --account $ACCOUNT \
  --passphrase $PRIVATEKEY \
  --contract $CONTRACT \
  --rounds $ROUNDS \
  --required_trainers_number $TRAINERS \
  




