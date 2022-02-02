from os import wait
import time
from brownie import accounts, network, config, Lottery
from dbus import Interface
from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKHAIN_ENVIRONMENTS,
    get_contract,
    fund_with_link,
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
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    lottery.startLottery({"from": account}).wait(1)
    print("Lottery has Started")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    fund_with_link(lottery.address).wait(1)
    # fund the contract
    lottery.endLottery({"from": account}).wait(1)
    print("Lottery ended")


def enter_lottery(index=None):
    account = get_account(index=index)
    Lottery[-1].enter({"from": account, "value": account.balance() / 2})


def check_lottery_status():
    return Lottery[-1].lottery_state()


def main():
    deploy()
    start_lottery()
    enter_lottery(index=1)
    enter_lottery(index=2)
    enter_lottery(index=3)
    enter_lottery(index=4)
    enter_lottery(index=5)
    end_lottery()
    time.sleep(10)
    print(get_account(index=0).balance())
    print(get_account(index=1).balance())
    print(get_account(index=2).balance())
    print(get_account(index=3).balance())
    print(get_account(index=4).balance())
    print(get_account(index=5).balance())
    print(Lottery[-1].balance())
