// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract SimpleStorage {
    uint256 public favNumber;
    struct People {
        string name;
        uint256 favNumber;
    }

    People[] public people;

    function store(uint256 _favNumber) public {
        favNumber = _favNumber;
    }

    function retrieve() public view returns (uint256) {
        return favNumber;
    }

    function addPerson(string memory _name, uint256 _favNumber) public {
        people.push(People({favNumber: _favNumber, name: _name}));
    }
}
