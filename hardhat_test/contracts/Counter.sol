// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Counter {
    uint256 number;

    function count() public {
        number += 1;
    }

    function retrieve() public view returns (uint256){
        return number;
    }
}