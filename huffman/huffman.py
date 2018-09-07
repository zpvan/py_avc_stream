
class HuffNode():

    def __init__(self, weight = -1, left_node= None, right_node = None):
        self.left_node = left_node
        self.right_node = right_node

        if weight == -1:
            self.weight = left_node.weight + right_node.weight
        else:
            self.weight = weight





class HuffTree():
    
    def __init__(self, sorted_dict):
        
        while len(sorted_dict) > 1:
            (key, value) = sorted_dict.popitem()
            
            
