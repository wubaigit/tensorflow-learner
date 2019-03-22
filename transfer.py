from keras.models import *
from keras.layers import *
from keras.applications import inception_v3
from keras.applications import xception
from keras.applications.inception_v3 import InceptionV3
from keras.applications.xception import Xception
from keras.preprocessing.image import *

from load_data import load_data

import h5py


def write_gap(MODEL, image_size, lambda_func, train_dir, test_dir):
    width = image_size[0]
    height = image_size[1]
    input_tensor = Input((height, width, 3))
    x = input_tensor
    if lambda_func:
        x = Lambda(lambda_func)(x)

    base_model = MODEL(input_tensor=x, weights='imagenet', include_top=False)
    model = Model(base_model.input, GlobalAveragePooling2D()
                  (base_model.output))

    gen = ImageDataGenerator()
    train_generator = gen.flow_from_directory(train_dir, image_size, shuffle=False,
                                              batch_size=16)
    test_generator = gen.flow_from_directory(test_dir, image_size, shuffle=False,
                                             batch_size=16, class_mode=None)

    train = model.predict_generator(train_generator, train_generator.nb_sample)
    test = model.predict_generator(test_generator, test_generator.nb_sample)
    with h5py.File("gap_%s.h5" % MODEL.func_name) as h:
        h.create_dataset("train", data=train)
        h.create_dataset("test", data=test)
        h.create_dataset("label", data=train_generator.classes)


image_size = 299

(dataset_dir, train_dir, validation_dir, test_dir) = load_data(image_size)

write_gap(InceptionV3, (image_size, image_size),
          inception_v3.preprocess_input, train_dir, test_dir)
write_gap(Xception, (image_size, image_size),
          xception.preprocess_input, train_dir, test_dir)
