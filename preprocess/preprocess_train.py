import bson
import skimage.io
import io
import os

train_file = open('../data/train.bson', 'rb')

train_data = bson.decode_file_iter(train_file)

img_to_cat = {}

index = 0
for key in train_data:
    index += 1
    product_id = key['_id']
    category_id = key['category_id']
    for e, pic in enumerate(key['imgs']):
        picture = skimage.io.imread(io.BytesIO(pic['picture']))
        cat_path = '../data/train/' + str(category_id)
        if not os.path.exists(cat_path):
            os.mkdir(cat_path)
        skimage.io.imsave(cat_path + '/' + str(product_id) + '_' + str(e) + '.jpg', picture)
        if index % 1000 == 0:
            print(index)