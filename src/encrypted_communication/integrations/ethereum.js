const constants = require("../constants")
console.log(constants.WEB3_PROVIDER_URL)

const Web3 = require("web3");
const EthereumTx = require('ethereumjs-tx').Transaction;
const axios = require('axios');
const ethNetwork = constants.WEB3_PROVIDER_URL
const web3 = new Web3(new Web3.providers.HttpProvider(ethNetwork));
 
async function transferFund(sendersData, recieverData, amountToSend, message = undefined) {
    return new Promise(async (resolve, reject) => {
        var nonce = await web3.eth.getTransactionCount(sendersData.address);
        web3.eth.getBalance(sendersData.address, async (err, result) => {
            if (err) {
                return reject();
            }
            let balance = web3.utils.fromWei(result, "ether");
            console.log(balance + " ETH");
            if(balance < amountToSend) {
                console.log('insufficient funds');
                return reject();
            }
   
            let gasPrices = await getCurrentGasPrices();
            
            let details = {
                "to": recieverData.address,
                "value": web3.utils.toHex(web3.utils.toWei(amountToSend.toString(), 'ether')),
                "gas": 51000,
                "gasPrice": gasPrices.low * 1000000000,
                "nonce": nonce,
                "data" : web3.utils.toHex(message),
                "chainId": 4 // EIP 155 chainId - mainnet: 1, rinkeby: 4
            };
            
            const transaction = new EthereumTx(details, {chain: 'ropsten'});
            let privateKey = sendersData.privateKey.split('0x');
            let privKey = Buffer.from(privateKey[1],'hex');
            transaction.sign(privKey);
           
            const serializedTransaction = transaction.serialize();
            web3.eth.sendSignedTransaction('0x' + serializedTransaction.toString('hex'), (err, id) => {
                if(err) {
                    console.log(err);
                    return reject();
                }
                const url = `https://ropsten.etherscan.io/tx/${id}`;
                console.log(url);
                resolve({id: id, link: url});
            });
        });
    });
}

async function getCurrentGasPrices() {
    let response = await axios.get('https://ethgasstation.info/json/ethgasAPI.json');
    let prices = {
      low: response.data.safeLow / 10,
      medium: response.data.average / 10,
      high: response.data.fast / 10
    };
    return prices;
}


module.exports = {transferFund}
