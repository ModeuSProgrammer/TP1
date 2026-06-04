from pickle import FALSE

import datatest
from datetime import datetime
import io
import tkinter as tk
from tkinter import colorchooser
from matplotlib import figure
from PIL import Image, ImageTk, ImageGrab

df = datatest.df
part_df = df.drop(columns=['title', 'artist/s', 'key', 'mode', 'time_signature'])


def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"


# Глобальные выбранные значение x и y
current_x_index = 1
current_y_index = 2

# Цвет по умолчанию
red = 22
green = 1
blue = 62
color_hex = rgb_to_hex(red, green, blue)
color_code = color_hex
# Определяем нажал ли пользователь кнопку рисовать и координаты старта линии
draw_mode = False
prev_x, prev_y = None, None
# История линий всех и текущей
history = []
current_stroke = []


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
            exit_draw_mode(event)
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
            fig = figure.Figure(figsize=(6.6, 4.8),layout="constrained")
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
            x = canvas.winfo_rootx()
            y = canvas.winfo_rooty()
            w = canvas.winfo_width()
            h = canvas.winfo_height()
            img = ImageGrab.grab(
                bbox=(x, y, x + w, y + h)
            )
            img.save(filename)
            # fig.savefig(filename)

        # Действие с цветами
        def color_click():
            global color_code
            color_data = colorchooser.askcolor(title="Выберите цвет")
            if color_data[1]:
                color_code = color_data[1]
                color_button.config(bg=color_code)

        # Переход в режим рисования
        def drawing_mode():
            global draw_mode
            if not draw_mode:
                draw_mode = True
                btn_draw.config(relief=tk.SUNKEN, bg="darkgray")
                canvas.config(cursor="pencil")
            else:
                draw_mode = False
                btn_draw.config(relief=tk.RAISED, bg="SystemButtonFace")
                canvas.config(cursor="")

        # Нанесение линии в виде квадрата
        def draw(event):
            global prev_x, prev_y, draw_mode, current_stroke
            if not draw_mode:
                return
            try:
                size = int(borderwidth_spin.get())
            except ValueError:
                size = 6
            half = size // 2
            rect_id = canvas.create_rectangle(
                event.x - half,
                event.y - half,
                event.x + half,
                event.y + half,
                fill=color_code,
                outline=color_code
            )
            current_stroke.append(rect_id)
            prev_x, prev_y = event.x, event.y

        # Заканчиваем рисунок
        def stop_draw(event):
            global prev_x, prev_y, history, current_stroke
            if draw_mode and current_stroke:
                history.append(current_stroke)
            prev_x, prev_y = None, None

        # Отменяем действие
        def undo_lines(event=None):
            global history
            if event:
                if event.char not in ['\x1a', 'z', 'Z', 'я', 'Я'] and event.keysym not in ['z', 'Z']:
                    return
            if history:
                last_line = history.pop()
                for line_id in last_line:
                    canvas.delete(line_id)

        def exit_draw_mode(event):
            global draw_mode
            draw_mode = False
            btn_draw.config(relief=tk.RAISED, bg="SystemButtonFace")
            canvas.config(cursor="")

        window = tk.Tk()

        # Фрейм для меню сверху
        top_frame = tk.Frame(window)
        top_frame.pack(side=tk.TOP, fill=tk.X)
        # Верхнее меню рисование
        color_button = tk.Button(top_frame, bg=color_code, width=3, height=1, command=color_click)
        color_button.pack(side=tk.RIGHT, padx=(0, 25))
        color_label = tk.Label(top_frame, text="Цвет:", padx=5, pady=5)
        color_label.pack(side=tk.RIGHT)
        # Толщина по умолчанию для id = 6
        borderwidth_spin = tk.Spinbox(top_frame, width=5, from_=1, to=100)
        borderwidth_spin.delete(0, "end")
        borderwidth_spin.insert(0, 6)
        borderwidth_spin.pack(side=tk.RIGHT)
        borderwidth_label = tk.Label(top_frame, text="Толщина:", padx=5, pady=5)
        borderwidth_label.pack(side=tk.RIGHT)
        # Кнопка для того чтобы взять карандаш
        btn_draw = tk.Button(top_frame, text="Рисование", padx=5, pady=5, command=drawing_mode)
        btn_draw.pack(side=tk.RIGHT)

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

        canvas = tk.Canvas(width=660, height=480)
        canvas.pack(side=tk.LEFT)

        # Добавление изображение графика при иницилизации приложения
        image = get_scatter_as_photoimage()
        canvas.create_image(0, 0, anchor=tk.NW, image=image)

        # Следит за тем какие кнопки с каким событием
        canvas.bind("<Button-1>", draw)
        canvas.bind("<B1-Motion>", draw)
        canvas.bind("<ButtonRelease-1>", stop_draw)
        canvas.bind("<Button-3>", exit_draw_mode)

        # Отменяет действие
        window.bind("<Control-Key>", undo_lines)

        window.resizable(False, False)
        window.mainloop()
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


if __name__ == "__main__":
    app()
