import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from start_data import *

frames = 365
seconds_in_year = 365 * 24 * 60 * 60
years = 3
t = np.linspace(0, years*seconds_in_year, frames)

def  move_func(s, t):
    ( x1, vx1, y1, vy1, 
      xm, vxm, ym, vym) = s
    
#земля
    dxdt1 = vx1
    dvxdt1 = -G * m * x1 / (x1**2 + y1**2) ** 1.5 * A * np.exp(B * np.sqrt(x1**2+y1**2)) 
    dydt1 = vy1
    dvydt1 = -G * m * y1 / (x1**2 + y1**2) ** 1.5 * A * np.exp(B * np.sqrt(x1**2+y1**2)) 
#марс
    dxdt2 = vxm
    dvxdt2 = -G * m * xm / (xm**2 + ym**2) ** 1.5
    dydt2 = vym
    dvydt2 = -G * m * ym / (xm**2 + ym**2) ** 1.5 
    return (dxdt1, dvxdt1, dydt1, dvydt1,
            dxdt2, dvxdt2, dydt2, dvydt2)

G = 6.67 * 10**(-11)
m = 1.98 * 10**(30)
A = 1.5
B = 149 * 10**(-14)

s0 = (x0e,  vx0e,  y0e,  vy0e,
      x0m,  vx0m,  y0m,  vy0m)

sol = odeint(move_func, s0, t)

def solve_func(i, key):
    if key == 'point':
        x1 = sol[i, 0]
        y1 = sol[i, 2]
        
        x2 = sol[i, 4]
        y2 = sol[i, 6]

    elif key == 'line':
        x1 = sol[:i, 0]
        y1 = sol[:i, 2]
        
        x2 = sol[:i, 4]
        y2 = sol[:i, 6]
        
    return ((x1, y1), (x2, y2))

fig, ax = plt.subplots()

ball1, = plt.plot([], [], 'o', color='b')
ball_line1, = plt.plot([], [], '-', color='b')

ball2, = plt.plot([], [], 'o', color='r')
ball_line2, = plt.plot([], [], '-', color='r')

plt.plot([0], [0], 'o', color='black', ms=20)

def animate(i):
    ball1.set_data(solve_func(i, 'point')[0])
    ball_line1.set_data(solve_func(i, 'line')[0])

    ball2.set_data(solve_func(i, 'point')[1])
    ball_line2.set_data(solve_func(i, 'line')[1])


ani = FuncAnimation(fig, animate, frames=frames, interval=30)

plt.axis('equal')

edge = 4*x0e
ax.set_xlim(-edge, edge)
ax.set_ylim(-edge, edge)
ani.save('black_hole(mod_1).gif')