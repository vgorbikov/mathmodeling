import numpy as np
import matplotlib.pyplot as pl


#################################################################
# Значения коэффициентов полинома, при которых он имеет решение #
#################################################################
a0 = -1
b0 = -2
c0 = 3
d0 = 4
#################################################################



def get_func(a, b, c, d):
    """
    Возвращает полином 3й степени с заданными коэффициентами
    """
    return lambda x: a*x**3 + b*x**2 + c*x + d


def get_der_func(a, b, c, d):
    """
    Возвращает производную полинома 3й степени с заданными коэффициентами
    """
    return lambda x: 3*a*x**2 + 2*b*x + c


def get_der_fi(a, b, c, d):
    return lambda x: (3*a*x**2 + 2*b*x + c)*0.1 + 1



def sign(x):
    """
    Определение знака числа

    Возвращает -1, если число меньше ноля 
    Возвращает 1, если чисто больше ноля 
    """
    return x/abs(x)



def dichotomy_method(f, a: float, b: float, ep: float, max_it: int):
    """
    Метод дихотомии
    Находит точки на интервале [a, b], в которых функция f принимает значения 0

    f: функция f(x)
    a, b: интервал локализации
    ep: точность решения
    max_it: предельное число итераций
    """
    if f(a) == 0:
        return a
    if f(b) == 0:
        return b
    i = 0
    dx = abs(b - a)
    x0 = (a + b)/2
    while (dx > 2*ep) and (i < max_it):
        if f(x0) == 0:
            return x0
        if sign(f(a)) != sign(f(x0)):
            b = x0
        if sign(f(b)) != sign(f(x0)):
            a = x0
        dx = abs(b - a)
        x0 = (a + b)/2
        i+=1
    return [x0, i] 



def chord_method(f, a: float, b: float, ep: float, max_it: int):
    """
    Метод хорд

    f: функция f(x)
    a, b: интервал локализации
    ep: точность решения
    max_it: предельное число итераций
    """
    def cross(la, lb):
        return la - (lb - la)*f(la)/(f(lb) - f(la))

    if f(a) == 0:
        return a
    if f(b) == 0:
        return b
    i = 0
    dx = abs(b - a)
    x0 = cross(a, b)
    while (dx > 2*ep) and (i < max_it):
        if f(x0) == 0:
            return x0
        if sign(f(a)) != sign(f(x0)):
            b = x0
        if sign(f(b)) != sign(f(x0)):
            a = x0
        dx = abs(b - a)
        x0 = cross(a, b)
        i+=1
    return [x0, i] 



def condit_simpleit(a: float, b: float, ):
    """
    Определяет, выполняются ли условия сходимости метода простых итераций на интервале [a, b]
    """





def simpleit_method(f, x0, a: float, b: float, ep: float, max_it: int):
    """
    Метод простых итераций 

    fi: функция fi(x) для нахождения следующих приближений
    x0: Начальное приближение 
    a, b: интервал локализации
    ep: точность решения
    max_it: предельное число итераций
    """
    def fi(x):
        return f(x)*0.1 + x
    
    dx = abs(a-b)
    x = x0

    i = 0
    while (dx >= ep) and (i < max_it):
        new_x = fi(x)
        dx = abs(x - new_x)
        x = new_x
        i+=1
    return [x, i] 
        


def newtons_method(f, der_f, x0, a: float, b: float, ep: float, max_it: int):
    """
    Метод Ньютона

    f: функция f(x)
    der_f: производная f'(x)
    x0: Начальное приближение 
    a, b: интервал локализации
    ep: точность решения
    max_it: предельное число итераций
    """

    dx = abs(a-b)
    x = x0

    i = 0
    while (dx >= ep) and (i < max_it):
        new_x = x - f(x)/der_f(x)
        dx = abs(x - new_x)
        x = new_x
        i+=1
    return [x, i] 



f = get_func(a0, b0, c0, d0)



methods_names = [
    "Метод дихотомии",
    "Метод хорд",
    "Метод простых итераций",
    "Метод Ньютона (касательных)"
]

methods_realization = {
    "Метод дихотомии": dichotomy_method,
    "Метод хорд": chord_method,
    "Метод простых итераций": simpleit_method,
    "Метод Ньютона (касательных)": newtons_method
}



def default_or_current(str_inp, def_val):
    """
    Опозволяет установить значение ввода по умолачнию
    """
    if str_inp == '':
        return def_val
    else:
        return str_inp



def main_menu():
    # Настройки отображения графиков
    fig, ax = pl.subplots()
    ax.minorticks_on()
    ax.grid(which="major")
    ax.grid(which="minor", linestyle=':')
    ax.set_xlim([-5, 5])
    ax.set_ylim([-5, 5])

    def draw(f, a: float, b: float, step: float, label: str):
        """
        Рисует заданную функцию на указанном интервале
        """
        xs = np.arange(a, b, step)
        ys = [f(x) for x in xs]

        ax.plot(xs, ys, label=label)

    #значения по умолчанию
    df_acc = 0.0000001
    df_mi = 100
    df_x0 = 0

    print("<i>Введите q для выхода<i>")

    max_it = input("Введите максимальное число итераций [{}]: ".format(df_mi))
    if max_it != 'q': 
        max_it = int(default_or_current(max_it, df_mi))
    else: 
        return 0

    accuracy = float(default_or_current(input("Укажите желаемую точность [{}]: ".format(df_acc)), df_acc))

    ax.set_title("Определите интервалы локализации")
    draw(f, -4, 4, 0.1, "y = f(x)")
    draw(get_der_fi(a0, b0, c0, d0), -4, 4, 0.1, "fi'(x)")
    pl.show()

    intrvl = input("Укажите интервал локализации (левую и правую границу через пробел): ")
    intrvl = [float(i) for i in intrvl.split(" ")]
    
    st_x = float(default_or_current(input("Укажите начальное приближение корня [{}]: ".format(df_x0)), df_x0))

    print("Выберите метод решения:")
    for i in range(len(methods_names)):
        print("--- {} [{}]".format(methods_names[i], i))
    method = methods_names[int(input("[число]: "))]

    return  {"method": method,
             "x0": st_x,
             "interval": intrvl,
             "accuracy": accuracy,
             "max_iteration": max_it}



while True:
    params = main_menu()
    if  params == 0:
        break
    else:
        root = 0
        if (params["method"] == methods_names[0]) or (params["method"] == methods_names[1]):
            root, iters = methods_realization[params["method"]](
                f,
                params["interval"][0],
                params["interval"][1],
                params["accuracy"],
                params["max_iteration"] 
                )
        elif params["method"] == methods_names[2]:
            root, iters = methods_realization[params["method"]](
                f,
                params["x0"],
                params["interval"][0],
                params["interval"][1],
                params["accuracy"],
                params["max_iteration"] 
                )
        else: 
            root, iters = methods_realization[params["method"]](
                f,
                get_der_func(a0, b0, c0, d0),
                params["x0"],
                params["interval"][0],
                params["interval"][1],
                params["accuracy"],
                params["max_iteration"] 
                )


        print(
            """
            Метод: {}
            Интервал локализации: {intrvl}
            Начальное приближение: {}
            Точность: {}
            Максимальное число итераций: {}

            Корень на интервале {intrvl}: {}
            Найден за: {} итераций
            """.format(
                params["method"],
                params["x0"],
                params["accuracy"],
                params["max_iteration"],
                root,
                iters,
                intrvl = params["interval"]
            )
        )
