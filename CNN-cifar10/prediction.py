import os
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model
 

CATEGORIES = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']


def load_image(filename):
    """
    Load image and prepare it to prediction.
    Argument:
        filename (str): path to image file.
    Return:
        img (ndarray): Normalized image, prepare to prediction.
    """
    # Load and prepare image to evaluate.
    img = load_img(filename, target_size=(32, 32))
    img = img_to_array(img)
    img = img.reshape(1, 32, 32, 3)
    img = img.astype('float32')
    img = img / 255
    return img
 

def prediction(model, filename):
    """
    Make Prediction of the image based on model.h5 model.
    Argument:
        filename (str): path to image file.
    Return:
        Prediction (str): Prediction of the given model.
    """
    # Load model, image and make prediction.
    img = load_image(filename)
    model = load_model(model)
    result = model.predict(img)
    return result[0]

def print_res(result):
    max_res = result.argmax()
    for i in range(len(CATEGORIES)):
        print(">", end=" ") if i == max_res else print(" ", end=" ")
        print(f"{CATEGORIES[i]}: {round(result[i]*100, 2)}%")
    print(f"Result: {CATEGORIES[max_res]}")
 