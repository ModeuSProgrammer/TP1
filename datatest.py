import pandas as pd

# Чтение данных из файла csv
try:
    df = pd.read_csv('dataset.csv')
except Exception as e:
    print(f"Произошла непредвиденная ошибка: {e}")

# Дозапись в файл
def write_report(msg):
    try:
        with open("report.txt", "a", encoding="utf8") as file:
            file.write(f"{msg}\n")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

# Количество строк в наборе данных и колонок в датасете
def count_data(df):
    try:
        rows_count = df.shape[0]
        columns_count = df.shape[1]
        write_report(f"({rows_count}, {columns_count})")
        print(f"({rows_count}, {columns_count})")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

# Информация о типах данных, находящихся в каждой колонке набора данных
def info_type_df(df):
    try:
        with open("report.txt", "a", encoding="utf8") as file:
            df.info(buf=file)
        df.info()
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


# Информация о кол-ве незаполненных ячеек в каждой колонке исходного набора данных
def count_empty_cell(df):
    try:
        null_cell = df.isna().sum()
        write_report(null_cell)
        print(null_cell)
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

# Датафрейм с посчитанными данными: average, median,std_dev
def compute_descriptive_stats(df):
    try:
        average = df[['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'valence', 'tempo',
                      'duration_ms']].mean()
        median = df[['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'valence', 'tempo',
                     'duration_ms']].median()
        std_dev = df[['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'valence', 'tempo',
                      'duration_ms']].std()
        df_counted = pd.DataFrame({
            'Среднее': average,
            'Медиана': median,
            'Отклонение': std_dev}).round(2)

        write_report(df_counted)
        print(df_counted)
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

# Работа с категориальными значениями
def df_categorical_artists(df):
    try:
        df_artist = df['artist/s'].value_counts()
        write_report(df_artist)
        print(df_artist)
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

def df_categorical_key(df):
    try:
        df_key = df['key'].value_counts()
        write_report(df_key)
        print(df_key)
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

def df_categorical_mode(df):
    try:
        df_mode = df['mode'].value_counts()
        write_report(df_mode)
        print(df_mode)
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

def df_categorical_timesignature(df):
    try:
        df_time_signature = df['time_signature'].value_counts()
        write_report(df_time_signature)
        print(df_time_signature)
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

# Проверяем используется модуль из другого модуля
if __name__ == "__main__":
    with open("report.txt", "w", encoding="utf8") as file:
        count_data(df)
        info_type_df(df)
        count_empty_cell(df)
        compute_descriptive_stats(df)
        df_categorical_artists(df)
        df_categorical_key(df)
        df_categorical_mode(df)
        df_categorical_timesignature(df)
