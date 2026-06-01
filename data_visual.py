import datatest
from datetime import datetime
import io
import tkinter as tk
from matplotlib import figure
from PIL import Image, ImageTk

df = datatest.df
df = df.drop(columns=['title'])
# Глобальные выбранные значение x и y
current_x_index = 1
current_y_index = 2
part_numpy_df = df.drop(columns=['artist/s', 'key', 'mode', 'time_signature'])
part_category_df = df[['artist/s', 'key', 'mode', 'time_signature']]


def app():
    try:
        # Заполнение меню осей x и y
        def nav_xy_interface(columns):
            for col in columns:
                btn_y = tk.Button(frame_y, text=col, padx=10, pady=5)
                btn_y.pack(anchor=tk.NW, fill="x")
                btn_y.axis = "Y"
                btn_y.bind("<Button-1>", on_click_menu)
                btn_x = tk.Button(frame_x, text=col, padx=10, pady=5)
                btn_x.pack(side=tk.LEFT)
                btn_x.axis = "X"
                btn_x.bind("<Button-1>", on_click_menu)

        # Формирование списка значений
        def nav_add_xy_values():
            columns = (list(df.columns)[1:])
            nav_xy_interface(columns)

        # Изменяет значение графика
        def btn_switch_graph(title, axis):
            global current_x_index, current_y_index
            col_index = df.columns.get_loc(title)
            match axis:
                case 'X':
                    current_x_index = col_index
                case 'Y':
                    current_y_index = col_index

        # Отслеживает нажатие на кнопки меню
        def on_click_menu(event):
            btn_text = event.widget.cget("text")
            btn_axis = event.widget.axis
            btn_switch_graph(btn_text, btn_axis)
            update_image()

        # Обновление графика
        def update_image():
            global image
            image = get_scatter_as_photoimage()
            canvas.delete("all")
            canvas.create_image(0, 0, anchor=tk.NW, image=image)

        # Определение типа
        def get_col_type(column):
            if column in part_category_df.columns:
                return "category"
            else:
                return "numeric"

        # Работа с отображением графиков
        def get_scatter_as_photoimage():
            global current_x_index, current_y_index, fig
            fig = figure.Figure(layout="constrained")
            ax = fig.add_subplot()
            fig.supxlabel(df.columns[current_x_index])
            fig.supylabel(df.columns[current_y_index])
            x_column = df.iloc[:, current_x_index]
            y_column = df.iloc[:, current_y_index]
            x_type = get_col_type(df.columns[current_x_index])
            y_type = get_col_type(df.columns[current_y_index])
            #Варианты диаграмм
            if current_x_index == current_y_index and x_type == "numeric":
                ax.hist(x_column, bins=10)
            elif current_x_index == current_y_index and x_type == "category":
                counts = x_column.value_counts()
                ax.pie(counts.values, labels=counts.index)
            elif x_type == "category" and y_type == "numeric":
                counts = df.groupby(df.columns[current_x_index])[df.columns[current_y_index]].count()
                ax.bar(counts.index.astype(str), counts.values)
                ax.tick_params(axis='x', rotation=90, labelsize=8)
            elif x_type == "numeric" and y_type == "category":
                groups = [x_column[y_column == cat] for cat in y_column.unique()]
                ax.boxplot(groups, tick_labels=y_column.unique())
                ax.tick_params(axis='x', rotation=90, labelsize=8)
            else:
                ax.scatter(x_column, y_column, marker=">")

            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            buf.seek(0)
            return ImageTk.PhotoImage(Image.open(buf))

        # Сохранение изображения
        def save_click(event):
            global fig
            if fig is None:
                return
            now = datetime.now()
            time_formatted = now.strftime("%H_%M_%S")
            filename = f"graph_{time_formatted}.png"
            fig.savefig(filename)

        window = tk.Tk()

        # Создание областей для меню x и y
        frame_y = tk.Frame(borderwidth=1, relief=tk.SOLID, padx=5, pady=5)
        frame_y.pack(side=tk.LEFT, fill=tk.Y)
        frame_x = tk.Frame(borderwidth=1, relief=tk.SOLID, padx=5, pady=5)
        frame_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Создание области для расположения доп. кнопок
        frame_settings = tk.Frame(frame_y)
        frame_settings.pack(side=tk.BOTTOM, fill="x")
        btn_save = tk.Button(frame_settings, text="Сохранить", padx=5, pady=5)
        btn_save.pack(fill="x")
        btn_save.bind("<Button-1>", save_click)

        # Вызов функций связанных с отображением информации
        nav_add_xy_values()

        canvas = tk.Canvas(width=740, height=480)
        canvas.pack(side=tk.LEFT)
        # Добавление изображение графика при иницилизации приложения
        image = get_scatter_as_photoimage()
        canvas.create_image(0, 0, anchor=tk.NW, image=image)

        window.resizable(False, False)
        window.mainloop()
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


if __name__ == "__main__":
    app()
