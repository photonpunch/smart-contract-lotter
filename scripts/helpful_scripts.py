from brownie import (
    accounts,
    network,
    config,
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
    Contract,
)
from web3 import Web3

LOCAL_BLOCKHAIN_ENVIRONMENTS = ("development", "ganache-local")
FORKED_LOCAL_ENVIRONMENTS = ("mainnet-fork", "mainnet-fork-dev")


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    """This function will grab the contract addresses from brownie config
    if defined otherwise will deploy a mock version of that contract, and return a mock contract.

        Args:
            contract_name (string)
        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed version
            of the contract
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["netowrks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )

    return contract


DECIMALS = 8
INITIAL_VALUE = 20000000000


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    if len(MockV3Aggregator) <= 0:
        print(f"Deploying Mocks...")
        MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
        LinkToken.deploy({"from": account})
        VRFCoordinatorMock.deploy(LinkToken[-1], {"from": account})
        print(f"Deployed Mocks")
