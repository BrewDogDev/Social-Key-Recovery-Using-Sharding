import unittest
import random
from src.shamirs_secret import reconstruct_shamirs_secret, Shamirs_secret_sharing_setup

DEFAULT_SECRET = 99999999999998999999999998899999999999999999999999899999999999999999


class Shard_test(unittest.TestCase):
    def __test_with(self, min_shares, num_shares, expected_secret=DEFAULT_SECRET):
        SSS = Shamirs_secret_sharing_setup(min_shares, expected_secret)
        shares = []
        for i in range(num_shares):
            share = SSS.create_share()
            shares.append(share)
        actual_secret = reconstruct_shamirs_secret(
            random.sample(shares, min_shares))
        self.assertEqual(expected_secret, actual_secret,
                         'Reconstructed Secret did not match')

    def test_2_shares_min(self):
        self.__test_with(2, 2)

    def test_3_shares_min(self):
        self.__test_with(3, 3)

    def test_4_shares_min(self):
        self.__test_with(4, 5)

    def test_5_shares_min(self):
        self.__test_with(5, 10)

    def test_10_shares_min(self):
        self.__test_with(10, 100)

    def test_with_small_secret(self):
        self.__test_with(10, 100, 2)

    def test_with_huge_secret(self):
        self.__test_with(10, 100, 2**1080)

    # #this one take along time to compute so comment out
    # def test_with_100_shares_min_secret(self):
    #     self.__test_with(100, 200)


if __name__ == '__main__':
    unittest.main()
