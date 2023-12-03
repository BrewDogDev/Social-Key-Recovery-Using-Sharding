import hashlib
from math import log2
from utils import is_power_of_two

class Merkle_Tree:
    def __init__(self, _dataset):
        self.dataset = _dataset
        self.__build_tree_from_dataset()

    def __build_tree_from_dataset(self):
        self.__setup_leafs()
        #build tree from bottom up
        current_level_nodes = self.leafs
        while len(current_level_nodes) != 1:
            next_level_nodes = []
            for index in range(0, len(current_level_nodes), 2):
                left = current_level_nodes[index]
                right = current_level_nodes[index+1]
                hash = self.hash(left.get_hash() + right.get_hash())
                new_node = Node(hash, left, right)
                next_level_nodes.append(new_node)
            current_level_nodes = next_level_nodes

        self.merkle_root = current_level_nodes[0]
    def __setup_leafs(self):
        #initial leafs
        self.leafs = []
        for item in self.dataset:
            hash = self.hash(item)
            leaf = Node(hash)
            self.leafs.append(leaf)
        #potential bonus leaves if leafs size is not power of 2
        while not is_power_of_two(len(self.leafs)): 
            hash = self.hash(self.dataset[len(self.dataset)-1])#could probably do this a little smarter, but no biggie
            leaf = Node(hash)
            self.leafs.append(leaf)
        self.tree_height = log2(len(self.leafs))


    def hash(self, data):
        result = hashlib.sha3_512(data.encode())
        return result.hexdigest()

    def get_dataset_item(self, index):
        return self.dataset[index]

    def get_merkle_root_hash(self):
        return self.merkle_root.get_hash()

    def __get_proof(self, index, leafs, current_node):
        if current_node.is_leaf():
            return []
        
        left, right = current_node.get_children()
        next_leafs = leafs / 2
        next_index = index % next_leafs
        next_node = left if index < next_leafs else right
        piece_of_proof = right.get_hash() if index < next_leafs else left.get_hash()
        return self.__get_proof(next_index, next_leafs, next_node) + [piece_of_proof]
        # if(current_node.is_leaf()):
        #     return proof

        # left, right = current_node.get_children()
        # if index < leafs/2: #traverse left node
        #     proof.insert(0, right.get_hash())
        #     return self.__get_proof(index % leafs/2, leafs/2, left, proof)
        # else: #traverse right node
        #     proof.insert(0, left.get_hash())
        #     return self.__get_proof(index % leafs/2, leafs/2, right, proof)
    def get_proof(self, index):
        return self.__get_proof(index, 2**self.tree_height, self.merkle_root)
    def get_tree_height(self):
        return self.tree_height
    def __print_tree(self, node, num_tabs):
        tabs = ""
        for _ in range(num_tabs):
            tabs += "\t"
        print(tabs + node.get_hash())
        left, right = node.get_children()
        if not node.is_leaf():
            self.__print_tree(left, num_tabs + 1)
            self.__print_tree(right, num_tabs + 1)

    def print_tree(self):
        self.__print_tree(self.merkle_root, 0)
    


class Node:
    def __init__(self, _hash, _left = None, _right = None):
        self.hash = _hash
        self.left = _left
        self.right = _right
    def get_children(self):
        return (self.left, self.right)
    def get_hash(self):
        return self.hash
    def is_leaf(self):
        return not (self.left and self.right)
