from hashlib import sha256

class MerkleTreeObj:
    def __init__(self,data):
        self.left = None
        self.right = None
        self.data = data
        self.hash_value = sha256(data.encode('utf-8')).hexdigest()
        
def buildMerkleTree(value_list):
    num_nodes = len(value_list)
    nodes_list = []
    for ind in range(num_nodes):
        nodes_list.append(MerkleTreeObj(value_list[ind]))
    i = 0
    while i < num_nodes:
        if i+1 < num_nodes:
            node_left = nodes_list[i]
            node_right = nodes_list[i+1]
            parent_hash = MerkleTreeObj(node_left.hash_value+node_right.hash_value)
            nodes_list.append(parent_hash)
            parent_hash.left = node_left
            parent_hash.right = node_right
            num_nodes+=1
            i+=2
        else:
            break
    print(len(nodes_list))
    return nodes_list

def bfs(node,q,tree_file):
    if node != None:
        print(node.data)
        q.append(node.left)
        q.append(node.right)
        tree_file.write(f'Parent = {node.data}\n')
        if node.left != None:
            tree_file.write(f'Left Child = {node.left.data} - Parent = {node.data}\n')
        if node.right != None:
            tree_file.write(f'Right Child = {node.right.data} - Parent = {node.data}\n')
    while len(q) > 0:
        bfs(q.pop(0),q,tree_file)

    

value_input = input('Enter words separated using commas: ')
value_list = value_input.split(",")
if len(value_list) % 2 == 1:
    value_list.append(value_list[len(value_list)-1])
print(f'Building a merkle tree based on {value_list}')
tree_list = buildMerkleTree(value_list)[::-1]
for node in tree_list:
    print(node.data)
tree_file = open("merkle.tree", "w")
bfs(tree_list[0],[],tree_file)
tree_file.close()

