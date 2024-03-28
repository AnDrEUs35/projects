import numpy as np 
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


plt.style.use('dark_background')
# Определяем переменую величину
frames = 365
seconds_in_year = 365* 24 * 60 * 60
years = 3
t = np.linspace(0, years*seconds_in_year, frames)

# Определяем функцию для диф.уравнений

def move_func(s, t):
    (x1, v_x1, y1, v_y1,
     x2, v_x2, y2, v_y2) = s

    dx_dt1 = v_x1
    dv_xdt1 = - G * m * x1 / (x1**2 + y1**2) **1.5 * A * (np.exp(B / np.abs(x1)))
    dydt1 = v_y1
    dy_ydt1 = - G * m * y1 / (x1**2 + y1**2) **1.5 * A * (np.exp(B / np.abs(y1)))


    dx_dt2 = v_x2
    dv_xdt2 = - G * m * x2 / (x2**2 + y2**2) **1.5
    dydt2 = v_y2
    dy_ydt2 = - G * m * y2 / (x2**2 + y2**2) **1.5


    return (dx_dt1, dv_xdt1, dydt1, dy_ydt1,
    dx_dt2, dv_xdt2, dydt2, dy_ydt2)

G = 6.67 * 10**(-11)
m = 1.98 * 10**(30)
A = 1.5
B = 149 * 10**(19)


x01 = 149 * 10**9
v_x01 = 0
y01 = 0.1
v_y01 = 30000

x02 = 0.1
v_x02 = -24130
y02 = 1.52 * 149 * 10**9
v_y02 = 0

s0 = (x01, v_x01, y01, v_y01, 
      x02, v_x02, y02, v_y02)
sol = odeint(move_func, s0, t)

# Решение диф. Уравнения
def solve_func(i, key):
    if key == 'point':
        x1 = sol[i, 0]
        y1 = sol[i, 2]

        x2 = sol[i, 4]
        y2 = sol[i, 6]
    else:
        x1 = sol[:i, 0]
        y1 = sol[:i, 2]

        x2 = sol[:i, 4]
        y2 = sol[:i, 6]
    return ((x1, y1), (x2, y2))

# Строим график

fig, ax = plt.subplots()

ball1, = plt.plot([], [], 'o', color='b')
ball_line1, = plt.plot([], [], '-', color = 'b')

ball2, = plt.plot([], [], 'o', color='r')
ball_line2, = plt.plot([], [], '-', color = 'r')

plt.plot([0], [0], 'o', color='white', ms=20)

def animate(i):
    ball1.set_data(solve_func(i, 'point')[0])
    ball_line1.set_data(solve_func(i, 'line')[0])

    ball2.set_data(solve_func(i, 'point')[1])
    ball_line2.set_data(solve_func(i, 'line')[1])

ani = FuncAnimation(fig, animate, frames=frames, interval=30)

plt.axis('equal')
edge = 6*x01
ax.set_xlim(-edge, edge)
ax.set_ylim(-edge, edge)
ani.save('black_hole.gif')