import datatest
from datetime import datetime
import io
import tkinter as tk
from matplotlib import figure
from PIL import Image, ImageTk

df = datatest.df
part_df = df.drop(columns=['title', 'artist/s', 'key', 'mode', 'time_signature'])

# Глобальные выбранные значение x и y
current_x_index = 1
current_y_index = 2

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
            columns = (list(part_df.columns)[1:])
            nav_xy_interface(columns)

        # Изменяет значение графика
        def btn_switch_graph(title, flag):
            global current_x_index, current_y_index
            col_index = part_df.columns.get_loc(title)
            match flag:
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

        # Работа с отображением графиков
        def get_scatter_as_photoimage():
            global current_x_index, current_y_index, fig
            fig = figure.Figure(layout="constrained")
            ax = fig.add_subplot()
            fig.supxlabel(part_df.columns[current_x_index])
            fig.supylabel(part_df.columns[current_y_index])
            x_column = part_df.iloc[:, current_x_index]
            y_column = part_df.iloc[:, current_y_index]
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
