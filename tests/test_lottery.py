from brownie import Lottery, accounts, web3, exceptions
import pytest
from scripts.helpful_scripts import get_account
from scripts.deploy_lottery import deploy
from web3 import Web3
import pytest


def test_get_entrance_fee():
    # Arrange
    account = get_account()
    lotteryContract = deploy()
    entranceFee = lotteryContract.getEntranceFee()
    print(entranceFee)
    first_partecipant = accounts[1]
    print(account.balance())
    print(first_partecipant.balance())
    # Expect exception on this
    with pytest.raises(exceptions.VirtualMachineError):
        lotteryContract.enter({"from": first_partecipant, "value": entranceFee - 10000})
    with pytest.raises(exceptions.VirtualMachineError):
        lotteryContract.enter({"from": first_partecipant, "value": entranceFee + 10000})
    with pytest.raises(exceptions.VirtualMachineError):
        lotteryContract.startLottery({"from": first_partecipant})
    with pytest.raises(exceptions.VirtualMachineError):
        lotteryContract.endLottery({"from": first_partecipant})
    with pytest.raises(exceptions.VirtualMachineError):
        lotteryContract.endLottery({"from": account})

    lotteryContract.startLottery({"from": account})

    with pytest.raises(exceptions.VirtualMachineError):
        lotteryContract.enter({"from": first_partecipant, "value": entranceFee - 10000})

    lotteryContract.enter({"from": first_partecipant, "value": entranceFee + 10000})
    lotteryContract.enter({"from": accounts[2], "value": entranceFee * 100})
    lotteryContract.enter({"from": accounts[3], "value": entranceFee * 100})

    assert lotteryContract.balance() == 3 * entranceFee

    print(lotteryContract.balance())
    # assert entranceFee > web3.toWei(0.018, "ether")
    # assert entranceFee < web3.toWei(0.022, "ether")
