from brownie import accounts, network, config, MockV3Aggregator
from web3 import Web3

DECIMALS = 8
STARTINGPRICE = 20000000000
LOCAL_BLOCKHAIN_ENVIRONMENTS = ("development", "ganache-local")
FORKED_LOCAL_ENVIRONMENTS = ("mainnet-fork", "mainnet-fork-dev")


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    if len(MockV3Aggregator) <= 0:
        print(f"Deploying Mocks...")
        MockV3Aggregator.deploy(DECIMALS, STARTINGPRICE, {"from": get_account()})
        print(f"Deployed Mocks")
