const constants = require("./constants")
const ethereum = require("./integrations/ethereum")
const recovery_nft = require("./integrations/recovery_nft")
const cryptographer = require("./cryptographer")

async function black_hole_communication(from_user, to_user, message){
    cipher_str = await cryptographer.encrypt(message, to_user.PUBLIC_KEY)
    ethereum.transferFund({address: from_user.ADDRESS, privateKey: from_user.PRIVATE_KEY }, {address: constants.USERS.ZERO.ADDRESS}, 0, cipher_str)
    msg = await cryptographer.decrypt(cipher_str, to_user.PRIVATE_KEY)
    console.log(msg)
}

async function user_to_user_communication(from_user, to_user, message){
    cipher_str = await cryptographer.encrypt(message, to_user.PUBLIC_KEY)
    ethereum.transferFund({address: from_user.ADDRESS, privateKey: from_user.PRIVATE_KEY }, {address: to_user.ADDRESS}, 0, cipher_str)
    msg = await cryptographer.decrypt(cipher_str, to_user.PRIVATE_KEY)
    console.log(msg)
}

async function nft_communication(from_user, to_user, token_uri){
    //file must be uploaded to IPFS (use pinata)
    recovery_nft.mintNFT(from_user, to_user.ADDRESS, token_uri)
}

module.exports = {
    black_hole_communication,
    user_to_user_communication,
    nft_communication
}

