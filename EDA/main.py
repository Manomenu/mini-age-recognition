# ZBIORCZE INFO:
# czytaj info w pliku eda/data_importer


from data_importer import data_importer
import matplotlib.pylab as plt
import seaborn as sns
import numpy as np
import math
import cv2

plt.style.use('ggplot')

# data
df_images = data_importer.import_images()


# functions
def count_images_per_age(dataframe):
    # Grouping by 'Age' column and counting occurrences of each age
    age_counts = dataframe['Age'].value_counts().sort_index()
    return age_counts

def count_image_per_race(dataframe):
    
    race_counts = dataframe['Race'].value_counts().sort_index()
    return race_counts

def count_image_per_gender(dataframe):
    
    gender_counts = dataframe['Gender'].value_counts().sort_index()
    return gender_counts

def calculate_image_features(image_array):
    """Oblicza jasność i kontrast obrazu."""
    brightness = np.mean(image_array)  # Średnia jasność
    contrast = np.std(image_array)     # Standardowe odchylenie pikseli dla kontrastu
    return brightness, contrast

def apply_gabor_filter(image, kernel_size=31, sigma=4.0, theta=0, lam=10.0, gamma=0.5, psi=0):
   
    gabor_kernel = cv2.getGaborKernel((kernel_size, kernel_size), sigma, theta, lam, gamma, psi, ktype=cv2.CV_32F)
    filtered_image = cv2.filter2D(image, -1, gabor_kernel)
    return filtered_image

def display_random_images(dataframe):
 
    random_selection = dataframe.sample(n=16)

    
    fig, axes = plt.subplots(4, 4, figsize=(10, 10))
    fig.subplots_adjust(hspace=0.5, wspace=0.5)
    fig.suptitle('Sample Images')

    for i, ax in enumerate(axes.flat):
       
        if i < len(random_selection):
            image_data = random_selection.iloc[i]['Images']
            ax.imshow(image_data)
            ax.axis('off')

    plt.show()


def aplly_ege_filter(img):
    min_intensity_grad, max_intensity_grad = 100, 200
    edge_img = cv2.Canny(img, min_intensity_grad, max_intensity_grad) 
    return edge_img


# accepting just dataframe that has one column ['Images']
# you can convert array to dataframe like so: pd.DataFrame(array, ['Images'])
def random_imgs(images_only_dataframe):
    # Select 16 random rows from the dataframe
    random_selection = images_only_dataframe.sample(n=16)

    # Create a 4x4 subplot grid
    fig, axes = plt.subplots(4, 4, figsize=(10, 10))
    fig.subplots_adjust(hspace=0.5, wspace=0.5)
    fig.suptitle('Sample Images')

    for i, ax in enumerate(axes.flat):
        # Plot each image
        if i < len(random_selection):
            image_data = random_selection.iloc[i]['Images']
            ax.imshow(image_data)
            ax.axis('off')
    plt.show()



plt.show()
brightness = []
contrast = []

brightness_after_gabor = []
contrast_after_gabor = []

brightness_after_edgedetection=[]
contrast_after_edgedetection=[]

for img_array in df_images['Images']:
    # Stosowanie filtru Gabora
    filtered_image = apply_gabor_filter(img_array)
    edge_image=aplly_ege_filter(img_array)

    # Obliczanie cech po filtrze
    img_brightness, img_contrast = calculate_image_features(filtered_image)
    brightness_after_gabor.append(img_brightness)
    contrast_after_gabor.append(img_contrast)

    img_brightness, img_contrast = calculate_image_features(img_array)
    brightness.append(img_brightness)
    contrast.append(img_contrast)

    img_brightness, img_contrast = calculate_image_features(edge_image)
    brightness_after_edgedetection.append(img_brightness)
    contrast_after_edgedetection.append(img_contrast)

df_images['Brightness'] = brightness
df_images['Contrast'] = contrast
df_images['BrightnessAfterGabor'] = brightness_after_gabor
df_images['ContrastAfterGabor'] = contrast_after_gabor
df_images['BrightnessAfterEdge']=brightness_after_edgedetection
df_images['ContrastAfterEdge']=contrast_after_edgedetection
# ilosc osob w danym wieku


print(df_images.shape)
print(df_images.info())

# # show images losowe 
display_random_images(df_images)

age_group_images = df_images.groupby('Age')['Images'].apply(lambda x: np.mean(np.array(list(x)), axis=0))
n = len(age_group_images)  


rows = cols = math.ceil(math.sqrt(n))
fig, axs = plt.subplots(rows, cols, figsize=(cols * 4, rows * 4))
#wyswietlenie sredniej twarzy kazdej grupy
for i, (age, image) in enumerate(age_group_images.items()):
   
    row = i // cols
    col = i % cols
    ax = axs[row, col] if n > 1 else axs
    ax.imshow(image.astype('uint8'))
    ax.set_title(f'Wiek {age}')
    ax.axis('off')

for i in range(n, rows*cols):
    axs.flat[i].axis('off')
plt.figure(figsize=(10, 6))
plt.hist(df_images['Age'], bins=20, edgecolor='black')
plt.title('Histogram of Age Distribution')
plt.xlabel('Ages')
plt.ylabel('Frequency')
plt.show()

plt.figure(figsize=(10, 8))
labels=['Male', 'Female']
gender_freq=count_image_per_gender(df_images)
plt.bar(labels,gender_freq,color=np.random.rand(len(labels),3));
plt.title('Histogram of Gender Distribution')
plt.xlabel('Gender')
plt.ylabel('Frequency')
plt.legend(title='Gender')
plt.show()


plt.figure(figsize=(12, 8))
labels=['White', 'Black', 'Asian', 'Indian', 'Others']
races_freq=count_image_per_race(df_images)
plt.bar(labels,races_freq,color=np.random.rand(len(labels),3))
plt.title('Histogram of Race Distribution')
plt.xlabel('Race')
plt.ylabel('Frequency')
plt.legend(title='Race')
plt.show()



plt.figure(figsize=(10, 6))
plt.hist(df_images['Size'], bins=20, edgecolor='black')
plt.title('Histogram of Size Distribution')
plt.xlabel('Size in KB')
plt.ylabel('Frequency')
plt.show()


age_group = df_images.groupby('Age')['Size'].mean()

# Tworzenie wykresu
plt.figure(figsize=(10, 6))
plt.bar(age_group.index, age_group.values, edgecolor='black')
plt.title('Histogram of Average Image Size by Age')
plt.xlabel('Age')
plt.ylabel('Average Image Size in KB')
plt.xticks(np.arange(0, 101, 5))  # Ustawienie podziałek osi X co 10 lat
plt.grid(axis='y')
plt.show()





# Przetwarzanie obrazów i dodawanie cech do DataFrame


# Tworzenie wykresów
plt.figure(figsize=(10, 6))
sns.histplot(data=df_images, x='Brightness')
plt.title('Histogram of Brightness')
plt.xlabel('Brightness')
plt.ylabel('Image count')
plt.show()

plt.figure(figsize=(10, 6))
sns.histplot(data=df_images, x='Contrast')
plt.title('Histogram of Contrast')
plt.xlabel('Contrast')
plt.ylabel('Image count')
plt.show()


average_brightness_by_age = df_images.groupby('Age')['Brightness'].mean()


plt.figure(figsize=(10, 6))
plt.bar(average_brightness_by_age.index, average_brightness_by_age.values, edgecolor='black')
plt.title('Average brightness  by age')
plt.xlabel('Age')
plt.ylabel('Average brightness')
plt.xticks(np.arange(0, 101, 5))  
plt.grid(axis='y')
plt.show()

# Sredni dla gup wiekowych wanie i obliczanie średniego kontrastu dla każdej grupy wiekowej
average_contrast_by_age = df_images.groupby('Age')['Contrast'].mean()

# wykres
plt.figure(figsize=(10, 6))
plt.bar(average_contrast_by_age.index, average_contrast_by_age.values, edgecolor='black')
plt.title('Average contrast  by age')
plt.xlabel('Age')
plt.ylabel('Average contrast')
plt.xticks(np.arange(0, 101, 5))  
plt.grid(axis='y')
plt.show()



sample_images = df_images['Images'].sample(5)
img = df_images.loc[df_images['Size'].idxmax()]['Images']

contrast_img = cv2.addWeighted(img, 2.5, np.zeros(img.shape, img.dtype), 0, 0)

# Konwersja do skali szarości
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detekcja krawędzi
min_intensity_grad, max_intensity_grad = 100, 200
edge_img = cv2.Canny(img, min_intensity_grad, max_intensity_grad)

# Tworzenie wykresów
fig, ax = plt.subplots(1, 4, figsize=(20, 10))
ax[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)); ax[0].set_title('Original Image')
ax[1].imshow(cv2.cvtColor(contrast_img, cv2.COLOR_BGR2RGB)); ax[1].set_title('Increased Contrast')
ax[2].imshow(img_gray, cmap='gray', vmin=0, vmax=255); ax[2].set_title('Grayscale')
ax[3].imshow(edge_img, cmap='gray', vmin=0, vmax=255); ax[3].set_title('Edge Detection') 
plt.show()
# Tworzenie wykresu
fig, axs = plt.subplots(2, 5, figsize=(20, 8))

for i, img_array in enumerate(sample_images):
    # Oryginalny obraz
    axs[0, i].imshow(cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB))
    axs[0, i].set_title(f'Original Image {i+1}')
    axs[0, i].axis('off')

    # Obraz po zastosowaniu filtru Gabora
    gabor_image = apply_gabor_filter(img_array)
    axs[1, i].imshow(cv2.cvtColor(gabor_image, cv2.COLOR_BGR2RGB))
    axs[1, i].set_title(f'Gabor Filtered {i+1}')
    axs[1, i].axis('off')



average_brightness_by_class = df_images.groupby('Age')['BrightnessAfterGabor'].mean()
plt.figure(figsize=(10, 6))
average_brightness_by_class.plot(kind='bar')
plt.title('Average Brightness After Gabor Filter by Age Group')
plt.xlabel('Age Group')
plt.ylabel('Average Brightness After Gabor Filter')
plt.xticks(np.arange(0, 101, 5))
plt.show()


# Grupowanie danych według klasy (np. 'Age') i obliczanie średniego kontrastu
average_contrast_by_class = df_images.groupby('Age')['ContrastAfterGabor'].mean()


plt.figure(figsize=(10, 6))
average_contrast_by_class.plot(kind='bar')
plt.title('Average Contrast After Gabor Filter by Age Group')
plt.xlabel('Age Group')
plt.ylabel('Average Contrast After Gabor Filter')
plt.xticks(np.arange(0, 101, 5))
plt.show()


average_brightness_by_class = df_images.groupby('Age')['BrightnessAfterEdge'].mean()
average_contrast_by_class = df_images.groupby('Age')['ContrastAfterEdge'].mean()

plt.figure(figsize=(10, 6))
average_brightness_by_class.plot(kind='bar')
plt.title('Average Brightness After Edge detection by Age Group')
plt.xlabel('Age Group')
plt.ylabel('Average Brightness After Edge detection Filter')
plt.xticks(np.arange(0, 101, 5))
plt.show()

plt.figure(figsize=(10, 6))
average_contrast_by_class.plot(kind='bar')
plt.title('Average Contrast After Edge detection by Age Group')
plt.xlabel('Age Group')
plt.ylabel('Average Contrast After Edge detection')
plt.xticks(np.arange(0, 101, 5))
plt.show()