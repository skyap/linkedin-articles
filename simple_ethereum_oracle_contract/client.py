import web3
from web3 import Web3
from web3.middleware import geth_poa_middleware

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
if w3.isConnected():
    if web3.__version__.split(".")[0] == "4":
        w3.middleware_stack.inject(geth_poa_middleware,layer=0)
    else:
        w3.middleware_onion.inject(geth_poa_middleware,layer=0)
else:
    assert False, "No connection"
w3.eth.defaultAccount = w3.eth.accounts[0]


with open("contract_address.txt","r") as f:
    contract_address = f.read()
with open("abi.txt","r") as f:
    abi = f.read()   

contract = w3.eth.contract(abi=abi,address=contract_address)

result = contract.functions.getETHPrice().call()
contract.functions.updateETHPrice().transact()

print("ETH Market Price:",result/100)
print("Requesting Oracle to update Price")