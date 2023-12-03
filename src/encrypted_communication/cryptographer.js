const EthCrypto = require('eth-crypto');

async function encrypt(message, public_key){
    const cipher = await EthCrypto.encryptWithPublicKey(
        public_key,
        message
    );
    const cipher_str = EthCrypto.cipher.stringify(cipher);
    return cipher_str
}

async function decrypt(cipher_str, private_key){
    const cipher = EthCrypto.cipher.parse(cipher_str)
    const plain_text_message = await EthCrypto.decryptWithPrivateKey(private_key, cipher);
    return plain_text_message
}
module.exports = {
    encrypt,
    decrypt
}
