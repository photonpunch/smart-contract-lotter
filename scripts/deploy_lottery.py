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
    account = get_account()

    return Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["var_fee"],
        config["networks"][network.show_active()]["vrf_key_hash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )


def main():
    deploy()
