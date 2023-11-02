# ВАРИАНТ 8:
# f(x) = cos(x), [-1, 1.5]
#Вычисленное (вручную) значение: 1.83896597
#Ф(2.98) - 4.9856

import random
import numpy as np
import matplotlib.pyplot as plt



def show_graph(f, a, b):
    xs = np.arange(a, b, 0.01)
    ys = [f(x) for x in xs]

    plt.plot(xs, ys)
    plt.show()



def trapezoid_method(f, a, b):
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
    
    return S



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
    n = len(i)
    i_mid = sum(i)/n
    sig = np.sqrt(sum([(ii - i_mid)**2 for ii in i ])/n)
    return sig



def define_delta(sigma: float, gamma: float, n: int):
    2.98*sigma/np.sqrt(n)

