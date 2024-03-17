from hashlib import sha256
import json

class MerkleTreeObj:
    def __init__(self,data,hash_value):
        self.left = None
        self.right = None
        self.data = data
        self.hash_value = hash_value

def buildTreeFromFile():
    map = {}
    tree_file = open('merkle.tree')
    tree_data = json.load(tree_file)
    root = None
    for item in tree_data:
        parent = item["parent"]
        map[parent["data"]] = MerkleTreeObj(parent["data"],parent["hash_value"])
    for item in tree_data:
        parent = item["parent"]
        if root is None:
            root = parent
        left_val = item["left_child"]
        right_val = item["right_child"]
        map[parent["data"]].left = map[left_val["data"]] if left_val != None else None
        map[parent["data"]].right = map[right_val["data"]] if right_val != None else None
    return root

tree_root = buildTreeFromFile()