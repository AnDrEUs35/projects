import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from start_data import *

frames = 1460
seconds_in_year = 365 * 24 * 60 * 60
years = 15
t = np.linspace(0, years*seconds_in_year, frames)

def  move_func(s, t):
    ( x1, vx1, y1, vy1, z1, vz1) = s
    
    dxdt1 = vx1
    dvxdt1 = -G * m * x1 / (x1**2 + y1**2 + z1**2) ** 1.5 * A * np.exp(B * np.sqrt(x1**2 + y1**2 + z1**2)) 
    dydt1 = vy1
    dvydt1 = -G * m * y1 / (x1**2 + y1**2 + z1**2) ** 1.5 * A * np.exp(B * np.sqrt(x1**2 + y1**2 + z1**2)) 
    dzdt1 = vz1
    dvzdt1 = -G * m * z1 / (x1**2 + y1**2 + z1**2) ** 1.5 * A * np.exp(B * np.sqrt(x1**2 + y1**2 + z1**2))

    return (dxdt1, dvxdt1, dydt1, dvydt1, dzdt1, dvzdt1)

G = 6.67 * 10**(-11)
m = 2*1.98 * 10**(30)
A = 0.5
B = 149 * 10**(-14)

s0 = (x0e,  vx0e,  y0e,  vy0e, z0e, vz0e)

sol = odeint(move_func, s0, t)

def solve_func(i, key):
    if key == 'point':
        x1 = sol[i, 0]
        y1 = sol[i, 2]
        z1 = sol[i, 4]

    elif key == 'line':
        x1 = sol[:i, 0]
        y1 = sol[:i, 2]
        z1 = sol[:i, 4]        
    return (x1, y1), (z1,)

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

ball1, = plt.plot([], [], [], 'o', color='b')
ball_line1, = plt.plot([], [], [], '-', color='b')

plt.plot([0], [0], [0], 'o', color='black', ms=20)

def animate(i):
    ball1.set_data(solve_func(i, 'point')[0])
    ball1.set_3d_properties(solve_func(i, 'point')[1])
    ball_line1.set_data(solve_func(i, 'line')[0])
    ball_line1.set_3d_properties(solve_func(i, 'line')[1])

ani = FuncAnimation(fig, animate, frames=frames, interval=30)

plt.axis('equal')

edge = 3*x0e
ax.set_xlim3d(-edge, edge)
ax.set_ylim3d(-edge, edge)
ax.set_zlim3d(-edge, edge)
ani.save('black_hole(mod_4).gif')