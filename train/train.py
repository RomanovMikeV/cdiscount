import sys
import torch
import torch.utils.data
import torchvision

# Мои библиотеки
sys.path.append('../src/')
import item_tree
import softmax_tree
import dataset

batch_size = 8

tree = item_tree.ItemTree('../data/tree.csv')

train_dataset = dataset.ItemDataset('../data', 
                                    mode='train',
                                    transforms=torchvision.transforms.Compose([
                                        torchvision.transforms.Scale(224),
                                        torchvision.transforms.CenterCrop(224),
                                        torchvision.transforms.ToTensor()
                                    ]))

valid_dataset = dataset.ItemDataset('../data', 
                                    mode='valid',
                                    transforms=torchvision.transforms.Compose([
                                        torchvision.transforms.Scale(224),
                                        torchvision.transforms.CenterCrop(224),
                                       torchvision.transforms.ToTensor()
                                    ]))

train_loader = torch.utils.data.DataLoader(train_dataset,
                                           batch_size=batch_size,
                                           shuffle=True,
                                           num_workers=4)

valid_loader = torch.utils.data.DataLoader(valid_dataset,
                                           batch_size=batch_size,
                                           shuffle=True,
                                           num_workers=4)


model = torchvision.models.resnet101(pretrained=True)
model.fc = torch.nn.Linear(2048, len(tree))
model.cuda()
model.eval()

criterion = softmax_tree.HierarhicalSoftMax(tree)
# print(model)

preoptimizer = torch.optim.Adam(model.fc.parameters(), lr=1.0e-5)
optimizer = torch.optim.Adam(model.parameters(), lr=1.0e-5)





# Скрипт обучения (с параллельной валидацией)
for batch, target in train_loader:
    preoptimizer.zero_grad()
    valid_loss = 0.0
    for valid_batch, valid_target in valid_loader:
        valid_batch = torch.autograd.Variable(valid_batch).cuda()
        out = model.forward(valid_batch)
        
        valid_loss = criterion.forward(out, valid_target)
        break
    
    batch = torch.autograd.Variable(batch).cuda()
    out = model.forward(batch)
    
    loss = criterion.forward(out, target)
    loss.backward()
    
    preoptimizer.step()
    print(loss.data[0], valid_loss.data[0])
