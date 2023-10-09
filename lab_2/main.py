import numpy as np
import matplotlib.pyplot as pl
from scipy import interpolate


class GraphData():
    """
    Структура для хранения и преобразования данных графика
    """
    def __init__(self, graphs_data: list[list]) -> None:
        # данные графиков, разделённые по осям
        self.graphs: list[list] = [[[point[0] for point in graph],[point[1] for point in graph]] for graph in graphs_data]
        self.sort_points()


    @classmethod
    def load_graphs(cls, path):
        """
        Метод для загрузки данных из файла
        """
        with open(path, "r") as f:
            data = f.read()
        return cls([[[float(num) for num in point.split(',')] for point in graph.split('\n')] for graph in data.split('\n===next===\n')])


    def sort_points(self):
        for graph in self.graphs:

            sorted = False
            while not sorted:
                sorted = True
                for i in range(len(graph[0])-1):
                    if graph[0][i] > graph[0][i+1]:
                        sorted = False
                        xtmp = graph[0][i]
                        ytmp = graph[0][i]
                        graph[0][i] = graph[0][i+1]
                        graph[0][i+1] = xtmp
                        graph[1][i] = graph[1][i+1]
                        graph[1][i+1] = xtmp



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
    """
    Возвращает интерполирующую функцию для точек (x1, x2, x3)
    """
    l = np.array([
        [x1**2, x1, 1.],
        [x2**2, x2, 1.],
        [x3**2, x3, 1.]
    ])
    r = np.array([y1, y2, y3])
    sol = np.linalg.solve(l, r)
    return lambda x: sol[0]*x**2 + sol[1]*x + sol[2]



def global_lagrange(x, xs: list, ys: list):
    """
    Возвращает значение функции в точке x
    Для рассчёта требует координаты всех опорных точек интерполяции
    """
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



intpl_methods_description = {
        0: "linear",
        1: "parabolic",
        2: "Lagrange",
        3: "Cube splain"
    }

intpl_mths = {
    0: inter_linear,
    1: inter_parabolic,
    2: inter_lagrange,
    3: inter_cube
}



def main_menu(g_count: int):
    print("Введите q для выхода\n<!>При выборе нескольких графиков, они отображаются в режиме наложения")
    graph_numbers = input("Введите номера графиков для отображения через пробел [0-{}]: ".format(g_count-1))
    if graph_numbers != 'q': 
        graph_numbers = [int(i) for i in graph_numbers.split(' ')]
    else: 
        return 0
    print("Выберите метод интерполяции:")
    for mth in intpl_methods_description.items():
        print("{} [{}]".format(mth[1], mth[0]))
    intpl_method = int(input("> "))
    return  {"gnums": graph_numbers,
             "method": intpl_method}



g = GraphData.load_graphs("g.txt")



while True:
    params = main_menu(g.graph_count)
    if  params == 0:
        break
    else:
        for gnum in params["gnums"]:
            pl.plot(*intpl_mths[params["method"]](g.graphs[gnum][0], g.graphs[gnum][1], 0.01))
            pl.scatter(g.graphs[gnum][0], g.graphs[gnum][1])
        pl.show()


pl.show()