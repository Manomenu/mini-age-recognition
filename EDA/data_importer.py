import tarfile
from PIL import Image
import io
import pandas as pd
import numpy as np
import re

def retrieve_first_number(string):
    match = re.search(r'\d+', string)
    if match:
        return int(match.group())
    else:
        return None

class data_importer:
    @classmethod
    def import_images(cls):
        file_path = '../crop_part1.tar.gz'
        # Open the tar.gz file
        tar = tarfile.open(file_path, 'r:gz')

        # Lists to store data
        image_data = []
        ages = []

        # Regular expression pattern to extract age from file names
        pattern = re.compile(r'(\d+)_')

        # Iterate through the files in the tar archive
        for member in tar.getmembers():
            if member.name.endswith('.jpg'):
                # Extract image bytes from the tar archive
                file = tar.extractfile(member)
                if file is not None:
                    # Read image bytes into PIL Image
                    img_data = file.read()
                    img = Image.open(io.BytesIO(img_data))
                    # Convert image to numpy array
                    img_array = np.array(img)
                    # Append image array to the list
                    image_data.append(img_array)
                    age = retrieve_first_number(member.name.split('/')[1])
                    ages.append(age)

        # Close the tar file
        tar.close()

        # Create a DataFrame from image data and age info
        df = pd.DataFrame({'Images': image_data, 'Age': ages})
        return df