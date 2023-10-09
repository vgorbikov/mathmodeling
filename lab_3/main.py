import numpy as np
import matplotlib.pyplot as pl
import random


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



def calculate_coeffs(xs: list, ys: list, degree: int):
    """
    Возвращает массив с коэффициентами, найдеными по методу наименьших квадратов
    """
    points_count = len(xs)
    lm = []
    rm = []
    for i in range(degree+1):
        lmstring = []
        for j in range(degree+1):
            lmstring.append(sum([x**(i+j) for x in xs]))
        lm.append(lmstring)
        rm.append(sum([ys[j]*(xs[j]**i) for j in range(points_count)]))
    l = np.array(lm)
    r = np.array(rm)
    return np.linalg.solve(l, r)



def create_poly(deg: int, coeffs: list):
    """
    Строит функцию полинома заданной степени

    deg: степень полинома
    coeffs: список коэффициентов
    """
    if len(coeffs) != (deg + 1):
        raise ValueError("Полином степени {} должен содержать {} коэффициентов".format(deg, deg+1))
    
    def poly(x: float):
        # sum = 0
        # for i in range(deg+1):
        #     sum += coeffs[i]*(x**i)

        # return sum
        sum = coeffs[-1]*x + coeffs[-2]
        for i in range(deg-2, -1, -1):
            sum = sum*x + coeffs[i]
        return sum

    return poly



def poly_noised_points(xstart: int, xstop: int, coeffs: list, deg: int, spread: float = 0):
    """
    Возвращает точки для вывода полинома заданной степени с заданным шумом
    """
    x = np.arange(xstart, xstop, 0.5)
    y = np.empty((len(x), 1))
    noise = np.empty((len(x), 1))

    for i in range(len(x)):
        noise[i] = random.gauss(0.0, spread)
        p = create_poly(deg, coeffs)
        y[i] = p(x[i]) + noise[i]

    return x, y



def sqsum_error(poly, xs, ys):
    sum = 0
    for i in range(len(xs)):
        sum += (ys[i]-poly(xs[i]))**2
    return sum



def main_menu(g_count: int):
    print("Введите q для выхода\n<!>При выборе нескольких графиков, они отображаются в режиме наложения")
    graph_numbers = input("Введите номера графиков для отображения через пробел [0-{}]: ".format(g_count-1))
    if graph_numbers != 'q': 
        graph_numbers = [int(i) for i in graph_numbers.split(' ')]
    else: 
        return 0
    deg = int(input("Укажите степень полинома: "))
    return  {"gnums": graph_numbers,
             "degree": deg}



g = GraphData.load_graphs("g.txt")



while True:
    params = main_menu(g.graph_count)
    if  params == 0:
        break
    else:
        for gnum in params["gnums"]:
            graph = g.graphs[gnum]
            cfs = calculate_coeffs(graph[0], graph[1], params["degree"])

            poly = create_poly(params["degree"], cfs)
            intr_x = np.arange(graph[0][0], graph[0][-1], 0.1)
            intr_y = [poly(x) for x in intr_x]

            pl.plot(intr_x, intr_y)
            pl.scatter(g.graphs[gnum][0], g.graphs[gnum][1])

            print("Суммарная ошибка: {}".format(sqsum_error(poly, graph[0], graph[1])))
        pl.show()

