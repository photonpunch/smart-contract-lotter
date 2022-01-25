//SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract Lottery {
    using SafeMathChainlink for uint256;
    address public owner;
    uint256 public usdEntryFee;
    bool public isLotteryRunning;
    AggregatorV3Interface internal ethUsdPriceFeed;
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    constructor(address _ethUsdPriceFeedAddress) public {
        owner = msg.sender;
        usdEntryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_ethUsdPriceFeedAddress);
    }

    address payable[] public players;

    function enter() public payable {
        // Set Minimum 50$
        uint256 feeAtEnterTime = getEntranceFee();
        require(
            msg.value > feeAtEnterTime,
            "Fee is not large enought to take part in lottery!"
        );
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
            !isLotteryRunning,
            "Lottery is already running cannot start it."
        );
        isLotteryRunning = true;
    }

    function endLottery() public onlyOwner {
        require(
            isLotteryRunning,
            "Lottery is not running. It must be started before it can be ended."
        );
        isLotteryRunning = false;
    }
}
