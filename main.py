import numpy as np 
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from initial_data import * 


plt.style.use('dark_background')
# Определяем переменую величину
frames = 730
seconds_in_year = 365 * 24 * 60 * 60
years = 2
t = np.linspace(0, years*seconds_in_year, frames)


#_____

accretion_disk_y =  [0, 0.5, 1, 0.5, 0]
accretion_disk_x = [-2, -1, 0, 1, 2]


a = 0.5
b = 0.1
# 
def move_func(s, t):
    x, vx, y, vy = s
    r = a + b * t

    dx_dt = vx
    dvx_dt = -a * x / r
    dy_dt = vy
    dvy_dt = -a * y / r

    return [dx_dt, dvx_dt, dy_dt, dvy_dt]

s0 = [x0_venus, v_x0_venus, y0_venus, v_y0_venus]

sol = odeint(move_func, s0, t)

def solve_func(i, key):
    if key == 'point':
        x1 = sol[i, 0]
        y1 = sol[i, 2]


    elif key == 'line':
        x1 = sol[:i, 0]
        y1 = sol[:i, 2]
        
    return (x1, y1)

fig, ax = plt.subplots()

ball1, = plt.plot([], [], 'o', color='b')
ball_line1, = plt.plot([], [], '-', color='b')


def animate(i):
    ball1.set_data(solve_func(i, 'point'))
    ball_line1.set_data(solve_func(i, 'line'))


ani = FuncAnimation(fig, animate, frames=frames, interval=30)

plt.plot(accretion_disk_x, accretion_disk_y, '-', color='white')
plt.plot([0], [0], 'o', color='#FF4500', ms=30)

plt.axis('equal')

edge = 4*x0_earth

ax.set_xlim(-edge, edge)
ax.set_ylim(-edge, edge)

ani.save('black_hole.gif' )