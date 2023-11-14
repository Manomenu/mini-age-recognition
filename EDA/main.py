# ZBIORCZE INFO:
# czytaj info w pliku eda/data_importer


from data_importer import data_importer
import matplotlib.pylab as plt
import seaborn as sns

plt.style.use('ggplot')

# data
df_images = data_importer.import_images()


# functions
def count_images_per_age(dataframe):
    # Grouping by 'Age' column and counting occurrences of each age
    age_counts = dataframe['Age'].value_counts().sort_index()
    return age_counts

def display_random_images(dataframe):
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
print(df_images.shape)

# show images
display_random_images(df_images)

# ilosc osob w danym wieku
plt.figure(figsize=(10, 6))
plt.hist(df_images['Age'], bins=20, edgecolor='black')
plt.title('Histogram of Age Distribution')
plt.xlabel('Ages')
plt.ylabel('Frequency')
plt.show()


# age_counts = count_images_per_age(df_images)
# plt.figure(figsize=(10, 6))
# age_counts.plot(kind='bar')
# plt.title('Distribution of Images per Age')
# plt.xlabel('Age')
# plt.ylabel('Count')
# plt.show()
#
# plt.figure(figsize=(8, 8))
# age_counts.plot(kind='pie', autopct='%1.1f%%')
# plt.title('Distribution of Images per Age')
# plt.ylabel('')
# plt.show()




