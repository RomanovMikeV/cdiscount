import bson
import skimage.io
import io
import os

test_file = open('../data/test.bson', 'rb')

test_data = bson.decode_file_iter(test_file)

img_to_cat = {}

index = 0
for key in test_data:
    index += 1
    product_id = key['_id']
    for e, pic in enumerate(key['imgs']):
        picture = skimage.io.imread(io.BytesIO(pic['picture']))
        cat_path = '../data/test/'
        skimage.io.imsave(cat_path + str(product_id) + '_' + str(e) + '.jpg', picture)
        if index % 1000 == 0:
            print(index)