import os, sys
from web3 import Web3

class Utils:

    def __init__(self, addr):
        self.w3 = Web3(Web3.HTTPProvider(addr))
        if(not self.w3.isConnected()):
            sys.exit(f"ERROR CONNECTING TO {addr}")   

        self.private_key = os.getenv("PORTFOLIO_PRIVATE_KEY")
        self.account_addr = os.getenv("PORTFOLIO_ADDR")
        self.chain_id = int(os.getenv("NET_CHAIN_ID"))

    def send_signed_transaction(self, tx):
        siegned_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(siegned_tx.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return [tx_hash, tx_receipt]
    



