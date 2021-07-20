import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

def Currency(image)
    np.set_printoptions(suppress=True)

    # Load the model
    model = tensorflow.keras.models.load_model('Keras//keras_model.h5', compile=False)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)


    # resizing the image to be at least 224x224
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model(data)
    tensor_array = prediction.numpy()
    tensor_max = np.max(tensor_array)
    Index = np.where(tensor_array == tensor_max)

    with open('labels.txt', 'r') as f:
        labels = [line.strip() for i, line in enumerate(f.readlines())]
    return (labels[int(Index[1])])