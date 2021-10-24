import json
import os

from web3 import Web3
from solcx import compile_source, install_solc
from dotenv import load_dotenv

install_solc("0.6.0")

load_dotenv()

private_key = os.getenv("PORTFOLIO_PRIVATE_KEY")
account_addr = os.getenv("PORTFOLIO_ADDR")
chain_id = int(os.getenv("PORTFOLIO_CHAINID"))

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

if(not w3.isConnected()):
    print("ERROR CONNECTING TO LOCAL CHAIN")

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

compiled_sol = compile_source(simple_storage_file, output_values=["abi", "metadata", "bin"],solc_version="0.6.0")

with open("./compiled.json", "w") as file:
    json.dump(compiled_sol, file)

contract_id, contract_interface = compiled_sol.popitem()

bytecode = contract_interface['bin']
abi =  contract_interface['abi']

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.getTransactionCount(account_addr)

transaction_create_contract = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "from": account_addr, 
        "nonce":  nonce,
    })
    
signed_txn = w3.eth.account.sign_transaction(transaction_create_contract, private_key=private_key)

tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Deployed contract with addr {tx_receipt.contractAddress}")

storageInstance = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=abi
)

print(f"Initial Stored Value {storageInstance.functions.retrieve().call()}")


transaction_call_store = storageInstance.functions.store(10).buildTransaction(
    {
        "chainId": chain_id,
        "from": account_addr, 
        "nonce":  nonce+1,
    })

signed_store_tx = w3.eth.account.sign_transaction(transaction_call_store, private_key=private_key)

print("Updating stored Value...")

tx_store_hash = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_store_hash)

# storageInstance.functions.store(25).transact({"from" : account_addr})

print(f"Got updated value {storageInstance.functions.retrieve().call()}")
