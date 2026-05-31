import datatest
import io
import tkinter as tk
from matplotlib import figure
from PIL import Image, ImageTk

current_x_index = 1
current_y_index = 2
try:
    df = datatest.df
    # Создание главного окна
    window = tk.Tk()

    # Заполнение меню осей xy
    def nav_xy_interface(columns):
        frame_y = tk.Frame(borderwidth=1, relief=tk.SOLID, padx=5, pady=5)
        frame_y.pack(side=tk.LEFT, fill=tk.Y)
        frame_x = tk.Frame(borderwidth=1, relief=tk.SOLID, padx=5, pady=5)
        frame_x.pack(side=tk.BOTTOM, fill=tk.X)
        for col in columns:
            btn_y = tk.Button(frame_y, text=col, padx=5, pady=5)
            btn_y.pack(anchor=tk.NW)
            btn_y.axis = "Y"
            btn_y.bind("<Button-1>", on_click)
            btn_x = tk.Button(frame_x, text=col, padx=5, pady=5)
            btn_x.pack(side=tk.LEFT)
            btn_x.axis = "X"
            btn_x.bind("<Button-1>", on_click)

    # Заполнение значений
    def nav_add_xy_values():
        part_df = df.drop(columns=['title', 'artist/s', 'key', 'mode', 'time_signature'])
        columns = (list(part_df.columns)[1:])
        nav_xy_interface(columns)


    # Выбор значения меню
    def btn_switch_menu(title, flag):
        global current_x_index, current_y_index
        part_df = df.drop(columns=['title', 'artist/s', 'key', 'mode', 'time_signature'])
        col_index = part_df.columns.get_loc(title)
        print(col_index)
        match flag:
            case 'X':
               current_x_index = col_index
            case 'Y':
               current_y_index = col_index


    def on_click(event):
        btn_text = event.widget.cget("text")
        btn_axis = event.widget.axis
        btn_switch_menu(btn_text, btn_axis)
        print(f"Вы нажали: {btn_text} {btn_axis}")
        update_image()

    def update_image():
        global image
        image = get_scatter_as_photoImage()
        canvas.delete("all")
        canvas.create_image(0, 0, anchor=tk.NW, image=image)

    # Работа с отображением графиков
    def get_scatter_as_photoImage():
        global current_x_index, current_y_index,image
        fig = figure.Figure()
        ax = fig.add_subplot()
        part_df = df.drop(columns=['title', 'artist/s', 'key', 'mode', 'time_signature'])
        fig.supxlabel(part_df.columns[current_x_index])
        fig.supylabel(part_df.columns[current_y_index])
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


