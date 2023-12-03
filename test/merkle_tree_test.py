from utils import is_even
import unittest
from src.merkle_tree import Merkle_Tree



class Merkle_Tree_Test(unittest.TestCase):
    def __test_with(self, dataset):
        merkle_tree = Merkle_Tree(dataset)
        self.__check_dataset(dataset, merkle_tree)
        self.__check_proofs(dataset, merkle_tree)


    def __check_dataset(self, dataset, merkle_tree):
        for index in range(len(dataset)):
            self.assertEqual(dataset[index], merkle_tree.get_dataset_item(index),
                'dataset item {index} did not match, value: {dataset[i]}')
    def __check_proofs(self, dataset, merkle_tree):
        for index in range(len(dataset)):
            self.__validate_proof(index, merkle_tree)

    def __validate_proof(self, dataset_index, merkle_tree):
        dataset_item = merkle_tree.get_dataset_item(dataset_index)
        proof = merkle_tree.get_proof(dataset_index)

        current_index = dataset_index
        current_hash = merkle_tree.hash(dataset_item)
        for hash in proof:
            if is_even(current_index):
                current_hash = merkle_tree.hash(current_hash + hash)
            else:
                current_hash = merkle_tree.hash(hash + current_hash)
            current_index //= 2
        self.assertEqual(current_hash, merkle_tree.get_merkle_root_hash())

    def test_2_items(self):
        dataset = ["0", "1"]
        self.__test_with(dataset)     
    def test_4_items(self):
        dataset = ["0", "1", "2", "3"]
        self.__test_with(dataset)
    def test_8_items(self):
        dataset = ["0", "1", "2", "3", "4", "5", "6", "7"]
        self.__test_with(dataset)
    def test_16_items(self):
        dataset = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]
        self.__test_with(dataset)
    def test_128_items(self):
        dataset = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
                   "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
                   "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
                   "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
                   "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
                   "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
                   "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
                   "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
        ]
        self.__test_with(dataset)
    
    def test_3_items(self):
        dataset = ["0", "1", "2"]
        self.__test_with(dataset)
    def test_7_items(self):
        dataset = ["0", "1", "2", "3", "4", "5", "6", "7"]
        self.__test_with(dataset)
    def test_15_items(self):
        dataset = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]
        self.__test_with(dataset)
    def test_17_items(self):
        dataset = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16"]
        self.__test_with(dataset)
    def test_65_items(self):
        dataset = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
                   "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
                   "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
                   "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
                   "65"
        ]
        self.__test_with(dataset)

    


if __name__ == '__main__':
    unittest.main()
