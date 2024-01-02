# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import os
import cv2
import numpy as np
import shutil
from PIL import Image, ImageFilter
#import requests
import face_recognition
import random
#from image_utils import drawBoundingBoxWithAgeEstimate

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def drawBoundingBoxWithAgeEstimate(image, left, top, bottom, right, ageEstimate):
    padding = 2
    cv2.rectangle(image, (left - padding , top - padding ), (right + padding , bottom+ padding), (36,255,12), 5)
    label = str(ageEstimate)
  #  (w, h), _ = cv2.getTextSize(label, font_face,  font_size, line_type)

    cv2.rectangle(image, (left , top  - padding ), (left  + padding, top), (36,255,12), 5)
    cv2.rectangle(image, (left , top  - padding ), (left  + padding, top), (36,255,12), -1)
   # cv2.putText(image, label ,(left, top), font_face, font_size ,font_color ,line_type)




# Testing the face recognition

with open('PeopleDataVerification.txt', 'w', encoding='utf-8') as out:
    folder_path = "./Selected"
    # odpal program bedac w folderze recognitio_evaluation
    result_folder = os.path.join("./", 'result')
    image_files = [file for file in os.listdir(folder_path) if
                   file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        # original_image = Image.open(image_path)
        # image = ImageTk.PhotoImage(original_image)

        face_rec_image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(face_rec_image)
        face_count = 0
        if face_locations:
            for face_location in face_locations:
                face_count += 1
                top, right, bottom, left = face_location
                face_image = face_rec_image[:, :]
                drawBoundingBoxWithAgeEstimate(face_image, left, top, bottom, right, random.randint(0, 100))
        out.write(image_file.split(".")[0] + "." + image_file.split(".")[1] + ";" + str(face_count) + "\n")

        os.makedirs(result_folder, exist_ok=True)
        pil_image = Image.fromarray(face_rec_image)
        result_image_path = os.path.join(result_folder, f"result_{image_file}")
        pil_image.save(result_image_path, quality=95)









# Copying images with different face counts

# with open('PeopleData.txt', 'w', encoding='utf-8') as out:
#     items = os.listdir("./Data")
#     face_count = [0] * 100
#     linename = ""
#     for item in items:
#         item_path = os.path.join("./Data", item)
#         if os.path.isdir(item_path):
#             # print(item)
#             f = open(f"./Data/{item}/PersonData.txt", "r")
#             Lines = f.readlines()
#             count = 0
#
#             for line in Lines:
#                 line = line.strip()
#                 if line.endswith(".jpg"):
#                     if count > 1 and count < 15 and face_count[count] < 100:
#                         #print(str(item) + "/" + linename)
#                         shutil.copy("Data/" + str(item) + "/" + linename, 'Selected')
#                         out.write(linename.split(".")[0] + ";" + str(count)+"\n")
#                         face_count[count] += 1
#                     count = 0
#                     linename = line
#                 else:
#                     count += 1
#             # print(str(count))
#             f.close()
#
#     count = 0
#     items = os.listdir("./DataSingle")
#     for item in items:
#         item_path = os.path.join("./DataSingle", item)
#         if count > 100:
#             break
#         shutil.copy("DataSingle/" + str(item), 'Selected')
#         out.write(item.split(".")[0] + ";1\n")
#         count += 1
#
#     f = open(f"NoHumansURL.txt", "r")
#     Lines = f.readlines()
#     for line in Lines:
#         image_url = line.strip()
#         img_data = requests.get(image_url).content
#         img_name = image_url.split("/")[-1]
#         out.write(img_name.split(".")[0] + ";0\n")
#         with open(f'./Selected/{img_name}', 'wb') as handler:
#             handler.write(img_data)
#
#     #print(face_count)
#
#     items = os.listdir("./Selected")
#     for item in items:
#         os.rename("./Selected/" + item, "./Selected/" + item.split(".")[0] + ".original.jpg")



# Modifying images

# def gammaCorrection(src, gamma):
#     invGamma = 1 / gamma
#
#     table = [((i / 255) ** invGamma) * 255 for i in range(256)]
#     table = np.array(table, np.uint8)
#
#     return cv2.LUT(src, table)
#
# count = 0
# for item in os.listdir("./Selected"):
#     img = cv2.imread("./Selected/" + item)
#
#     gammaImg = gammaCorrection(img, 3)
#     cv2.imwrite("./Selected/" + item.split(".")[0] + ".gamma.jpg", gammaImg)
#
#     avgBlurImg = cv2.blur(img,(10,10))
#     cv2.imwrite("./Selected/" + item.split(".")[0] + ".blur.jpg", avgBlurImg)
#
#     alpha = 0.4  # Contrast control
#     beta = 100 # Brightness control
#     # call convertScaleAbs function
#     contrastImg = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
#     cv2.imwrite("./Selected/" + item.split(".")[0] + ".contrast.jpg", contrastImg)
#
#     if count % 10 == 0:
#         print(count)
#     count += 1