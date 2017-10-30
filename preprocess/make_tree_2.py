import collections

fin = open('../data/category_names.csv')

tree = {'root_0': {'children': []}}
next(fin)
for line in fin:
    s_line = line[:-1].split(',')
    s_line[3] = ','.join(s_line[3:])
    s_line = s_line[:4]
    
    track = s_line[1:]
    class_code = s_line[0]
    
    #if class_code == "1000006131":
    #    print(s_line)
    
    for depth in range(len(track)):
        name = track[depth] + '_' + str(depth + 1)
        if depth == len(track) - 1:
            name = track[depth] + '_' + class_code
        parent = 'root_0'
        if depth > 0.1:
            parent = track[depth - 1] + '_' + str(depth)
        tree[name] = {'parent': parent}
        
        if depth == len(track) - 1:
            tree[name]['code'] = class_code
     #       if class_code == "1000006131":
     #           print(tree[name], name)

#print(tree['FUSIBLE_3'], '<- check')
for key in tree.keys():
    if 'code' in tree[key]:
        if tree[key]['code'] == '1000006131':
            print(tree[key], key)
    if 'parent' in tree[key]:
        parent = tree[key]['parent']
        if 'children' not in tree[parent]:
            tree[parent]['children'] = []
        tree[parent]['children'].append(key)
        
current_node = tree['root_0']

print_order = []
node_to_index = {}

to_scan = collections.deque()
to_scan.append('root_0')

while True:
    if len(to_scan) > 0:
        scanning = to_scan.popleft()
        print_order.append(scanning)
        if "children" in tree[scanning]:
            for child in tree[scanning]["children"]:
                to_scan.append(child)
    else:
        break
        
#print(len(print_order))
#print(print_order[0])

for index in range(len(print_order)):
    node_to_index[print_order[index]] = index

#print(tree['root_0'])
#print(tree['ART DE LA TABLE - ARTICLES CULINAIRES_1'])

#print(print_order[:100])
to_print = []
for name in print_order[1:]:
    #print(name)
    parent = tree[name]['parent']
    #print(node_to)
    out_name = name.replace('\n', '')
    one_line = [out_name, str(node_to_index[parent] - 1)]
    #fout.write(out_name + ',' + str(node_to_index[parent] - 1))
    if 'code' in tree[name]:
        one_line.append(str(tree[name]['code']))
    one_line = ';'.join(one_line)
    to_print.append(one_line)
    #fout.write('\n')
    
fout = open('../data/tree.csv', 'w+')
fout.write('\n'.join(to_print))
fout.write('\n')
fout.close()
#while True:
#fout = open('../data/tree.csv', 'w+')
#def print_tree(tree, root, index):
#    if 'children' in tree[root]:
#        for child in tree[root]['children']:
#            fout.write(child + ',' + str(index) + '\n')