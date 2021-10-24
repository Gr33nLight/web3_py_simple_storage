// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "./SimpleStorage.sol";

contract StorageFactory is SimpleStorage {
    SimpleStorage[] public simpleStorageArray;

    function createSimpleStorage() public {
        SimpleStorage simpleStorage = new SimpleStorage();

        simpleStorageArray.push(simpleStorage);
    }

    function sfStore(uint256 _storageIndex, uint256 _storageNumber) public {
        address storageAddress = address(simpleStorageArray[_storageIndex]);

        SimpleStorage simpleStorage = SimpleStorage(storageAddress);

        simpleStorage.store(_storageNumber);
    }

    function sfGet(uint256 _storageIndex) public view returns (uint256) {
        address storageAddress = address(simpleStorageArray[_storageIndex]);

        SimpleStorage simpleStorage = SimpleStorage(storageAddress);

        return simpleStorage.retrieve();
    }
}
