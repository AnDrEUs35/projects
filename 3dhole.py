import numpy as np 
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import imageio
import os


# Определяем переменую величину
frames = 2000
seconds_in_year = 365* 24 * 60 * 60
years = 5
t = np.linspace(0, years*seconds_in_year, frames)
plt.style.use('dark_background')


# Определяем функцию для диф.уравнений

def move_func(s, t):
    (x1, v_x1, y1, v_y1, z1, v_z1) = s

    dx_dt1 = v_x1
    dv_xdt1 = - G * m * x1 / (x1**2 + y1**2 + z1**2) **1.5 * A * (np.exp(B * np.sqrt(x1**2 + y1**2  + z1**2)))
    dydt1 = v_y1
    dy_ydt1 = - G * m * y1 / (x1**2 + y1**2 + z1**2) **1.5 * A * (np.exp(B * np.sqrt(x1**2 + y1**2  + z1**2)))
    dzdt1 = v_z1
    dv_zdt1 = - G * m * z1 / (x1**2 + y1**2 + z1**2) **1.5 * A * (np.exp(B * np.sqrt(x1**2 + y1**2  + z1**2)))

    return (dx_dt1, dv_xdt1, dydt1, dy_ydt1, dzdt1, dv_zdt1)

G = 6.67 * 10**(-11)
m = 1.98 * 10**(30)
A = 2.55
B = 149 * 10**(-14)


x01 = 149 * 10**9
v_x01 = 0
y01 = 0.1
v_y01 = 30000
z01 = 10
v_z01 = 30000

backgrounds_colors = ['black']

s0 = (x01, v_x01, y01, v_y01, z01, v_z01)
sol = odeint(move_func, s0, t)

# Решение диф. Уравнения
def solve_func(i, key):
    if key == 'point':
        x1 = sol[i, 0]
        y1 = sol[i, 2]
        z1 = sol[i, 4]
    else:
        x1 = sol[:i, 0]
        y1 = sol[:i, 2]
        z1 = sol[:i, 4]

    return ((x1, y1), (z1, ))

# Строим график

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

ball1, = plt.plot([], [], [], 'o', color='b')
ball_line1, = plt.plot([], [], [], '-', color = 'b')


plt.plot([0], [0], [0], 'o', color='black', ms=20)

def animate(i):
    ball1.set_data(solve_func(i, 'point')[0])
    ball1.set_3d_properties(solve_func(i, 'point')[1])
    ball_line1.set_data(solve_func(i, 'line')[0])
    ball_line1.set_3d_properties(solve_func(i, 'line')[1])




ani = FuncAnimation(fig, animate, frames=frames, interval=30)

plt.axis('equal')
edge = 2*x01
ax.set_xlim3d(-edge, edge)
ax.set_ylim3d(-edge, edge)
ax.set_zlim3d(-edge, edge)
ani.save('3dhole.gif')
