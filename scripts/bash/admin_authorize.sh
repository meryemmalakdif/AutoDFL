#!/bin/sh


IPADDRESSZKSYNC=$(dig zksync-local-node-l2-zksync-1 +short)

IPADDRESS=$(dig zksync-local-node-l2-geth-1 +short)



PROVIDER="${IPADDRESS}:8545"

PROVIDERZKSYNC="${IPADDRESSZKSYNC}:3050"


PRIVATEKEY="0xe20eb92b34a3c5bd2ef0802a4bc443a90e73fc4a0edc4781446d7b22a44cc5d8"

ACCOUNT="0x8A91DC2D28b689474298D91899f0c1baF62cB85b"


python admin_authorize.py \
  --provider_layer2 "http://$PROVIDER" \
  --abi_oracle /root/abi_operator.json \
  --account $ACCOUNT \
  --passphrase $PRIVATEKEY \
  --contract_oracle $CONTRACT_ORACLE \
  --oracle_node $ORACLE_NODE_ADDRESS \

  

  






