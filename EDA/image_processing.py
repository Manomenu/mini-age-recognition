from data_importer import data_importer
import matplotlib.pylab as plt
import seaborn as sns
import numpy as np
import math
from PIL import Image
import numpy as np
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
from main import aplly_ege_filter
from skimage.transform import resize


def get_original_and_edge_side_by_side(original_image):
    resulting_image = aplly_ege_filter(original_image)
    resized_resulting_image = resize(resulting_image, original_image.shape, mode='constant', anti_aliasing=True)

    # Set red color for the edges
    resized_resulting_image_colored = np.zeros_like(resized_resulting_image)

    resized_resulting_image_colored[resulting_image > 0, 0] = 255
    resized_resulting_image_colored[resulting_image > 0, 1] = 255
    resized_resulting_image_colored[resulting_image > 0, 2] = 255

    # Convert pixel values to the appropriate range for display
    return  np.concatenate((original_image / 255.0, resized_resulting_image_colored), axis=1)
    #return np.concatenate((original_image / 255.0, resized_resulting_image), axis=1)

def get_original_and_edge_on_top(original_image):
    resulting_image = aplly_ege_filter(original_image)
    resized_resulting_image = resize(resulting_image, original_image.shape, mode='constant', anti_aliasing=True)


    # Convert pixel values to the appropriate range for display
    combined_image = np.concatenate((original_image / 255.0, resized_resulting_image), axis=1)
    # Set a vibrant green color for the edges
    edge_color = np.zeros_like(original_image, dtype=np.uint8)
    edge_color[1, :, :] = 255

    # Overlay edges on top of the original image with the specified color
    return np.where(resized_resulting_image > 0, edge_color / 255.0, original_image / 255.0)