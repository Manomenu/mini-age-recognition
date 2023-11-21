# ZBIORCZE INFO:
# czytaj info w pliku eda/data_importer


from data_importer import data_importer
import matplotlib.pylab as plt
import seaborn as sns
import numpy as np
import math

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


# def display_random_images(dataframe):
    # Select 16 random rows from the dataframe
    random_selection = dataframe.sample(n=16)

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


# basic info
# rozmiar danych
# print(df_images.shape)
# print(df_images.info())
# print(df_images.tail(10));
# # show images losowe 
# display_random_images(df_images)

# age_group_images = df_images.groupby('Age')['Images'].apply(lambda x: np.mean(np.array(list(x)), axis=0))
# n = len(age_group_images)  


# rows = cols = math.ceil(math.sqrt(n))
# fig, axs = plt.subplots(rows, cols, figsize=(cols * 4, rows * 4))
# #wyswietlenie sredniej twarzy kazdej grupy
# for i, (age, image) in enumerate(age_group_images.items()):
   
#     row = i // cols
#     col = i % cols
#     ax = axs[row, col] if n > 1 else axs
#     ax.imshow(image.astype('uint8'))
#     ax.set_title(f'Wiek {age}')
#     ax.axis('off')

# for i in range(n, rows*cols):
#     axs.flat[i].axis('off')
# plt.show()


# ilosc osob w danym wieku
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



def calculate_image_features(image_array):
    """Oblicza jasność i kontrast obrazu."""
    brightness = np.mean(image_array)  # Średnia jasność
    contrast = np.std(image_array)     # Standardowe odchylenie pikseli dla kontrastu
    return brightness, contrast

# Przetwarzanie obrazów i dodawanie cech do DataFrame
brightness = []
contrast = []

for img_array in df_images['Images']:
    img_brightness, img_contrast = calculate_image_features(img_array)
    brightness.append(img_brightness)
    contrast.append(img_contrast)

df_images['Brightness'] = brightness
df_images['Contrast'] = contrast

# Tworzenie wykresów
plt.figure(figsize=(10, 6))
sns.histplot(data=df_images, x='Brightness')
plt.title('Rozkład Jasności Obrazów')
plt.xlabel('Jasność')
plt.ylabel('Liczba Obrazów')
plt.show()

plt.figure(figsize=(10, 6))
sns.histplot(data=df_images, x='Contrast')
plt.title('Rozkład Kontrastu Obrazów')
plt.xlabel('Kontrast')
plt.ylabel('Liczba Obrazów')
plt.show()


average_brightness_by_age = df_images.groupby('Age')['Brightness'].mean()


plt.figure(figsize=(10, 6))
plt.bar(average_brightness_by_age.index, average_brightness_by_age.values, edgecolor='black')
plt.title('Średnia Jasność Obrazów w Zależności od Wiek')
plt.xlabel('Wiek')
plt.ylabel('Średnia Jasność')
plt.xticks(np.arange(0, 101, 5))  
plt.grid(axis='y')
plt.show()

# Sredni dla gup wiekowych wanie i obliczanie średniego kontrastu dla każdej grupy wiekowej
average_contrast_by_age = df_images.groupby('Age')['Contrast'].mean()

# wykres
plt.figure(figsize=(10, 6))
plt.bar(average_contrast_by_age.index, average_contrast_by_age.values, edgecolor='black')
plt.title('Średni Kontrast Obrazów w Zależności od Wiek')
plt.xlabel('Wiek')
plt.ylabel('Średni Kontrast')
plt.xticks(np.arange(0, 101, 5))  
plt.grid(axis='y')
plt.show()

# age_counts = count_images_per_age(df_images)
# plt.figure(figsize=(10, 6))
# age_counts.plot(kind='bar')
# plt.title('Distribution of Images per Age')
# plt.xlabel('Age')
# plt.ylabel('Count')

# plt.figure(figsize=(8, 8))
# age_counts.plot(kind='pie', autopct='%1.1f%%')
# plt.title('Distribution of Images per Age')
# plt.ylabel('')
# plt.show()




