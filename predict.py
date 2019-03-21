from PIL import Image

from keras.models import load_model
from keras.preprocessing import image
from keras.applications.inception_v3 import preprocess_input


target_size = (299, 299)

def predict(model, img, target_size):
  """Run model prediction on image
  Args:
    model: keras model
    img: PIL format image
    target_size: (w, h) tuple
  Returns:
    list of predicted lablels and their probabilities
  """
  if img.size != target_size:
      img = img.resize(target_size)
  
  
  