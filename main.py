import numpy as np 
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from initial_data import * 


plt.style.use('dark_background')
# Определяем переменую величину
frames = 365
seconds_in_year = 365 * 24 * 60 * 60
years = 1
t = np.linspace(0, years*seconds_in_year, frames)


#_____

r = 10
theta = np.linspace(0, 2*np.pi, 100)
x13 = r * np.cos(theta)
y13= r * np.sin(theta)

#_____



def  move_func(s, t):
    ( x0_earth, v_x0_earth, y0_earth, v_y0_earth, 
      x0_venus, v_x0_venus, y0_venus, v_y0_venus,
      ) = s
#земля
    dxdt1 = v_x0_earth
    dvxdt1 = -G * m * x0_earth / (x0_earth**2 + y0_earth**2) ** 1.5
    dydt1 = v_y0_earth
    dvydt1 = -G * m * y0_earth / (x0_earth**2 + y0_earth**2) ** 1.5
#марс
    dxdt2 = v_x0_venus
    dvxdt2 = -G * m * x0_venus / (x0_venus**2 + y0_venus**2) ** 1.5
    dydt2 = v_y0_venus
    dvydt2 = -G * m * y0_venus / (x0_venus**2 + y0_venus**2) ** 1.5
    return (dxdt1, dvxdt1, dydt1, dvydt1,
            dxdt2, dvxdt2, dydt2, dvydt2)

G = 6.67 * 10**(-11)
m = 1.98 * 10**(30)


s0 = (x0_earth,  v_x0_earth,  y0_earth,  v_y0_earth,
      x0_venus, v_x0_venus, y0_venus, v_y0_venus)

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

plt.plot([0], [0], 'o', color='#FF4500', ms=30)
plt.plot(x13, y13, 'o', color='orange')

def animate(i):
    ball1.set_data(solve_func(i, 'point')[0])
    ball_line1.set_data(solve_func(i, 'line')[0])

    ball2.set_data(solve_func(i, 'point')[1])
    ball_line2.set_data(solve_func(i, 'line')[1])


ani = FuncAnimation(fig, animate, frames=frames, interval=30)

plt.axis('equal')

edge = 4*x0_earth

ax.set_xlim(-edge, edge)
ax.set_ylim(-edge, edge)
ani.save('black_hole.gif')