#!/bin/sh


IPADDRESSZKSYNC=$(dig zksync-local-node-l2-zksync-1 +short)

IPADDRESS=$(dig zksync-local-node-l2-geth-1 +short)



PROVIDER="${IPADDRESS}:8545"

PROVIDERZKSYNC="${IPADDRESSZKSYNC}:3050"


PRIVATEKEY="0x3eb15da85647edd9a1159a4a13b9e7c56877c4eb33f614546d4db06a51868b1c"

ACCOUNT="0xE90E12261CCb0F3F7976Ae611A29e84a6A85f424"


python admin_apiConsumer.py \
  --provider_layer2 "http://$PROVIDERZKSYNC" \
  --abi_oracle /root/abi.json \
  --account $ACCOUNT \
  --passphrase $PRIVATEKEY \
  --contract_api_consumer $CONTRACT_APICONSUMER \
  --contract_business_logic $BUSINESS_CONTRACT_ADDRESS \

  

  






