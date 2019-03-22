"""
数据预处理:
将数据输入神经网络前，应该讲数据格式化为经过预处理的浮点数张量

二分类问题：
最后一层激活函数为 sigmoid，
损失函数：binary_crossentropy
"""

from keras.preprocessing.image import ImageDataGenerator
from load_data import load_data

image_size = 299
batch_size = 20


def train():
    (dataset_dir, train_dir, validation_dir, test_dir) = load_data(image_size)

    train_datagen = ImageDataGenerator(rescale=1./255)
    test_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(image_size, image_size),
        batch_size=batch_size,
        class_mode='binary'
    )

    validation_generator = test_datagen.flow_from_directory(
        validation_dir,
        target_size=(image_size, image_size),
        batch_size=batch_size,
        class_mode='binary'
    )
