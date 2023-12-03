pragma solidity ^0.8.7;
// SPDX-License-Identifier: GPL-3.0

abstract contract Recoverable_Asset{
    ///@notice assets associated with "recovered" address will be sent to "recovering" address
    function Recover_Assets(address recovered, address recovering)external virtual returns(bool success);
}