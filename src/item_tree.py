class ItemTree:
    def __init__(self, source_file_name):
        fin = open(source_file_name)
        
        self.__tree__ = [{'name': 'root', 'parent': -1, 'children': []}]
        self.__name_to_index__ = {'root': 0}
        self.__code_to_index__ = {}
        index = 1
        
        for line in fin:
            if len(line) == 0:
                break
            s_line = line[:-1].split(';')
            name = s_line[0]
            parent = int(s_line[1]) + 1
            to_append = {'name': name, 'parent': parent, 'children': []}
            if len(s_line) > 2:
                to_append['code'] = int(s_line[2])
                self.__code_to_index__[int(s_line[2])] = index
            self.__tree__.append(to_append)
            self.__name_to_index__[name] = index
            if parent >= 0:
                self.__tree__[parent]['children'].append(index)
            
            index += 1
            
        fin.close()
        
        for index in range(len(self.__tree__)):
            node = self.__tree__[index]
            if len(node['children']) > 0:
                node['max_child'] = max(node['children'])
                node['min_child'] = min(node['children'])
        
    def __len__(self):
        return len(self.__tree__)
    
    def get_id_by_name(self, name):
        return self.__name_to_index__[name]
    
    def get_id_by_code(self, code):
        return self.__code_to_index__[code]
    
    def get_track(self, node_id):
        track = []
        
        current_id = node_id
        
        while current_id >= 0:
            track.append(self.__tree__[current_id])
            current_id = self.__tree__[current_id]['parent']
        
        return track
    
    def get_track_by_name(self, node_name):
        return self.get_track(self.get_id_by_name(node_name))
    
    def get_track_by_code(self, node_code):
        return self.get_track(self.get_id_by_code(node_code))
    
    def __getitem__(self, index):
        return self.__tree__[index]