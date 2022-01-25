from brownie import Lottery
from scripts.helpful_scripts import get_account
from scripts.deployLottery import deploy


def test_get_entrance_fee():
    account = get_account()
    lotteryContract = deploy()
    entranceFee = lotteryContract.getEntranceFee()
    print(entranceFee)
    assert entranceFee > 0
