import numpy as np
import matplotlib.pyplot as pl



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


    @property
    def graph_count(self):
        return len(self.graphs)



def main_menu(g_count: int):
    print("Введите q для выхода\n<!>При выборе нескольких графиков, они отображаются в режиме наложения")
    return input("Введите номера графиков для отображения через пробел [0-{}]: ".format(g_count-1))    



g = GraphData.load_graphs("g.txt")

while True:
    choice = main_menu(g.graph_count)
    if  choice == "q":
        break
    else:
        for n in [int(i) for i in choice.split(' ')]:
            pl.scatter(g.axis_separated_graphs[n][0], g.axis_separated_graphs[n][1])
        pl.show()