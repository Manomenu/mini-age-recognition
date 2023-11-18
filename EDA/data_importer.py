# USER INFO:
# https://drive.google.com/drive/folders/0BxYys69jI14kU0I1YUQyY1ZDRUE?resourcekey=0-01Pth1hq20K4kuGVkp3oBw
# wybierz plik crop_part1 i go pobierz
# wwal do go main folderu projektu i powinno byc git, patrz tylko czy do nazwy pliku nie dodalo sie np. (1) na koncu




import zipfile
from PIL import Image
import io
import pandas as pd
import numpy as np
import re



class data_importer:
    @classmethod
    def import_images(cls):
        file_path = '../crop_full.zip'
        print(file_path)

        # Otwórz plik ZIP
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            # Lista plików w archiwum ZIP
            file_list = zip_ref.namelist()

           
            image_data = []
            ages = []
            genders = []  
            ethnicities = []  

            
            for file_name in file_list:
                if file_name.endswith('.jpg'):
                    # otworz plik
                    with zip_ref.open(file_name) as file:
                        # analiza pliku
                        img_data = file.read()
                        img = Image.open(io.BytesIO(img_data))
                        img_array = np.array(img)
                        image_data.append(img_array)

                      # Wyodrębnij wiek, płeć i etniczność z nazwy pliku
                        info = cls.extract_info_from_filename(file_name)
                        if info is not None and len(info) == 3:  # Sprawdź, czy info ma oczekiwaną długość
                            age, gender, ethnicity = info
                            ages.append(age)
                            genders.append(gender)
                            ethnicities.append(ethnicity)
                        else:
                            print(f"Problem with file: {file_name}. Skipping...")

        #  tworzenie data frame
        df = pd.DataFrame({'Images': image_data, 'Age': ages, 'Gender': genders, 'Race': ethnicities})
        
        
        return df
    @staticmethod
    def extract_info_from_filename(file_name):
        # Use regular expressions to extract age, gender, and race from the file name
        pattern = re.compile(r'(\d+)_(\d)_(\d)_(\d+)')
        match = pattern.search(file_name)

        if match:
            age = int(match.group(1))
            gender = int(match.group(2))
            race = int(match.group(3))
            # date_time = match.group(4)  # If you need date&time as well

            return age, gender, race
        else:
            return None