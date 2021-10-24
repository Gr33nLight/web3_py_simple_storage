import json
import os

from utils import Utils
from solcx import compile_source, install_solc
from dotenv import load_dotenv

install_solc("0.6.0")

load_dotenv()

account_addr = os.getenv("PORTFOLIO_ADDR")
chain_id = int(os.getenv("PORTFOLIO_CHAINID"))

utils = Utils('http://127.0.0.1:7545');

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

compiled_sol = compile_source(simple_storage_file, output_values=["abi", "metadata", "bin"],solc_version="0.6.0")

with open("./compiled.json", "w") as file:
    json.dump(compiled_sol, file)

contract_id, contract_interface = compiled_sol.popitem()

bytecode = contract_interface['bin']
abi =  contract_interface['abi']

SimpleStorage = utils.w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = utils.w3.eth.getTransactionCount(account_addr)

transaction_create_contract = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "from": account_addr, 
        "nonce":  nonce,
    })
    
tx_hash, tx_receipt = utils.send_signed_transaction(transaction_create_contract)

print(f"Deployed contract with addr {tx_receipt.contractAddress}")

storageInstance = utils.w3.eth.contract(
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

print("Updating stored Value...")

tx_store_hash, tx_receipt = utils.send_signed_transaction(transaction_call_store)

# storageInstance.functions.store(25).transact({"from" : account_addr})

print(f"Got updated value {storageInstance.functions.retrieve().call()}")