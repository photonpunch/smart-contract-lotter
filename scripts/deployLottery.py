from brownie import network, config, Lottery
from scripts.helpful_scripts import (
    deploy_mocks,
    get_account,
    MockV3Aggregator,
    LOCAL_BLOCKHAIN_ENVIRONMENTS,
)


def deploy():
    print(f"Running deployment on {network.show_active()}")
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKHAIN_ENVIRONMENTS:
        aggregatorAddress = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        if len(MockV3Aggregator) == 0:
            deploy_mocks()
        aggregatorAddress = MockV3Aggregator[-1].address

    return Lottery.deploy(aggregatorAddress, {"from": account})


def main():
    deploy()
