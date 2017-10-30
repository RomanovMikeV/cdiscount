index = -1
nodes = []
name_to_index = {}

for depth in range(3):
    fin = open("../data/category_names.csv")

    next(fin)

    for line in fin:
        s_line = line[:-1].split(',')
        s_line[3] = ','.join(s_line[3:])
        s_line = s_line[:4]
        
        track = s_line[1:]
        class_code = s_line[0]
         
        if class_code == '1000015309':
            print(line)

        node = track[depth]
        if node not in name_to_index:
            if class_code == '1000015309':
                print(line)

            index += 1
            name_to_index[node] = index
                
            parent_index = None
            if depth == 0:
                parent_index = -1
            else:
                parent_name = track[depth - 1]
                parent_index = name_to_index[parent_name]
            to_append = {'name': node, 'parent': parent_index}
            if depth == 2:
                to_append['code'] = class_code
            nodes.append(to_append)
    fin.close()
    
fout = open('../data/tree.csv', 'w+')

for node in nodes:
    if 'code' in node:
        fout.write(node['name'] + ';' + str(node['parent']) + ';' + node['code'] + '\n')
    else:
        fout.write(node['name'] + ';' + str(node['parent']) + '\n')
    
fout.close()
