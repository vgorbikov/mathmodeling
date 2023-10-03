import numpy as np
import matplotlib.pyplot as pl
from scipy import interpolate
# from lab1.main import GraphData


class GraphData():
    """
    Структура для хранения и преобразования данных графика
    """
    def __init__(self, graphs_data: list[list]) -> None:
        self.graphs: list[list] = graphs_data
        # данные графиков, разделённые по осям
        self.axis_separated_graphs: list[list] = [[[point[0] for point in graph],[point[1] for point in graph]] for graph in self.graphs]


    @classmethod
    def load_graphs(cls, path):
        """
        Метод для загрузки данных из файла
        """
        with open(path, "r") as f:
            data = f.read()
        return cls([[[float(num) for num in point.split(',')] for point in graph.split('\n')] for graph in data.split('\n===next===\n')])


    def sort_points(self):
        pass


    @property
    def graph_count(self):
        return len(self.graphs)
    



def piece_linear(x1: int, x2: int, y1: int, y2: int):
    """
    Возвращает интерполирующую функцию для промежутка (x1, x2)
    """
    a = (y2-y1)/(x2-x1)
    b = y1 - a*x1
    return lambda x: a*x + b



def piece_parabolic(x1, x2, x3, y1, y2, y3):
    l = np.array([
        [x1**2, x1, 1.],
        [x2**2, x2, 1.],
        [x3**2, x3, 1.]
    ])
    r = np.array([y1, y2, y3])
    sol = np.linalg.solve(l, r)
    return lambda x: sol[0]*x**2 + sol[1]*x + sol[2]



def global_lagrange(x, xs: list, ys: list):
    l = 0
    for i in range(len(xs)):
        top = 1
        down = 1
        for j in range(len(xs)):
            if j != i:
                top *= x - xs[j]
                down *= xs[i] - xs[j]
        l += ys[i]*(top/down)
    return l



def inter_linear(xs: list, ys: list, step: int):
    """
    Принимает массив x-координат и y-координат
    Возвращает массив из двух массивов вида [[x], [y]]
    Выходной массив дополнен промежуточными точками
    """
    inter_xs = []
    inter_ys = []

    for i in range(0, len(xs)-1):
        inter_func = piece_linear(xs[i], xs[i+1], ys[i], ys[i+1])
        xn = xs[i]
        while xn < xs[i+1]:
            inter_xs.append(xn)
            inter_ys.append(inter_func(xn))
            xn += step
    return [inter_xs, inter_ys]



def inter_parabolic(xs: list, ys: list, step: int):
    inter_xs = []
    inter_ys = []

    inter_func = piece_parabolic(xs[0], xs[1], xs[2], ys[0], ys[1], ys[2])
    cpn = 1
    xn = xs[0]
    while xn < xs[-1]:
        if cpn != len(xs) - 2:
            if xn >= xs[cpn + 1] - 0.5*(xs[cpn + 1] - xs[cpn]):
                cpn += 1
                inter_func = piece_parabolic(xs[cpn-1], xs[cpn], xs[cpn+1], ys[cpn-1], ys[cpn], ys[cpn+1])
        inter_xs.append(xn)
        inter_ys.append(inter_func(xn))
        xn += step
    return [inter_xs, inter_ys]



def inter_lagrange(xs: list, ys: list, step):
    inter_xs = []
    inter_ys = []

    xn = xs[0]
    while xn < xs[-1]:
        inter_xs.append(xn)
        inter_ys.append(global_lagrange(xn, xs, ys))
        xn += step
    return [inter_xs, inter_ys]



def inter_cube(xs, ys, step):
    inter_xs = []
    inter_ys = []

    ks = interpolate.splrep(xs, ys)

    xn = xs[0]
    while xn < xs[-1]:
        inter_xs.append(xn)
        inter_ys.append(interpolate.splev(xn, ks))
        xn += step
    return [inter_xs, inter_ys]



xs = [1, 2, 3, 4, 5, 6, 7, 8]
ys = [0, 3, 5, 6, 6, 8, 3, 2]

# xs = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
# ys = [1/np.cos(x) for x in xs]



# pl.plot(*inter_linear(xs, ys, 0.01))
pl.plot(*inter_parabolic(xs, ys, 0.01))
# pl.plot(*inter_lagrange(xs, ys, 0.01))
# pl.plot(*inter_cube(xs, ys, 0.01))
pl.scatter(xs, ys)


def main_menu(g_count: int):
    print("Введите q для выхода\n<!>При выборе нескольких графиков, они отображаются в режиме наложения")
    return input("Введите номера графиков для отображения через пробел [0-{}]: ".format(g_count-1))    



# g = GraphData.load_graphs("g.txt")

# while True:
#     choice = main_menu(g.graph_count)
#     if  choice == "q":
#         break
#     else:
#         for n in [int(i) for i in choice.split(' ')]:
#             pl.scatter(g.axis_separated_graphs[n][0], g.axis_separated_graphs[n][1])
#         pl.show()

pl.show()