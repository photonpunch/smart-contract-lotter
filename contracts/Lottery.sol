//SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery is Ownable, VRFConsumerBase {
    using SafeMathChainlink for uint256;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;
    address payable[] public players;
    bytes32 public keyHash;
    uint256 public fee;
    uint256 public randomness;
    address payable public recentWinner;

    event RequestedRandomness(bytes32 requestId);

    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING
    }

    LOTTERY_STATE public lottery_state;

    constructor(
        address _ethUsdPriceFeedAddress,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyhash
    ) public VRFConsumerBase(_vrfCoordinator, _link) {
        lottery_state = LOTTERY_STATE.CLOSED;
        usdEntryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_ethUsdPriceFeedAddress);
        fee = _fee;
        keyHash = _keyhash;
    }

    function enter() public payable {
        require(
            lottery_state == LOTTERY_STATE.OPEN,
            "Lottery is not currently running please wait for admin to start!"
        );
        // Set Minimum 50$
        uint256 feeAtEnterTime = getEntranceFee();
        require(msg.value > feeAtEnterTime, "Fee too small!");
        msg.sender.transfer(msg.value - feeAtEnterTime);
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
            lottery_state == LOTTERY_STATE.CLOSED,
            "Lottery is already running cannot start it."
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.OPEN,
            "Lottery is not running. It must be started before it can be ended."
        );
        lottery_state = LOTTERY_STATE.CALCULATING;
        bytes32 requestId = requestRandomness(keyHash, fee);
        emit RequestedRandomness(requestId);
    }

    /**
     * Callback function used by VRF Coordinator
     */
    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        require(
            lottery_state == LOTTERY_STATE.CALCULATING,
            "You aren't there yet!."
        );
        require(_randomness > 0, "random-not-found");
        //Set winner.
        uint256 indexOfWinner = _randomness % players.length;
        randomness = _randomness;
        recentWinner = players[indexOfWinner];
        recentWinner.transfer(address(this).balance);

        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
    }
}
