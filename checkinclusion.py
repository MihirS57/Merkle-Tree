from hashlib import sha256
import json

class MerkleTreeObj:
    def __init__(self,data):
        self.left = None
        self.right = None
        self.data = data

def buildTreeFromFile():
    map = {}
    tree_file = open('merkle.tree')
    tree_data = json.load(tree_file)
    root = None
    for item in tree_data:
        parent = item["parent"]
        map[parent] = MerkleTreeObj(parent)
    for item in tree_data:
        parent = item["parent"]
        if root is None:
            root = map[parent]
        left_val = item["left_child"]
        right_val = item["right_child"]
        map[parent].left = map[left_val] if left_val != None else None
        map[parent].right = map[right_val] if right_val != None else None
    return root

def checkInclusion(temp_root,searchItem):
    if temp_root.left == None and temp_root.right == None:
        if temp_root.data == searchItem:
            return True
        else:
            return False
    
    respLeft = checkInclusion(temp_root.left,searchItem)
    respRight = checkInclusion(temp_root.right,searchItem)

    if respLeft == False and respRight:
        if temp_root.left.data not in hash_set:
            hash_set.add(temp_root.left.data)
            hash_list.append(temp_root.left.data)
    elif respLeft and respRight == False:
        if temp_root.right.data not in hash_set:
            hash_set.add(temp_root.right.data)
            hash_list.append(temp_root.right.data)
    elif respLeft and respRight:
        if temp_root.left.data not in hash_set:
            hash_set.add(temp_root.left.data)
            hash_list.append(temp_root.left.data)
    return respLeft or respRight


hash_set = set()
hash_list = []
tree_root = buildTreeFromFile()
print(tree_root.data)
print(checkInclusion(tree_root,"mihir"),hash_list)