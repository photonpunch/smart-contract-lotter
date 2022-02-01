from brownie import network, config, Lottery
from scripts.helpful_scripts import (
    deploy_mocks,
    get_account,
    MockV3Aggregator,
    LOCAL_BLOCKHAIN_ENVIRONMENTS,
    get_contract,
)


def deploy():
    print(f"Running deployment on {network.show_active()}")
    account = get_account(id="learning-cotract-account")

    return Lottery.deploy(
        get_contract("eth_usd_price_feed"),
        get_contract("vrf_coordinator"),
        {"from": account},
    )


def main():
    deploy()
