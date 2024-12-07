import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


G = 6.67 * 10 ** (-11)
M = 900 * 1.98 * 10 ** (30)
c = 3e8
R = 149 * 10**9
Rs = 696340000
eccentricity = 0.8

# некая частица 1
x0e = 0.37499 * R
vx0e = 0
y0e = 0
vy0e =  np.sqrt(G * M / x0e * (1 + eccentricity))

# некая частица 2
x0m = 0
vx0m = 20000
y0m = 2 * 149 * 10 ** 9
vy0m = 0

aph = 0.466697 * R
Va = np.sqrt(G * M / x0e * (1 - eccentricity))
l = (x0e * vy0e + aph * Va) / 2
plt.style.use('dark_background')
frames = 500
T = 365 * 24 * 60 * 60  # seconds_in_year
years = 0.08
t = np.linspace(0, years * T, frames)


def move_func(s, t):
    (x1, vx1, y1, vy1,
     xm, vxm, ym, vym) = s

    p = (x1**2 + y1**2)**0.5 / Rs
    # l = (x1 * vy1 + y1 * vx1) / 2

    dxdt1 = vx1
    dvxdt1 = -G * M * T / R**3 * x1 / p**3 * (1 + 3 * l**2 / (R**2 * c**2 * p**2))
    dydt1 = vy1
    dvydt1 = -G * M * T / R**3 * y1 / p**3 * (1 + 3 * l**2 / (R**2 * c**2 * p**2))

    dxdt2 = vxm
    dvxdt2 = -G * M * xm / (xm ** 2 + ym ** 2) ** 1.5
    dydt2 = vym
    dvydt2 = -G * M * ym / (xm ** 2 + ym ** 2) ** 1.5
    return (dxdt1, dvxdt1, dydt1, dvydt1,
            dxdt2, dvxdt2, dydt2, dvydt2)


s0 = (x0e, vx0e, y0e, vy0e,
      x0m, vx0m, y0m, vy0m)

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

    # ball2.set_data(solve_func(i, 'point')[1])
    # ball_line2.set_data(solve_func(i, 'line')[1])


ani = FuncAnimation(fig, animate, frames=frames, interval=30)

plt.axis('equal')

edge = 3 * x0e
ax.set_xlim(-edge, edge)
ax.set_ylim(-edge, edge)
ani.save('black_hole(yes!!!).gif')