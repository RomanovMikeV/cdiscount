import os
import pickle
import torch
import torchvision

class ItemDataset(torch.utils.data.Dataset):
    def __init__(self, data_dir, 
                 valid_frac=0.1, 
                 mode='train', 
                 transforms=torchvision.transforms.ToTensor()):
        self.train_dir = data_dir + '/train'
        self.transforms = transforms
        
        self.train_images = []
        self.valid_images = []
        
        self.dataset_file = 'item_dataset_index.pickle'
        
        dataset = None
        no_index = False
        if os.path.exists(self.dataset_file):
            with open(self.dataset_file, 'rb') as fin:
                dataset = pickle.load(fin)
                if dataset['valid_frac'] != valid_frac or dataset['data_dir'] != data_dir:
                    no_index = True
                else:
                    self.train_images = dataset['train_images']
                    self.valid_images = dataset['valid_images']
                    self.class_to_num = dataset['class_to_num']
                
        else:
            no_index = True
            
        if no_index:
            self.class_to_num = {}
            class_index = 0
            for category in os.listdir(self.train_dir):
                cat_images = 0
                for img in os.listdir(self.train_dir + '/' + category):
                    cat_images += 1
            
                image_index = 0
                train_threshold = int((1.0 - valid_frac) * float(cat_images))
            
                for img in os.listdir(self.train_dir + '/' + category):
                    if image_index >= train_threshold:
                        self.valid_images.append(self.train_dir + 
                                                 '/' + category + 
                                                 '/' + img)
                    else:
                        self.train_images.append(self.train_dir + 
                                                 '/' + category + 
                                                 '/' + img)
                    image_index += 1
                self.class_to_num[category] = class_index
                class_index += 1
#             print(image_index, '<- Image Index')
            to_save = {'valid_frac': valid_frac,
                       'data_dir': data_dir,
                       'train_images': self.train_images,
                       'valid_images': self.valid_images,
                       'class_to_num': self.class_to_num}
            
            with open(self.dataset_file, 'wb+') as fout:
                pickle.dump(to_save, fout)
        if mode == 'train':
            self.images = self.train_images
        elif mode == 'valid':
            self.images = self.valid_images
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, index):
        image_path = self.images[index]
        image_class = image_path.split('/')[-2] 
        img = torchvision.transforms.Image.open(image_path)
        #print(img.size)
        img = self.transforms(img.convert('RGB'))
        #print(image_class)
        return img, int(image_class)