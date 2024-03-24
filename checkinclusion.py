from hashlib import sha256
import json
import sys

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
        map[parent["data"]] = MerkleTreeObj(parent["data"],parent["hash"])
    for item in tree_data:
        parent = item["parent"]
        if root is None:
            root = map[parent["data"]]
        left_val = item["left_child"]
        right_val = item["right_child"]
        map[parent["data"]].left = map[left_val["data"]] if left_val["data"] != None else None
        map[parent["data"]].right = map[right_val["data"]] if right_val["data"] != None else None
    return root

def checkInclusion(temp_root,searchItem):
    global proveInclusion
    if temp_root.left == None and temp_root.right == None:
        if temp_root.data == searchItem:
            return True
        else:
            return False
    
    respLeft = checkInclusion(temp_root.left,searchItem)
    respRight = checkInclusion(temp_root.right,searchItem)

    if respLeft == False and respRight:
        if temp_root.left.hash_value not in hash_set:
            hash_set.add(temp_root.left.hash_value)
            hash_list.append(temp_root.left.hash_value)
            proveInclusion = sha256((temp_root.left.hash_value+proveInclusion).encode('utf-8')).hexdigest()
    elif respLeft and respRight == False:
        if temp_root.right.hash_value not in hash_set:
            hash_set.add(temp_root.right.hash_value)
            hash_list.append(temp_root.right.hash_value)
            proveInclusion = sha256((proveInclusion+temp_root.right.hash_value).encode('utf-8')).hexdigest()
    elif respLeft and respRight:
        if temp_root.left.hash_value not in hash_set:
            hash_set.add(temp_root.left.hash_value)
            hash_list.append(temp_root.left.hash_value)
            proveInclusion = sha256((temp_root.left.hash_value+proveInclusion).encode('utf-8')).hexdigest()
    return respLeft or respRight

searchItem = sys.argv[1]
hash_set = set()
hash_list = []
proveInclusion = sha256(searchItem.encode('utf-8')).hexdigest();
tree_root = buildTreeFromFile()
searchResults = checkInclusion(tree_root,searchItem)
if searchResults and tree_root.hash_value == proveInclusion:
    print(f'yes {hash_list}')
else:
    print("No")