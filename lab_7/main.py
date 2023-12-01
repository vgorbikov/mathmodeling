import numpy as np
import matplotlib.pyplot as plt

# Вариант 8
# y' = 0,2y + 0,3x^2 + 1,6
#y(0)=1
# Аналитическое решение: y = 84*e^(x/5) - (3/2)*x^2 - 15*x - 83


def dy(x: float, y: float):
    '''
    Возвращает значение производной функции в точке с координатами (x, y)
    '''
    return 0.2*y + 0.3*x**2 + 1.6


def handmade_solution(x: float):
    '''
    Реализация наалитического решения дифура
    '''
    return 84*np.e**(x/5) - 1.5*x**2 - 15*x - 83


def euler(x0: float, y0: float, dy: callable, a: float, b: float, step: float):
    '''
    Возвращает координаты точек для построения кривой численного решения дифференциального уравнения
    '''
    xs = [x0]
    ys = [y0]
    while xs[-1] < b:
        if xs[-1]+step > b:
            break
        ys.append(ys[-1] + dy(xs[-1], ys[-1])*step)
        xs.append(xs[-1]+step)
    return xs, ys


def runge_kutt(x0: float, y0: float, dy: callable, a: float, b: float, step: float):
    xs = [x0]
    ys = [y0]
    while xs[-1] < b:
        if xs[-1]+step > b:
            break
        k1 = dy(xs[-1], ys[-1])
        k2 = dy(xs[-1]+step/2, ys[-1]+k1*step/2)
        k3 = dy(xs[-1]+step/2, ys[-1]+step*k2/2)
        k4 = dy(xs[-1]+step, ys[-1]+step*k3)
        ys.append(ys[-1]+step*(k1+2*k2+2*k3+k4)/6)
        xs.append(xs[-1]+step)
    return xs, ys



print("Дано уравнение вида: y' = 0,2y + 0,3x^2 + 1,6")
print('С начальными условиями: y(0)=1')
print('Аналитическое решение: y = 84*e^(x/5) - (3/2)*x^2 - 15*x - 83')
print('Сравнительная таблица значений в точках от 0 до 2 с шагом 0.2:')

an_xs = [i*0.2 for i in range(0, 10 + 1)]
an_ys = [handmade_solution(x) for x in an_xs]
eu_xs, eu_ys = euler(0, 1, dy, 0, 2, 0.2)
rk_xs, rk_ys = runge_kutt(0, 1, dy, 0, 2, 0.2)

print('x | an | eu | r-k')
for i in range(11):
    print(f'{i*0.2} | {an_ys[i]} | {eu_ys[i]} | {rk_ys[i]}')

ax = plt.subplot()
ax.minorticks_on()
ax.grid(which='major', color='black')
ax.grid(which='minor', linestyle='--')
ax.plot(an_xs, an_ys, label='analytic', color='red')
ax.plot(eu_xs, eu_ys, label='euler', color='blue')
ax.plot(rk_xs, rk_ys, label='runge-kutt', color='green')
ax.legend()
plt.show()