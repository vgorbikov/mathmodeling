import random
import itertools
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


normalise = [random.random() for i in range(1000)]



def get_dens_bins(values: list, bins_count: int):
    """
    Возвращает список значений и список накопленных весов для построения гистограммы
    """
    cor = 0
    hist_values = []
    weights = []
    n = len(values)

    values = sorted(values)
    a = (1-cor)*values[0]
    b = (1+cor)*values[-1]
    d = (1 + cor)*(values[-1] - values[0])
    dx = d/bins_count

    for i in range(1, bins_count+1):
        di = (a+(i-1)*dx, a+i*dx)
        hist_values.append(a+(i-0.5)*dx)
        k_i = 0
        for v in values:
            if v>di[0] and v<di[1]:
                k_i += 1
            if v>di[1]:
                break
        weights.append(k_i/(n*dx))

    return hist_values, weights



def get_dist_bins(values: list, bins_count: int):
    cor = 0
    values = sorted(values)

    n = len(values)
    d = (1 + cor)*(values[-1] - values[0])
    dx = d/bins_count
    vals, wghts = get_dens_bins(values, bins_count)
    dist_wghts = []

    k_q = 0
    for i in range(0, len(vals)):
        k_i = wghts[i]*n*dx
        k_q += k_i
        dist_wghts.append(k_q/n)

    return vals, dist_wghts



def equal_inverse(count: int, a: float, b: float):
    """
    Возвращает count равнорасперделённых на интервале (a, b) случайных значений
    """
    values = [random.random() for i in range(count)]
    def inver_func(r):
        return r*(b-a)+a

    return [inver_func(x) for x in values]



def gauss_clt(count: int, mu: float, sig: float):
    """
    Возвращает count нормально распределённых на интервале случайных значений
    Можно задать матожидание и среднеквадратичное отклонение
    """
    n = 12
    vals = []
    for i in range(count):
        vi = sum([random.random() for i in range(n)])
        vals.append((vi*(12/n)-6)*sig+mu)
    return vals



def reley_neuman(count: int, sig: float):
    """
    Возвращает count случайных значений, распределённыз по рэлеевскому закону
    Можно указать моду
    """
    def w(x):
        return (x/sig**2)*np.e**(-1*(x**2)/(2*sig**2))
    
    values = []
    a = 0
    b = 4*sig
    m = w(sig)

    def g(x):
        return 0.8*w(x)

    while len(values)<count:
        ri = random.random()
        rj = random.random()
        x = a + (b - a)*ri
        y = m*rj
        if y<=g(x):
            values.append(x)
    
    return values



theory_graphs = {
    "density":{
        "equal": stats.uniform.pdf,
        "gauss": stats.norm.pdf,
        "reley": stats.rayleigh.pdf
    },
    "distribution": {
        "equal": stats.uniform.cdf,
        "gauss": stats.norm.cdf,
        "reley": stats.rayleigh.cdf
    }
}



def get_volume():
    while True:
        count = input("Укажите объём выборки [10^4]:")
        if count == '':
            count = 10000
        try:
            count = int(count)
            return count
        except:
            print("<!>Необходимо ввести целое число<!>")



def get_bins_count():
    while True:
        count = input("Укажите количество интервалов группировки [21]:")
        if count == '':
            count = 21
        try:
            count = int(count)
            return count
        except:
            print("<!>Необходимо ввести целое число<!>")
        


def eq_menu():
    print("<i>Равномерное распределение<i>")
    a, b = (int(num) for num in input("Укажите параметры <a> и <b> через пробел: ").split(' '))
    count = get_volume()
    bins_count = get_bins_count()

    def norm(x):
        if x>b:
            return 1
        if x<=a:
            return 0
        return (x-a)/(b-a)
    
    def norm_dense(x):
        if x>=b:
            return 0
        if x<=a:
            return 0
        return 1/(b-a)

    eq_vals = equal_inverse(count, a, b)
    dens_vals, dens_weights = get_dens_bins(eq_vals, bins_count=bins_count)
    plt.figure(1)
    plt.title("Эмпирическая и теоритическая плотность")
    plt.hist(dens_vals, 
             weights=dens_weights, 
             bins=len(dens_vals),
             label='Эмпирическая плотность')
    xs = np.arange(a-1, b+1, 0.01)
    dens_ys = [norm_dense(x) for x in xs]
    plt.plot(xs, dens_ys, label="Теоретическая плотность")
    plt.legend()

    dist_vals, dist_weights = get_dist_bins(eq_vals, bins_count=bins_count)
    plt.figure(2)
    plt.title("Эмпирическая и теоритическая функция распределения")
    plt.hist(dist_vals, 
             weights=dist_weights, 
             bins=len(dist_vals),
             label="Полигон накопленных частот")
    dist_ys = [norm(x) for x in xs]
    plt.plot(xs, dist_ys, label="Теоретическое распределение")
    plt.legend()

    plt.show()



def gauss_menu():
    print("<i>Нормальное распределение<i>")
    mu, sig = (int(num) for num in input("Укажите параметры <mu> и <sigma> через пробел: ").split(' '))
    count = get_volume()
    bins_count = get_bins_count()
    gauss_vals = gauss_clt(count, mu, sig)

    dens_vals, dens_weights = get_dens_bins(gauss_vals, bins_count=bins_count)
    plt.figure(1)
    plt.title("Эмпирическая и теоритическая плотность")
    plt.hist(dens_vals, 
             weights=dens_weights, 
             bins=len(dens_vals),
             label='Эмпирическая плотность')
    xs = np.arange(mu-4*sig, mu+4*sig, 0.01)
    dens_ys = stats.norm.pdf(xs, mu, sig)
    plt.plot(xs, dens_ys, label="Теоретическая плотность")

    dist_vals, dist_weights = get_dist_bins(gauss_vals, bins_count=bins_count)
    plt.figure(2)
    plt.title("Эмпирическая и теоритическая функция распределения")
    plt.hist(dist_vals, 
             weights=dist_weights, 
             bins=len(dist_vals),
             label="Полигон накопленных частот")
    dist_ys = stats.norm.cdf(xs, mu, sig)
    plt.plot(xs, dist_ys, label="Теоретическое распределение")

    plt.show()



def reley_menu():
    print("<i>Рэлеевское распределение<i>")
    sig = int(input("Укажите параметр <sigma>: "))
    count = get_volume()
    bins_count = get_bins_count()
    reley_vals = reley_neuman(count, sig)

    dens_vals, dens_weights = get_dens_bins(reley_vals, bins_count=bins_count)
    plt.figure(1)
    plt.title("Эмпирическая и теоритическая плотность")
    plt.hist(dens_vals, 
             weights=dens_weights, 
             bins=len(dens_vals),
             label='Эмпирическая плотность')
    xs = np.arange(0, 4*sig, 0.01)
    dens_ys = stats.rayleigh.pdf(xs, 0, sig)
    plt.plot(xs, dens_ys, label="Теоретическая плотность")

    dist_vals, dist_weights = get_dist_bins(reley_vals, bins_count=bins_count)
    plt.figure(2)
    plt.title("Эмпирическая и теоритическая функция распределения")
    plt.hist(dist_vals, 
             weights=dist_weights, 
             bins=len(dist_vals),
             label="Полигон накопленных частот")
    dist_ys = stats.rayleigh.cdf(xs, 0, sig)
    plt.plot(xs, dist_ys, label="Теоретическое распределение")

    plt.show()



def menu():
    type_menu = {
        0: ("Равномерное распределение", eq_menu),
        1: ("Нормальное распределение", gauss_menu),
        3: ("Рэлеевское распределение", reley_menu)
    }

    while True:
        print("Выберите распределение:")
        for tp in type_menu.items():
            print("\t- {} [{}]".format(tp[1][0], tp[0]))
        type = int(input("> "))
        type_menu[type][1]()

menu()



