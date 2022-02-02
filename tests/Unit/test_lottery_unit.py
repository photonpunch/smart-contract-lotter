from brownie import network, exceptions
import pytest
from scripts.helpful_scripts import (
    LOCAL_BLOCKHAIN_ENVIRONMENTS,
    fund_with_link,
    get_account,
    get_contract,
    VRFCoordinatorMock,
)
from scripts.deploy_lottery import deploy
from web3 import Web3
import pytest


def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    lottery = deploy()
    # Act
    entranceFee = lottery.getEntranceFee()
    expectedFee = Web3.toWei(0.25, "ether")
    # Assert
    assert expectedFee == entranceFee


def test_cant_enter_if_not_started():
    # Arrange
    lottery = deploy()
    account = get_account()
    # Act/Assert
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": account, "value": lottery.getEntranceFee() + 1000000})


def test_can_start_and_enter_lottery():
    # Arrange
    lottery = deploy()
    account = get_account()
    # Act
    lottery.startLottery({"from": account}).wait(1)
    lottery.enter({"from": account, "value": lottery.getEntranceFee() + 1000000}).wait(
        1
    )
    # Assert
    assert lottery.players(0) == account


def test_can_end_lottery():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy()
    account = get_account()
    # Act
    lottery.startLottery({"from": account}).wait(1)
    lottery.enter({"from": account, "value": lottery.getEntranceFee() + 1000000}).wait(
        1
    )
    fund_with_link(lottery.address)
    lottery.endLottery({"from": account}).wait(1)
    # Assert
    assert lottery.lottery_state() == 2


def test_can_pick_winner_correctly():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy()
    account = get_account()
    # Act
    lottery.startLottery({"from": account}).wait(1)
    lottery.enter(
        {"from": get_account(index=0), "value": lottery.getEntranceFee() + 1000000}
    ).wait(1)
    lottery.enter(
        {"from": get_account(index=1), "value": lottery.getEntranceFee() + 1000000}
    ).wait(1)
    lottery.enter(
        {"from": get_account(index=2), "value": lottery.getEntranceFee() + 1000000}
    ).wait(1)
    fund_with_link(lottery.address).wait(1)
    tx = lottery.endLottery({"from": account})
    tx.wait(1)
    requestId = tx.events["RequestedRandomness"]["requestId"]
    print(f"RequestId is {requestId}")
    vrf_coordinator = get_contract("vrf_coordinator")
    winner_starting_balance = account.balance()
    contract_starting_balance = lottery.balance()
    vrf_tx = vrf_coordinator.callBackWithRandomness(
        requestId, 777, lottery.address, {"from": vrf_coordinator}
    )
    vrf_tx.wait(1)
    print(vrf_tx.events)
    # print(lottery.address)

    # lottery.rawFulfillRandomness(requestId, 777, {"from": vrf_coordinator})

    recentWinnter = lottery.recentWinner()
    print(len(VRFCoordinatorMock))
    # Assert
    assert lottery.balance() == 0
    assert recentWinnter == account
    assert account.balance() == winner_starting_balance + contract_starting_balance
