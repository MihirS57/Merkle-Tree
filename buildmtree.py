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
    print(f'Adding additional dummy data of {remain} size')
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

    
print('Enter words separated using commas (for eg: your input can be /[mihir,shah,viterbi,csci/]> ): ')
value_input = sys.argv[1]
value_input = value_input[1:len(value_input)-1]
value_list = value_input.split(",")
print(f'Original Data: {value_list}')
value_list = adjustDataItems(len(value_list),value_list)

print(f'Building a merkle tree based on {value_list}')
tree_list = buildMerkleTree(value_list)[::-1]
json_list = []
bfs(tree_list[0],[])
json_object = json.dumps(json_list, indent=4)
with open("merkle.tree", "w") as tree_file:
    tree_file.write(json_object)

