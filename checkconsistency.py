from hashlib import sha256
import json
import sys

class MerkleTreeObj:
    def __init__(self,data,hash_value):
        self.left = None
        self.right = None
        self.data = data
        self.hash_value = hash_value

def adjustDataItems(size,value_list):
    i = 2
    power = 0
    while pow(i,power) < size:
        power+=1
    remain =  pow(i,power) - size
    if remain == 0:
        return value_list
    # print(f'Adding additional dummy data of {remain} size')
    if remain % 2 == 1:
        for i in range(0,remain):
            value_list.append(value_list[size-1])
    else:
        for i in range(size-remain,size):
            value_list.append(value_list[i])
    return value_list
        
def buildMerkleTree(value_list):
    num_nodes = len(value_list)
    nodes_list = []
    for ind in range(num_nodes):
        nodes_list.append(MerkleTreeObj(value_list[ind],
        sha256(value_list[ind].encode('utf-8')).hexdigest()))
    i = 0
    while i < num_nodes:
        if i+1 < num_nodes:
            node_left = nodes_list[i]
            node_right = nodes_list[i+1]
            concat_val = node_left.hash_value+node_right.hash_value
            parent_hash = MerkleTreeObj(concat_val,sha256(concat_val.encode('utf-8')).hexdigest())
            nodes_list.append(parent_hash)
            parent_hash.left = node_left
            parent_hash.right = node_right
            num_nodes+=1
            i+=2
        else:
            break
    # print(len(nodes_list))
    return nodes_list

def bfs(node,q):
    if node != None:
        # print(node.data)
        q.append(node.left)
        q.append(node.right)
        tree_dic = {
            "parent": {
                "data": node.data,
                "hash": node.hash_value
            },
            "left_child": {
                "data": None if node.left == None else node.left.data,
                "hash": None if node.left == None else node.left.hash_value,
            },
            "right_child": {
                "data": None if node.left == None else node.right.data,
                "hash": None if node.left == None else node.right.hash_value,
            }
        }
        json_list.append(tree_dic)
    while len(q) > 0:
        bfs(q.pop(0),q)
    
def buildAndGenerateFile(value_list_1, value_list_2):
    global json_list
    
    tree_list_1 = buildMerkleTree(value_list_1)[::-1]
    tree_list_2 = buildMerkleTree(value_list_2)[::-1]
    tree_data = {}
    bfs(tree_list_1[0],[])
    tree_data = {
        "Tree 1": json_list,
        "Tree 2": []
    }
    json_list = []
    bfs(tree_list_2[0],[])
    tree_data["Tree 2"] = json_list
    json_object = json.dumps(tree_data, indent=4)
    with open("merkle.trees", "w") as tree_file:
        tree_file.write(json_object)

def buildTreeFromFile():
    map1 = {}
    map2 = {}
    tree_file = open('merkle.trees')
    tree_data = json.load(tree_file)
    root1 = None
    root2 = None
    tree1_data = tree_data["Tree 1"]
    tree2_data = tree_data["Tree 2"]
    
    for item in tree1_data:
        parent = item["parent"]
        map1[parent["data"]] = MerkleTreeObj(parent["data"],parent["hash"])
    for item in tree1_data:
        parent = item["parent"]
        if root1 is None:
            root1 = map1[parent["data"]]
        left_val = item["left_child"]
        right_val = item["right_child"]
        map1[parent["data"]].left = map1[left_val["data"]] if left_val["data"] != None else None
        map1[parent["data"]].right = map1[right_val["data"]] if right_val["data"] != None else None
    
    for item in tree2_data:
        parent = item["parent"]
        map2[parent["data"]] = MerkleTreeObj(parent["data"],parent["hash"])
    for item in tree2_data:
        parent = item["parent"]
        if root2 is None:
            root2 = map2[parent["data"]]
        left_val = item["left_child"]
        right_val = item["right_child"]
        map2[parent["data"]].left = map2[left_val["data"]] if left_val["data"] != None else None
        map2[parent["data"]].right = map2[right_val["data"]] if right_val["data"] != None else None
    return root1,root2

def checkConsistency(nodes_list_1,nodes_list_2):
    for idx,node in enumerate(nodes_list_1):
        if idx >= og_size:
            break
        if node != nodes_list_2[idx]:
            return []
    
    root1,root2 = buildTreeFromFile()
    if root1.hash_value == root2.hash_value:
        print("Same tree")
        return [root2.hash_value]
    
    parentNodes = []
    leftChilds = []
    rightChilds = []
    queue = []
    queue.append(root2)
    while len(queue) > 0:
        temp_root = queue.pop(0)
        if temp_root.left != None and temp_root.right != None:
            parentNodes.append(temp_root)
            leftChilds.append(temp_root.left)
            rightChilds.append(temp_root.right)
            queue.append(temp_root.left)
            queue.append(temp_root.right)
      
    op = []
    ogHashExists = False
    for i in range(len(parentNodes)):
        if root1.hash_value == parentNodes[i].hash_value:
            ogHashExists = True
            break
    right_sibling = ''
    if ogHashExists:
        op.append(root1.hash_value)
        values = []    
        combinedHash = ''
        left_child = root1.hash_value
        while combinedHash != root2.hash_value:
            for idx,left_node in enumerate(leftChilds):
                if left_child == left_node.hash_value:
                    right_sibling = rightChilds[idx].hash_value
                    values.append(right_sibling)
                    break
            combinedValue = left_child+right_sibling
            combinedHash = sha256(combinedValue.encode('utf-8')).hexdigest()
            left_child = combinedValue
        
        op+=values
        op.append(combinedHash)
    else:
        values = []
        leftChildExists = False
        combinedHash = ''
        for node in parentNodes:
            if root1.left.hash_value == node.hash_value:
                values.append(root1.left.hash_value)
                leftChildExists = True
                break
        if not leftChildExists:
            return []
        combinedHash = root1.left.hash_value
        while combinedHash != root2.hash_value:
            for idx,left_node in enumerate(leftChilds):
                if combinedHash == left_node.hash_value:
                    right_sibling = rightChilds[idx].hash_value
                    values.append(right_sibling)
                    break
            combinedHash = combinedHash+right_sibling
            combinedHash = sha256(combinedHash.encode('utf-8')).hexdigest()
        op+=values
        op.append(combinedHash)
    return op         
    
value_input_1 = sys.argv[1]
value_input_2 = sys.argv[2]
json_list = []
value_list_1 = value_input_1[1:len(value_input_1)-1].split(",")
value_list_2 = value_input_2[1:len(value_input_2)-1].split(",")
og_size = len(value_list_1)
value_list_1 = adjustDataItems(len(value_list_1),value_list_1)
value_list_2 = adjustDataItems(len(value_list_2),value_list_2)
buildAndGenerateFile(value_list_1,value_list_2)
op = checkConsistency(value_list_1,value_list_2)
root1,root2 = buildTreeFromFile()
if len(op) > 0 and op[len(op)-1] == root2.hash_value:
    print(f'New Tree Root: {root2.hash_value}')
    print(f'yes {op}')
else:
    print("no")
