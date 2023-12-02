from web3 import Web3

# Initialize Infura connection
infura_url = "https://mainnet.infura.io/v3/YOUR-PROJECT-ID"  # Replace with your Infura URL
web3 = Web3(Web3.HTTPProvider(infura_url))

# Check if connection is successful
if not web3.is_connected():
    raise Exception("Failed to connect to Ethereum network using Infura")

# Smart contract details
contract_address = Web3.to_checksum_address("INSERT CONTRACT ADDRESS HERE FOR ERC721")  # Replace with the actual contract address
abi = [
    {
        "constant": True,
        "inputs": [{"name": "tokenId", "type": "uint256"}],
        "name": "ownerOf",
        "outputs": [{"name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]

# Initialize contract instance
contract = web3.eth.contract(address=contract_address, abi=abi)

# Function to get unique holders
def get_unique_holders(max_tokens):
    holders = set()
    for token_id in range(1, max_tokens + 1):  # Assuming token IDs start from 1
        try:
            owner = contract.functions.ownerOf(token_id).call()
            holders.add(owner)
        except Exception as e:
            print(f"Error fetching owner for token ID {token_id}: {e}")
    return holders

# Fetching and saving holders
try:
    max_tokens = 50   # Set the maximum number of tokens, adjust as needed
    holders = get_unique_holders(max_tokens)

    # Writing holders to a file
    with open("erc721_holders.txt", "w") as file:
        for holder in holders:
            file.write(holder + "\n")

    print(f"Unique holders data saved. Total holders: {len(holders)}")
except Exception as e:
    print(f"An error occurred: {e}")