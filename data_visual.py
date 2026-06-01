import data_scatter


try:
    df = data_scatter.df
    part_category_df = df[['title', 'artist/s', 'key', 'mode', 'time_signature']]

    def get_category_titles():
        titles = list(part_category_df[:1])
        print(titles)


    get_category_titles()

except Exception as e:
    print(f"Произошла непредвиденная ошибка: {e}")
