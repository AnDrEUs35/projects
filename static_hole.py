import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Функция, описывающая дифференциальное уравнение движения по архимедовой спирали
def archemedean_spiral_equation(s, t, a, b):
    # Распаковываем текущие координаты и скорости
    x, y, vx, vy = s
    
    # Вычисляем радиус спирали в момент времени t
    r = a + b * t
    
    # Производные координат по времени
    dxdt = vx
    dydt = vy
    d2xdt2 = -a * vx / r
    d2ydt2 = -a * vy / r
    
    return [dxdt, dydt, d2xdt2, d2ydt2]

# Начальные условия
s0 = [0, 0, 1, 0]  # Начальные координаты (x, y) и скорости (vx, vy)

# Временной интервал
t = np.linspace(0, 10, 1000)

# Параметры архимедовой спирали
a = 0.5  # Параметр 'a' архимедовой спирали
b = 0.1  # Параметр 'b' архимедовой спирали

# Решаем дифференциальное уравнение
sol = odeint(archemedean_spiral_equation, s0, t, args=(a, b))

# Графическое представление результата
plt.figure(figsize=(6, 6))
plt.plot(sol[:, 0], sol[:, 1], label='Траектория движения по архимедовой спирали')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Движение по архимедовой спирали')
plt.legend()
plt.grid(True)
plt.axis('equal')
