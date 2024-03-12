from hashlib import sha256

class MerkleTreeObj:
    def _init_(self,data):
        self.left = None
        self.right = None
        self.data = data
        self.hash_value = sha256(data.encode('utf-8')).hexdigest()

def buildMerkleTree(value_list):
    num_nodes = len(nodes_list)
    nodes_list = []
    for i in range(num_nodes,2):
        if i+1 >= num_nodes:
            


value_input = input('Enter words separated using commas: ')
value_list = value_input.split(",")
print(f'Building a merkle tree based on {value_list}')
