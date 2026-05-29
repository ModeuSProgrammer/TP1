import datatest
import io
import tkinter as tk
from matplotlib import figure
from PIL import Image, ImageTk


def app():
    try:
        df = datatest.df
        # Создание главного окна
        window = tk.Tk()

        # Отображения меню ось y
        def nav_y_interface(columns):
            frame_y = tk.Frame(borderwidth=1, relief=tk.SOLID, padx=5, pady=5)
            frame_y.pack(side=tk.LEFT, fill=tk.Y)
            for col in columns:
                btn = tk.Button(frame_y, text=col, padx=5, pady=5)
                btn.pack(anchor=tk.NW)

        # Отображения меню ось x
        def nav_x_interface(columns):
            frame_x = tk.Frame(borderwidth=1, relief=tk.SOLID, padx=5, pady=5)
            frame_x.pack(side=tk.BOTTOM, fill=tk.X)
            for col in columns:
                btn = tk.Button(frame_x, text=col, padx=5, pady=5)
                btn.pack(side=tk.LEFT)

        # Заполнение значений
        def nav_add_xy_values():
            part_df = df.drop(columns=['title', 'artist/s', 'key', 'mode', 'time_signature'])
            columns = (list(part_df.columns)[1:])
            nav_y_interface(columns)
            nav_x_interface(columns)

        # Работа с отображением графиков
        def get_scatter_as_photoImage():
            fig = figure.Figure()
            ax = fig.add_subplot()
            part_df = df.drop(columns=['title', 'artist/s', 'key', 'mode', 'time_signature'])

            fig.supxlabel(part_df.columns[2])
            fig.supylabel(part_df.columns[1])
            ax.scatter([0], [0])
            buf = io.BytesIO()
            fig.savefig(buf)
            image = Image.open(buf)
            return ImageTk.PhotoImage(image)

        # Вызов функций связанных с отображением информации
        nav_add_xy_values()
        canvas = tk.Canvas(width=640, height=480)
        canvas.pack(side=tk.LEFT)

        # Добавление изображение графика
        image = get_scatter_as_photoImage()
        canvas.create_image(0, 0, anchor=tk.NW, image=image)

        # Отображение главного окна и его ограничение
        window.resizable(False, False)
        window.mainloop()

    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


if __name__ == "__main__":
    app()
