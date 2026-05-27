import pandas as pd

def create_report():
    try:
        # Чтение данных из файла csv
        df = pd.read_csv('dataset.csv')

        with open("report.txt", "w", encoding="utf8") as file:
            # Количество строк в наборе данных и колонок в датасете
            rows_count = df.shape[0]
            columns_count = df.shape[1]
            file.write(f"({rows_count}, {columns_count})\n")
            print(f"({rows_count}, {columns_count})")

            # Информация о типах данных, находящихся в каждой колонке набора данных
            df.info(buf=file)
            print(df.info())

            # Информация о кол-ве незаполненных ячеек в каждой колонке исходного набора данных
            null_cell = df.isna().sum()
            file.write(f"{null_cell}")
            print(null_cell)

            average = df[['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'valence', 'tempo',
                          'duration_ms']].mean()
            median = df[['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'valence', 'tempo',
                         'duration_ms']].median()
            std_dev = df[['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'valence', 'tempo',
                          'duration_ms']].std()
            # Датафрейм с посчитанными данными: average, median,std_dev
            df_counted = pd.DataFrame({
                'Среднее': average,
                'Медиана': median,
                'Отклонение': std_dev}).round(2)

            file.write(f"\n{df_counted}")
            print(df_counted)

            # Работа с категориальными значениями
            # Артисты категориальные данные
            df_categorical_artists = df['artist/s'].value_counts()
            file.write(f"\n{df_categorical_artists}")
            print(df_categorical_artists)

            # Ключ категориальные данные
            df_categorical_key = df['key'].value_counts()
            file.write(f"\n{df_categorical_key}")
            print(df_categorical_key)

            # Режим категориальные данные
            df_categorical_mode = df['mode'].value_counts()
            file.write(f"\n{df_categorical_mode}")
            print(df_categorical_mode)

            # Такт категориальные данные
            df_categorical_timesignature = df['time_signature'].value_counts()
            file.write(f"\n{df_categorical_timesignature}")
            print(df_categorical_timesignature)

    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

# Проверяем используется функция в пределах этого .py файла
if __name__ == "__main__":
    create_report()