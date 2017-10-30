import torch

class HierarhicalSoftMax:
    def __init__(self, tree):
        self.tree = tree
        
    def softmax(self, part_input):
        max_input = part_input.max()
        sm = torch.exp(part_input - max_input)
        sm = sm / torch.sum(sm)
        return sm
        
    def __forward_one__(self, input, target):
        res = 0
        track = self.tree.get_track_by_code(target)
        for index in range(len(track) - 1):
            parent_node = track[index + 1]
            
            node = track[index]
            node_id = self.tree.get_id_by_name(node['name'])
            
            min_child = parent_node['min_child']
            max_child = parent_node['max_child']
            positive_child = node_id
            part_input = input[min_child - 1:max_child]
            sm = self.softmax(part_input)
        
            res += -torch.log(sm[node_id - min_child])

        return res
    
    def forward(self, input, target):
        res = 0
        for index in range(len(target)):
            res += self.__forward_one__(input[index, :], target[index])
        return torch.mean(res)
    
    def predict(self, input):
        current_id = 0
        prob = 1.0
        while 'min_child' in self.tree[current_id]:
            min_child = self.tree[current_id]['min_child']
            max_child = self.tree[current_id]['max_child']
            
            part_input = input[min_child - 1:max_child]
            sm = self.softmax(part_input)
            val, current_id = sm.max(0)
#             print(val.size())
#             print(current_id.size())
            current_id = current_id.data.numpy()[0]
            
            val = val.data.numpy()[0]
            current_id = current_id + min_child
            prob *= val
#         print(self.tree[current_id], current_id)
        return self.tree[current_id]['code'], prob