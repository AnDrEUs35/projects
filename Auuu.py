import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation        

G = 6.67 * 1e-11
c = 2.99e5  # km / s

def move_func(r, t, L1):
    r1, r2, r3, = r  # расстояние, радиальная компонента скорости, угол
    l = L1
    return [r2, -1 / (2 * r1 ** 2) + l ** 2 / r1 ** 3 - 1 * 1.5 * l ** 2 / r1 ** 4, l / r1 ** 2]

# Задаём
x0 = 46001009 # km
y0 = 0
Vx = 0
Vy = 4756 # km / s

M = 1.98e35
ecc = 0.205

N = 15  # А это разве не количество периодов обращения?
frames = 500
scale = 1.2

phi = np.arctan2(y0, x0)
alpha = np.arctan2(Vy, Vx)

r_g_sun = (2 * G * M / (c * 1000) ** 2) / 1000  # km
r_merc = np.sqrt(x0 ** 2 + y0 ** 2) / r_g_sun

M = r_g_sun * 1000 * (c * 1000) ** 2 / (2 * G)  # kg
v_merc = np.sqrt(G * M / (r_merc * r_g_sun * 1000)) / 1000  # km/s

v_per_merc = v_merc * np.sqrt((1 + ecc) / (1 - ecc)) / c
v_thau = v_per_merc * np.sin(phi - alpha)  # тангенциальная скорость
v_r = v_merc * np.cos(phi - alpha)  # радиальная скорость

L1 = 1 * v_thau * r_merc  # момент импульса для круговой орбиты

r0 = [r_merc, v_r, phi]  # Расстояние, радиальная компонента скорость, угол
time = 2 * np.pi * r0[0] ** 2 / np.abs(L1)  # период обращения по круговой орбите
print(time)

t = np.linspace(0, N * time, frames)
sol = odeint(move_func, r0, t, args=(L1,))

# --------------------------------------------------------------------------------------
radius = sol[:, 0]
angle = sol[:, 2]

X = radius * np.cos(angle)
Y = radius * np.sin(angle)

fig, ax = plt.subplots()

plt.style.use('dark_background')
ax.set_xlim(-scale * x0, scale * x0)
ax.set_ylim(-scale * x0, scale * x0)
plt.plot([0], [0], 'o', color='orange', ms=20)
plt.plot([0], [0], 'o', color='black', ms=15)

plt.plot(X, Y, 'r', alpha=0.05)

ball1, = plt.plot([], [], 'o', color='g')
ball_line1, = plt.plot([], [], '-', color='g')

def func_anim(i):
    ball1.set_data(X[i], Y[i])
    ball_line1.set_data(X[:i], Y[:i])

ani = FuncAnimation(fig, func_anim, frames=np.arange(0, frames, 1), interval=100)

plt.axis('equal')

ani.save('name.gif', writer="pillow")