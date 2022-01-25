//SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract Lottery {
    address public owner;
    uint256 public usdEntryFee;
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
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {}

    function startLottery() public onlyOwner {}

    function endLottery() public onlyOwner {}
}
