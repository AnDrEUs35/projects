import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from start_data import *

file = open('cs.txt', mode='w')

plt.style.use('dark_background')
frames = 100
seconds_in_year = 365 * 24 * 60 * 60
years = 1
t = np.linspace(0, years*seconds_in_year, frames)

def  move_func(s, t):
    ( x1, vx1, y1, vy1, 
      xm, vxm, ym, vym) = s
    
    dxdt1 = vx1
    dvxdt1 = -G * m * x1 / (x1**2 + y1**2) ** 1.5 * A * np.exp(B * np.abs(x1+y1))
    dydt1 = vy1
    dvydt1 = -G * m * y1 / (x1**2 + y1**2) ** 1.5 * A * np.exp(B * np.abs(x1+y1))

    dxdt2 = vxm
    dvxdt2 = -G * m * xm / (xm**2 + ym**2) ** 1.5
    dydt2 = vym
    dvydt2 = -G * m * ym / (xm**2 + ym**2) ** 1.5
    return (dxdt1, dvxdt1, dydt1, dvydt1,
            dxdt2, dvxdt2, dydt2, dvydt2)

G = 6.67 * 10**(-11)
m = 10 * 1.98 * 10**(30)
A = 0.5
B = 149 * 10**(-14)

s0 = (x0e,  vx0e,  y0e,  vy0e,
      x0m,  vx0m,  y0m,  vy0m)

sol = odeint(move_func, s0, t)
coords1 = []
coords2 = []
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

    return (str(x1), str(y1)), (str(x2), str(y2))

def animate(i):
    coords1.append(solve_func(i, 'point')[0])
    coords2.append(solve_func(i, 'line')[0])

plt.axis('equal')

file.writelines(str(coords1))
file.write('\n')
file.writelines(str(coords2))
file.close()