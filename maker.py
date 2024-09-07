

#tokens transferred
import requests
from datetime import datetime

# replace with your own API key
api_key = '**********************'

# replace with the contract address of the MKR token
contract_address = '0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2'

# calculate the block numbers for February 24th, 2023
start_date_str = '2024-04-02 00:00:00'
end_date_str = '2024-04-02 23:59:59'
start_date = datetime.strptime(start_date_str, '%Y-%m-%d %H:%M:%S')
end_date = datetime.strptime(end_date_str, '%Y-%m-%d %H:%M:%S')
start_timestamp = int(start_date.timestamp())
end_timestamp = int(end_date.timestamp())

start_block = requests.get(f'https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp={start_timestamp}&closest=before&apikey={api_key}').json()['result']
end_block = requests.get(f'https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp={end_timestamp}&closest=before&apikey={api_key}').json()['result']

# make API call to retrieve transfer transactions on February 24th, 2023
url = f'https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={contract_address}&startblock={start_block}&endblock={end_block}&apikey={api_key}'
response = requests.get(url).json()
transfer_transactions = response['result']

# sum up the value field for each transfer transaction
total_transfer_amount = sum(int(tx['value']) for tx in transfer_transactions)
total_mkr = sum(int(tx['value'])/(10**18) for tx in response['result'])

print(f'Total amount of MKR token transferred on {start_date_str}: {total_transfer_amount} wei')
print(f'Total amount of MKR tokens transferred in the last 24 hours: {total_mkr} MKR')
"""
import requests
import time

# replace with your own API key
api_key = '6K6FJJ7X1Z2FJFHYND38R4U5IM4ARTR22U'

# replace with the contract address of the MKR token
contract_address = '0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2'

# calculate the block numbers for the last 24 hours
current_block = requests.get(f'https://api.etherscan.io/api?module=proxy&action=eth_blockNumber&apikey={api_key}').json()['result']
block_time = int(requests.get(f'https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp={int(time.time())}&closest=before&apikey={api_key}').json()['result'])
start_block = max(0, block_time - 5760) # assuming 15s block time, 5760 blocks in 24 hours
end_block = current_block

# make API call to retrieve total number of transfers within the last 24 hours
url = f'https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={contract_address}&startblock={start_block}&endblock={end_block}&apikey={api_key}'
response = requests.get(url).json()

# create a dictionary to keep track of the total token transfer amount for each address
address_dict = {}

for tx in response['result']:
    sender = tx['from']
    receiver = tx['to']
    value = float(tx['value']) / 1e18 # convert from wei to MKR token
    
    # update the total token transfer amount for the sender and receiver address
    if sender in address_dict:
        address_dict[sender] -= value
    else:
        address_dict[sender] = -value
        
    if receiver in address_dict:
        address_dict[receiver] += value
    else:
        address_dict[receiver] = value

# sort the dictionary by the token transfer amount in descending order
sorted_address = sorted(address_dict.items(), key=lambda x: x[1], reverse=True)

# print the top 10 addresses with the most token transfer
for i in range(10):
    print(f'{sorted_address[i][0]}: {sorted_address[i][1]} MKR')
"""