# import re
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.image as mpimg
from matplotlib import cm
from matplotlib import use as plot_in_window

# кладём в корень что ли
FILE_PATH = 'printer.cfg'

# принудительно заставляем рисовать в окне TkAgg - это соотвествующий бэкенд
plot_in_window('TkAgg')

def load_data(path):
    mesh_data = []
    row = []
    line_count = 0

    with open(path, 'r') as file:
        in_points_section = False
        for line in file:
            if 'points =' in line:
                in_points_section = True
                continue
            #нашли mesh - считываем
            elif in_points_section:
                # нам нужны только эти 5 строк из файла
                if not line.startswith("#*#"):
                    break
                if  line_count > 4:
                    return mesh_data
                #оставляем без всякой фигни в начале
                line = line.strip().replace(',','').split(' ')[3:]
                try:
                    row = [float(x) for x in line]
                finally:
                    line_count += 1
                    if row:
                        mesh_data.append(row)

    if not mesh_data or line_count < 5:
        print("Файл не тот!")

    return False



def calculate_max_delta_absolute(data):
    max_height = np.max(data)
    min_height = np.min(data)
    max_delta = abs(max_height - min_height)
    return max_delta

def main_draw(data):
    # Создание сетки для координат
    x = np.arange(data.shape[1])
    y = np.arange(data.shape[0])
    X, Y = np.meshgrid(x, y)

    # Создание цветового градиента
    colors = ["#523a28", "#a47551", "#d0b49f", "#e4d4c8", "#f9f1f0"]
    # cmap = LinearSegmentedColormap.from_list("custom_cmap", colors)
    # cmap = cm.copper
    # cmap = cm.gist_earth
    cmap = cm.coolwarm
    # Создание 3D-графика
    # Ширина 10 дюймов, высота 6 дюймов
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, data, cmap=cmap, edgecolor='white', rstride=1, cstride=1)



    # Добавление цветовой шкалы
    fig.colorbar(surf, shrink=1, aspect=6)

    # Настройка осей
    ax.set_xlabel('X ось')
    ax.set_ylabel('Y ось')
    ax.set_zlabel('Высота')

    # Поворот графика вокруг оси Z
    ax.view_init(elev=70, azim=-120)

    # Загрузка изображения
    #img = mpimg.imread('F5MTable.png')

    # Добавление изображения в левый нижний угол

    xmin, xmax = 0, -0.05  # Для X координат
    ymin, ymax = -1, -0.05  # Для Y координат

    # Преобразование матрицы в строку для отображения без скобок
    # data_str = data_str.replace('[','').replace(']','').replace(',','')  # Удаляем квадратные скобки и запятые

    # Преобразование сетки высот в строку для отображения без скобок и с выравниванием
    data_str = ''
    data_rounded = np.round(data, 2)
    data_rounded_mirr = data_rounded[::-1]
    for row in data_rounded_mirr:
        # Форматирование каждого элемента с выравниванием по правому краю в поле шириной 8 символов
        row_str = ''.join(f'{value:>8.2f}' for value in row)
        data_str += row_str + '\n'


    # Задаем заголовок фигуры
    fig.suptitle('Mesh level F5M Adv', fontsize=16)  # Устанавливаем заголовок
    # Установка угла обзора
    ax.view_init(elev=70, azim=-135)

    delta = calculate_max_delta_absolute(data)
    # Установка заголовка графика с матрицей высот
    ax.text2D(-0.6, 0.4, f'MAX \u2206 - {delta} мм', color='red', transform=ax.transAxes, fontsize=12, verticalalignment='top')

    ax.text2D(-0.6, 0.3, f'Карта высот:\n ----------------------------------------------------------', \
              transform=ax.transAxes, fontsize=10, verticalalignment='top')
    ax.text2D(-0.6, 0.2, f'{data_str}', transform=ax.transAxes, fontsize=10, verticalalignment='top')
    ax.text2D(1.2, -0.1, f'автор - @kozyayur', transform=ax.transAxes, fontsize=10, verticalalignment='top',color='blue')

    # Установка заголовка окна
    fig.canvas.manager.set_window_title('Mesh level F5M Adv')

    # Выводим
    #ax.imshow(img, aspect='auto', extent=(xm   in, xmax, ymin, ymax), zorder=10)
    plt.show(block=True)

if __name__ == "__main__":
    data= load_data(FILE_PATH)
    if data:
        data = np.array(data)  # вот они роднинькие
        main_draw(data)
    else:
        print("Smth wrong")