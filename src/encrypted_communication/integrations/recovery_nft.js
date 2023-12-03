const { RECOVERY_NFT_CONTRACT_ADDRESS, WEB3_PROVIDER_URL } = require("../constants")

const API_URL = WEB3_PROVIDER_URL

const { createAlchemyWeb3 } = require("@alch/alchemy-web3")
const web3 = createAlchemyWeb3(API_URL)

const contract = require("../../../contracts/ABIs/Recovery_NFT.json")
const nftContract = new web3.eth.Contract(contract.abi, RECOVERY_NFT_CONTRACT_ADDRESS)

async function mintNFT(from_user, to_address, tokenURI) {
    const nonce = await web3.eth.getTransactionCount(from_user.ADDRESS, "latest") //get latest nonce
    console.log(to_address)   
    //the transaction
    const tx = {
        from: from_user.ADDRESS,
        to: RECOVERY_NFT_CONTRACT_ADDRESS,
        nonce: nonce,
        gas: 500000,
        data: nftContract.methods.mintNFT(to_address, tokenURI).encodeABI(),
    }

    const signPromise = web3.eth.accounts.signTransaction(tx, from_user.PRIVATE_KEY)
    signPromise
        .then((signedTx) => {
        web3.eth.sendSignedTransaction(
            signedTx.rawTransaction,
            function (err, hash) {
            if (!err) {
                console.log(
                "The hash of your transaction is: ",
                hash,
                "\nCheck Alchemy's Mempool to view the status of your transaction!"
                )
            } else {
                console.log(
                "Something went wrong when submitting your transaction:",
                err
                )
            }
            }
        )
        })
        .catch((err) => {
        console.log(" Promise failed:", err)
        })
}
module.exports = {mintNFT}