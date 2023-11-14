from data_importer import  data_importer
import matplotlib.pylab as plt
import seaborn as sns
plt.style.use('ggplot')

# data
df_images = data_importer.import_images()


# basic info
print(df_images.shape)

print(df_images.head())

def count_images_per_age(dataframe):
    # Grouping by 'Age' column and counting occurrences of each age
    age_counts = dataframe['Age'].value_counts().sort_index()
    return age_counts

# Example usage:
image_counts_per_age = count_images_per_age(df_images)
print(image_counts_per_age)