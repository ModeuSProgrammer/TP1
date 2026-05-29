from datatest
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
        def nav_y_interface():
            frame_y = tk.Frame(borderwidth=1, relief=tk.SOLID, padx=5, pady=5)
            frame_y.pack(side=tk.LEFT, fill=tk.Y)
            name_btn = tk.Button(frame_y, text="значение 1", padx=5, pady=5)
            name_btn.pack(anchor=tk.NW)

        # Добавление значений меню ось y
        def nav_add_y_values():
            print (df)

        nav_add_y_values()
        # Отображения меню ось x
        def nav_x_interface():
            frame_x = tk.Frame(borderwidth=1, relief=tk.SOLID, padx=5, pady=5)
            frame_x.pack(side=tk.BOTTOM, fill=tk.X)

            name_btn = tk.Button(frame_x, text="значение 1", padx=5, pady=5)
            name_btn.pack(side=tk.LEFT)

        # Работа с отображением графиков
        def get_scatter_as_photoImage():
            fig = figure.Figure()
            ax = fig.add_subplot()
            fig.supxlabel("метка абцисс x")
            fig.supylabel("метка ординат y")
            ax.scatter([0], [0])
            buf = io.BytesIO()
            fig.savefig(buf)
            image = Image.open(buf)
            return ImageTk.PhotoImage(image)

        # Вызов функций связанных с отображением информации
        nav_y_interface()
        nav_x_interface()
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
