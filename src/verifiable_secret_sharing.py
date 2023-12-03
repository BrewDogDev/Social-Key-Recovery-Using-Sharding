from timeit import default_timer as timer

import hashlib

from src.biometric_encryption import encrypt, decrypt
from src.shamirs_secret import Shamirs_secret_sharing_setup, reconstruct_shamirs_secret
from src.merkle_tree import Merkle_Tree
from utils import is_even


def initialize(secret, num_shares, min_shares):
    start_SSS = timer()
    SSS = Shamirs_secret_sharing_setup(min_shares, secret)
    shares = [] #strings formatted x,y
    for _ in range(num_shares):
        x, y = SSS.create_share()
        share = f'{x},{y}'
        shares.append(share)
    end_SSS = timer()
    merkle_tree = Merkle_Tree(shares)
    proofs = []
    for index in range(len(shares)):
        proofs.append(merkle_tree.get_proof(index))
    merkle_root = merkle_tree.get_merkle_root_hash()
    end_MT = timer()
    print("time to Initialize SSS:\t", end_SSS - start_SSS)
    print("time to initialize MT: \t", end_MT - end_SSS)
    print("total initialize \t", end_MT-start_SSS)
    return (shares, proofs, merkle_root)

def my_hash(data):
    result = hashlib.sha3_512(data.encode())
    return result.hexdigest()
def validate_share(share, proof, index, merkle_root):
    current_index = index
    current_hash = my_hash(share)
    for hash in proof:
        if is_even(current_index):
            current_hash = my_hash(current_hash + hash)
        else:
            current_hash = my_hash(hash + current_hash)
        current_index //= 2
    return current_hash == merkle_root
def encrypt_shares(shares):
    encrypted_shares = []
    nonces = []
    for share in shares:
        nonce, cipher_text = encrypt(share)
        encrypted_shares.append(cipher_text)
        nonces.append(nonce)
    return encrypted_shares, nonces
def decrypt_shares(encrypted_shares, nonces):
    decrypted_shares = []
    for encrypted_share, nonce in zip(encrypted_shares, nonces):
        decrypted_shares.append(decrypt(nonce, encrypted_share))
    return decrypted_shares

def end_to_end(secret, num_shares, min_shares):
    shares, proofs, merkle_root = initialize(secret, num_shares, min_shares)
    encrypted_shares, nonces = encrypt_shares(shares)
    ########################## distribute ###############################
    ##########################   reclaim  ###############################
    decrypted_shares = decrypt_shares(encrypted_shares, nonces)
    points = []
    for index in range(len(decrypted_shares)):
        share = decrypted_shares[index]
        proof = proofs[index]
        xy = share.split(",")
        x = int(xy[0])
        y = int(xy[1])
        points.append((x, y))
        valid = validate_share(share, proof, index, merkle_root)
    reconstructed_secret = reconstruct_shamirs_secret(points[:min_shares])
    print("Secret Properly Reconstructed:", secret == reconstructed_secret)


if __name__ == "__main__":
    secret = 1010101010101010
    num_shares = 2
    min_shares = num_shares//2 + 1
    while num_shares < 10:
        print(f"Trial-----num_shares:{num_shares}-----min_shares:{min_shares}")
        end_to_end(secret, num_shares, min_shares)
        num_shares += 1
        min_shares = num_shares//2 + 1
