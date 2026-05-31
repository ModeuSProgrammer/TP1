import pandas as pd

try:
    df = pd.read_csv('dataset.csv')

    # Дозапись в файл
    def write_report(msg):
        with open("report.txt", "a", encoding="utf8") as file:
            file.write(f"{msg}\n")

    # Количество строк в наборе данных и колонок в датасете
    def count_data():
        rows_count = df.shape[0]
        columns_count = df.shape[1]
        write_report(f"({rows_count}, {columns_count})")
        print(f"({rows_count}, {columns_count})")

    # Информация о типах данных, находящихся в каждой колонке набора данных
    def info_type_df():
        with open("report.txt", "a", encoding="utf8") as file:
            df.info(buf=file)
        df.info()

    # Информация о кол-ве незаполненных ячеек в каждой колонке исходного набора данных
    def count_empty_cell():
        null_cell = df.isna().sum()
        write_report(null_cell)
        print(null_cell)

    # Датафрейм с посчитанными данными: average, median,std_dev
    def compute_descriptive_stats():
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

    # Работа с категориальными значениями
    def df_categorical_artists():
        df_artist = df['artist/s'].value_counts()
        write_report(df_artist)
        print(df_artist)

    def df_categorical_key():
        df_key = df['key'].value_counts()
        write_report(df_key)
        print(df_key)

    def df_categorical_mode():
        df_mode = df['mode'].value_counts()
        write_report(df_mode)
        print(df_mode)

    def df_categorical_timesignature():
        df_time_signature = df['time_signature'].value_counts()
        write_report(df_time_signature)
        print(df_time_signature)

except Exception as e:
    print(f"Произошла непредвиденная ошибка: {e}")

# Проверяем используется модуль из другого модуля
if __name__ == "__main__":
    with open("report.txt", "w", encoding="utf8") as file:
        count_data()
        info_type_df()
        count_empty_cell()
        compute_descriptive_stats()
        df_categorical_artists()
        df_categorical_key()
        df_categorical_mode()
        df_categorical_timesignature()
