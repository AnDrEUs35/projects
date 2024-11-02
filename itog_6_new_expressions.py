import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# некая частица 1
x0e = 2 * 149 * 10**9
vx0e = 0 #0
y0e = 0
vy0e = 7910 #40000

# некая частица 2
x0m = 0
vx0m = 7910
y0m = 6 * 149 * 10**9
vy0m = 0

plt.style.use('dark_background')
frames = 365
seconds_in_year = 365 * 24 * 60 * 60
years = 5
t = np.linspace(0, years*seconds_in_year, frames)

def  move_func(s, t):
    ( x1, vx1, y1, vy1, 
      xm, vxm, ym, vym) = s
    l = (x1 * vy1 - y1 * vx1) / np.sqrt(x1**2 + y1**2)
    
    dxdt1 = vx1
    dvxdt1 = -rg * c**2 * x1 / 2 * (x1**2 + y1**2)**1.5 + (x1 * vy1 - y1 * vx1)**2 * x1 / (x1**2 + y1**2)**7/2 - 3 * (x1 * vy1 - y1 * vx1)**2 * rg * x1 / (x1**2 + y1**2)**9/2
    dydt1 = vy1
    dvydt1 = -rg * c**2 * y1 / 2 * (x1**2 + y1**2)**1.5 + (x1 * vy1 - y1 * vx1)**2 * y1 / (x1**2 + y1**2)**7/2 - 3 * (x1 * vy1 - y1 * vx1)**2 * rg * y1 / (x1**2 + y1**2)**9/2

    dxdt2 = vxm
    dvxdt2 = -G * m * xm / (xm**2 + ym**2) ** 1.5
    dydt2 = vym
    dvydt2 = -G * m * ym / (xm**2 + ym**2) ** 1.5 
    return (dxdt1, dvxdt1, dydt1, dvydt1,
            dxdt2, dvxdt2, dydt2, dvydt2)

G = 6.67 * 10**(-11)
m = 10 * 1.98 * 10**(30)
c = 300000000
rg = 2 * G * m / c**2


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

plt.plot([0], [0], 'o', color='orange', ms=20)
plt.plot([0], [0], 'o', color='black', ms=15)

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
ani.save('black_hole(mod_6_NE).gif')