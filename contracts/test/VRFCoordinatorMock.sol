// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/LinkTokenInterface.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract VRFCoordinatorMock {
    LinkTokenInterface public LINK;

    event RandomnessRequest(
        address indexed sender,
        bytes32 indexed keyHash,
        uint256 indexed seed
    );

    event Response(
        bool success,
        bytes data,
        address consumentContract,
        uint256 randomness,
        bytes32 requestId,
        bytes4 selector
    );

    constructor(address linkAddress) public {
        LINK = LinkTokenInterface(linkAddress);
    }

    function onTokenTransfer(
        address sender,
        uint256 fee,
        bytes memory _data
    ) public onlyLINK {
        (bytes32 keyHash, uint256 seed) = abi.decode(_data, (bytes32, uint256));
        emit RandomnessRequest(sender, keyHash, seed);
    }

    function callBackWithRandomness(
        bytes32 requestId,
        uint256 randomness,
        address consumerContract
    ) public {
        VRFConsumerBase v;
        bytes memory resp = abi.encodeWithSelector(
            v.rawFulfillRandomness.selector,
            requestId,
            randomness
        );
        uint256 b = 206000;
        require(gasleft() >= b, "not enough gas for consumer");
        (bool success, bytes memory data) = consumerContract.call(resp);
        emit Response(
            success,
            data,
            consumerContract,
            randomness,
            requestId,
            v.rawFulfillRandomness.selector
        );
    }

    modifier onlyLINK() {
        require(msg.sender == address(LINK), "Must use LINK token");
        _;
    }
}
