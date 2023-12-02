from web3 import Web3, logs

# Initialize Infura connection
infura_url = "https://mainnet.infura.io/v3/YOUR-PROJECT-ID"
web3 = Web3(Web3.HTTPProvider(infura_url))

# Check if connection is successful
if not web3.is_connected():
    raise Exception("Failed to connect to Ethereum network using Infura")

# ERC20 contract details
contract_address = Web3.to_checksum_address("INSERT CONTRACT ADDRESS HERE FOR ERC20")  # Replace with the actual contract address
abi = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "from", "type": "address"},
            {"indexed": True, "internalType": "address", "name": "to", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"}
        ],
        "name": "Transfer",
        "type": "event"
    }
]

# Initialize contract instance
contract = web3.eth.contract(address=contract_address, abi=abi)

# Get past Transfer events
past_events = contract.events.Transfer.get_logs(fromBlock=0, toBlock='latest')

# Get unique holders
holders = set()
for event in past_events:
    holders.add(event['args']['from'])
    holders.add(event['args']['to'])

# Write unique holders to a file
with open('erc20_holders.txt', 'w') as f:
    for holder in holders:
        f.write(holder + '\n')