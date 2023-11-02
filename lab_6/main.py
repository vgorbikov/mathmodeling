# ВАРИАНТ 8:
# f(x) = cos(x), [-1, 1.5]
#Вычисленное (вручную) значение: 1.83896597
#Ф(2.98) - 4.9856

import random
import numpy as np
import matplotlib.pyplot as plt



def show_graph(f, a, b):
    """
    Выводит график функции f на промежутке [a, b]
    """
    xs = np.arange(a, b, 0.01)
    ys = [f(x) for x in xs]

    plt.plot(xs, ys)
    plt.show()



def trapezoid_method(f, a, b):
    """
    Возвращает значение интеграла функции f в пределах от a до b, найденное по методу трапеций
    """
    xs = np.arange(a, b, abs(b-a)/100)
    ys = [f(x) for x in xs]
    M = max(ys)
    N = round(np.sqrt(100*M*abs(b-a)**3/12)) + 1
    step = abs(b-a)/N

    S = 0
    for i in range(N):
        htop = f(a + step*i)
        hbot = f(a + step*(i+1))
        S += (htop+hbot)*step/2
    
    return S, N



def m_k_method1(f, a: float, b: float, n: int):
    h = abs(b-a)
    eq_values = [h*random.random()+a for i in range(n)]
    values = [f(u) for u in eq_values]
    s = abs(b-a)*sum(values)/n
    return s



def m_k_method2(f, a: float, b: float, n: int):
    m = 1.2
    k = 0
    for i in range(n):
        x = a + (b-a)*random.random()
        y = m*random.random()
        if y < f(x):
            k+=1
    
    s = m*(b-a)*(k/n)
    return s



def define_sigma(i: list):
    """
    Определяет выборочное среднеквадратичное отклонение для выборки i
    """
    n = len(i)
    i_mid = sum(i)/n
    sig = np.sqrt(sum([(ii - i_mid)**2 for ii in i ])/(n-1))
    return sig



def define_delta_montekarlo(sigma: float, n: int):
    """
    Определяет относительную точность для метода монте-карло 
    по заданному выборочному среднеквадратичному отклонению sigma выборки из n его оценок
    """
    return 2.98*sigma/np.sqrt(n)






print("Дана функция f(x)=cos(x). Найдём интеграл от f(x) на интервале [-1, 1.5]\n")
print("Вычисленное (вручную) значение: 1.83896597\n")

tr_res = trapezoid_method(np.cos, -1, 1.5)
print(f'По методу трапеций:             {tr_res[0]}; δ < 1%; N={tr_res[1]}\n')

n_mk1 = 1000
d1_mk = 100
while d1_mk > 1:
    mk_1_res = [m_k_method1(np.cos, -1, 1.5, n_mk1) for i in range(100)]
    mk_1_sig = define_sigma(mk_1_res)
    d1_mk = define_delta_montekarlo(mk_1_sig, n_mk1)*100
    if d1_mk > 1:
        n_mk1 *= 10
print(f'По методу Монте-Карло (1 сп.):  {mk_1_res[0]}; δ = {d1_mk}%; σ* = {mk_1_sig}\n')

n_mk2 = 1000
d2_mk = 100
while d2_mk > 1:
    mk_2_res = [m_k_method1(np.cos, -1, 1.5, n_mk2) for i in range(100)]
    mk_2_sig = define_sigma(mk_2_res)
    d2_mk = define_delta_montekarlo(mk_2_sig, n_mk2)*100
    if d2_mk > 1:
        n_mk2 *= 10
print(f'По методу Монте-Карло (2 сп.):  {mk_2_res[0]}; δ = {d2_mk}%; σ* = {mk_2_sig}\n')

show_graph(np.cos, -1, 1.5)