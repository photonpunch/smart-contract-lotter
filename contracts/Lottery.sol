//SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery is Ownable {
    using SafeMathChainlink for uint256;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING
    }

    LOTTERY_STATE public lottery_state;

    constructor(address _ethUsdPriceFeedAddress) public {
        lottery_state = LOTTERY_STATE.CLOSED;
        usdEntryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_ethUsdPriceFeedAddress);
    }

    address payable[] public players;

    function enter() public payable {
        require(
            lottery_state == LOTTERY_STATE.OPEN,
            "Lottery is not currently running please wait for admin to start!"
        );
        // Set Minimum 50$
        uint256 feeAtEnterTime = getEntranceFee();

        require(msg.value > feeAtEnterTime, "Fee too small!");
        //founderror
        //require(
        //    msg.value > feeAtEnterTime,
        //    "Fee is not large enought to take part in lottery!"
        //);
        //Sends back change
        msg.sender.send(msg.value - feeAtEnterTime);
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10**10; //18 decimals 8 from feed
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice;
        return costToEnter;
    }

    function startLottery() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.CLOSED &&
                lottery_state != LOTTERY_STATE.CALCULATING,
            "Lottery is already running cannot start it."
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        require(
            lottery_state != LOTTERY_STATE.CLOSED &&
                lottery_state != LOTTERY_STATE.CALCULATING,
            "Lottery is not running. It must be started before it can be ended."
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }
}
