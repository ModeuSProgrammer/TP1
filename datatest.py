import pandas as pd

# Чтение данных из файла csv
df = pd.read_csv('dataset.csv')

# Количество строк в наборе данных и колонок в датасете
rows_count = df.shape[0]
columns_count = df.shape[1]
print(f"({rows_count}, {columns_count})")

# Информация о типах данных, находящихся в каждой колонке набора данных
print(df.info())

# Информация о кол-ве незаполненных ячеек в каждой колонке исходного набора данных
null_cell = df.isna().sum()
print(null_cell)

average = df[['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'valence', 'tempo', 'duration_ms']].mean()
median = df[['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'valence', 'tempo', 'duration_ms']].median()
std_dev = df[['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'valence', 'tempo', 'duration_ms']].std()
# Датафрейм с посчитанными данными: average, median,std_dev
df_counted = pd.DataFrame({
                    'Среднее': average,
                    'Медиана': median,
                    'Отклонение': std_dev}).round(2)

print(df_counted)

# Работа с категориальными значениями
# Артисты категориальные данные
df_categorical_artists = df['artist/s'].value_counts()
print(df_categorical_artists)
# Ключ категориальные данные
df_categorical_key = df['key'].value_counts()
print(df_categorical_key)
# Режим категориальные данные
df_categorical_mode = df['mode'].value_counts()
print(df_categorical_mode)
# Такт категориальные данные
df_categorical_timesignature = df['time_signature'].value_counts()
print(df_categorical_timesignature)