# Вариант 8
# Найти максимум f(x) = x*e^(-x)

import numpy as np
import matplotlib.pyplot as plt
from enum import Enum



def opt_8(x: float):
    '''
    xe^(-x)\n
    Исследуемая функция: вариант 8
    '''
    return x*np.e**(-x)



def feb_gen(n: int):
    '''
    Генератор последовательности Фибоначчи
    '''
    def gen():
        num = 1
        pre_num = 0
        i = 0
        while i<n:
            yield num
            i += 1
            tmp = num
            num += pre_num
            pre_num = tmp
    return gen()



def sh_graph(f, a: float, b: float, dx: float):
    '''
    Вывод графика f(x)
    Указывается интервал отрисовки и шаг рассчёта
    '''
    plt.minorticks_on()
    plt.grid(which='major', color='black')
    plt.grid(which='minor', linestyle='--')

    xs = np.arange(a, b, dx)
    ys = [f(x) for x in xs]
    plt.plot(xs, ys)
    plt.show()



def dchm_method(f, a: float, b: float, ep: float) -> dict:
    '''
    Найти максимум функции f(x) по методу дихотомии\n
    Для поиска минимума, передайте функцию -f(x)
    '''

    n = 0

    while ((b-a)>ep):
        n += 1

        xl = (a+b)/2 - ep/2
        xr = (a+b)/2 + ep/2
        yl = f(xl)
        yr = f(xr)

        if yl<yr:
            a = xl
        elif yr<yl:
            b = xr
        else:
            a = xl
            b = xr
            break

    return {
        "xm": (a+b)/2,
        "ym": f((a+b)/2),
        "iterations_count": n
    }



def gr_method(f, a: float, b: float, ep: float) -> dict:
    '''
    Найти максимум функции f(x) по методу золотого сечения\n
    Для поиска минимума, передайте функцию -f(x)
    '''

    t = round(2/(1 + np.sqrt(5)), 10)

    xl = b - (b-a)*t
    xr = a + (b-a)*t
    yl = f(xl)
    yr = f(xr)
    
    n = 0

    while ((b-a)>ep):
        n += 1
        
        if yl<yr:
            a = xl
            xl = xr
            yl = yr
            xr = a + (b-a)*t
            yr = f(xr)
        elif yr<yl:
            b = xr
            xr = xl
            yr = yl
            xl = b - (b-a)*t
            yl = f(xl)
        else:
            a = xl
            b = xr
            xl = b - (b-a)*t
            xr = a + (b-a)*t
            yl = f(xl)
            yr = f(xr)

    return {
        "xm": (a+b)/2,
        "ym": f((a+b)/2),
        "iterations_count": n
    }



def fbn_method(f, a: float, b: float, n: int) -> dict:
    '''
    Найти максимум функции f(x) по методу Фибоначчи\n
    Для поиска минимума, передайте функцию -f(x)
    '''
    i = 1
    fnums = [float(i) for i in feb_gen(n+1)]

    l = (b-a)

    xl = a + (fnums[-3]/fnums[-1])*l
    xr = a + (fnums[-2]/fnums[-1])*l
    yl = f(xl)
    yr = f(xr)

    while (i<=n-1):
        if yl<yr:
            a = xl
            l = (b-a)
            xl = xr
            yl = yr
            xr = a + (fnums[-i-1]/fnums[-i])*l
            yr = f(xr)
        elif yr<yl:
            b = xr
            l = (b-a)
            xr = xl
            yr = yl
            xl = a + (fnums[-i-2]/fnums[-i])*l
            yl = f(xl)
        else:
            a = xl
            b = xr
            l = (b-a)
            xl = a + (fnums[-3]/fnums[-1])*l
            xr = a + (fnums[-2]/fnums[-1])*l
            yl = f(xl)
            yr = f(xr)
        i += 1

    return {
        "xm": (a+b)/2,
        "ym": f((a+b)/2),
        "accuracy": b - a
    }


# print(dchm_method(opt_8, -1, 2, 0.1))
# print(gr_method(opt_8, -1, 2, 0.0000001))
# print(fbn_method(opt_8, -1, 2, 31))


def get_interval():
    inp = input("Введите границы интервала (через пробел): ").split(" ")
    return float(inp[0]), float(inp[1])


def get_accuracy():
    inp = input("Введите желаемую точность [10^-3]: ")
    if inp == '':
        inp = 0.001
    return float(inp)


def get_itercount():
    inp = input("Введите количество итераций [22]: ")
    if inp == '':
        inp = 22
    return int(inp)


###############################
######## Сценарий меню ########
###############################

class Methods(Enum):
    DCH = 0
    GR = 1
    FBN = 2

methods = {
        "Метод дихотомии": Methods.DCH.value,
        "Метод золотого сечения": Methods.GR.value,
        "Метод Фибоначчи": Methods.FBN.value
    }

while True:
    sh_graph(opt_8, -1, 4, 0.01)
    print("Выберите метод оптимизации:")
    for itm in methods.items():
        print(f"\t- {itm[0]} [{itm[1]}]")

    try:
        meth = int(input(">: "))
    except:
        break

    match meth:
        case Methods.DCH.value:
            intrvl = get_interval()
            acc = get_accuracy()
            print(dchm_method(opt_8, intrvl[0], intrvl[1], acc))
        case Methods.GR.value:
            intrvl = get_interval()
            acc = get_accuracy()
            print(gr_method(opt_8, intrvl[0], intrvl[1], acc))
        case Methods.FBN.value:
            intrvl = get_interval()
            n = get_itercount()
            print(fbn_method(opt_8, intrvl[0], intrvl[1], n))
        case _:
            print("ohh")
            break


