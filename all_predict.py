import os
from PIL import Image
from keras.preprocessing import image
from keras.models import load_model
import numpy as np
from keras.applications.inception_v3 import preprocess_input

def currify_predict(model, target_size, real_val):
  def predict(img_path):
    """Run model prediction on image
    Args:
      model: keras model
      img: PIL format image
      target_size: (w,h) tuple
    Returns:
      list of predicted labels and their probabilities
    """
    img = Image.open(img_path)
    if img.size != target_size:
      img = img.resize(target_size)

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    if preds[0][0] > preds[0][1]:
      return 0 == real_val
    else:
      return 1 == real_val
  return predict

def walk(path, callback):
  all_length = len(os.listdir())
  acc = 0
  for fpath, _, file_list in os.walk(path):
    for file_name in file_list:
      print('path:', path)
      path = os.path.join(fpath, file_name)
      res = callback(path)
      print('res:', res)
      if res:
        acc += 1
  print('all:', all_length)
  print('acc:', acc)

target_size = (299, 299)

current_dir = os.path.dirname(__file__)
dataset = os.path.join(current_dir, 'dataset')
test = os.path.join(dataset, 'test')
first_scan_test = os.path.join(test, 'first-scan')
second_scan_test = os.path.join(test, 'second-scan')

model_path = os.path.join(current_dir, 'inceptionv3-ft-622.model')
model = load_model(model_path)

walk(first_scan_test, currify_predict(model, target_size, 0))