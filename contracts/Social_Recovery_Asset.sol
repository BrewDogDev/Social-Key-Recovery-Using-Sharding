pragma solidity ^0.8.7;
// SPDX-License-Identifier: GPL-3.0

import "./Recoverable_Asset.sol";

//Constants
string constant recovery_pre_configured = "Recovery has already been configured";


abstract contract Social_Recovery_Asset is Recoverable_Asset(){
    //Data
    struct Recovery_Congiguration{
        address recovery_address;
        string merkle_root_of_shards;
        bool initialized;
    }
    mapping(address => Recovery_Congiguration) recovery_configurations;

    //Events
    event recovery_configured(address recoverable, Recovery_Congiguration config);
    event assets_recovered(address recovered, address recovering);

    //modifiers
    modifier verify_recovery(address recovered){
        require(recovery_configurations[recovered].initialized);

        address recovery_address = recovery_configurations[recovered].recovery_address;
        require(msg.sender == recovery_address);
        _;
    }


    //API
    function configure_recovery(address _recovery_address, string calldata _merkle_root_of_shards)external {
        require(!recovery_configurations[msg.sender].initialized, recovery_pre_configured);
        
        Recovery_Congiguration storage config = recovery_configurations[msg.sender];
        
        config.recovery_address = _recovery_address;
        config.merkle_root_of_shards = _merkle_root_of_shards;
        config.initialized = true;

        emit recovery_configured(msg.sender, config);
    }
    //Parent


    //Internals
}