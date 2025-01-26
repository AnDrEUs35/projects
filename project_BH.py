import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib.animation as animation

G = 6.67 * 1e-11

def f(r, t, L1):
    r1, r2, r3,= r # расстояние, радиальная компонента скорости, угол 
    l = L1
    return [r2, -1/(2*r1**2) + l**2/r1**3 - 1*1.5*l**2/r1**4, l/r1**2]

# Задаём
x0 = 46001009 # km
y0 = 0
Vx = 0
Vy = 4756 # km / s

M = 1.98e35
ecc = 0.205


phi = np.arctan2(y0, x0)
alpha = np.arctan2(Vy, Vx)


c = 2.99e5 # km / s
r_g_sun = (2 * G * M / (c*1000)**2) / 1000 # km
r_merc = np.sqrt(x0**2 + y0**2) / r_g_sun


M = r_g_sun * 1000 * (c * 1000)**2 / (2 * G) # kg
v_merc = np.sqrt(G * M / (r_merc * r_g_sun * 1000)) / 1000 # km/s
N = 500


v_per_merc = v_merc * np.sqrt((1 + ecc) / (1 - ecc)) / c 
v_thau = v_per_merc * np.sin(phi - alpha) # тангенциальная скорость
v_r = v_merc * np.cos(phi - alpha) # радиальная скорость


L1 = 1 * v_thau * r_merc # момент импульса для круговой орбиты

r0 =[r_merc, v_r, phi] # Расстояние, радиальная компонента скорость, угол
time = 2 * np.pi * r0[0]**2 / L1 # период обращения по круговой орбите
print(time)

t = np.linspace(0, 15*time, N)
sol = odeint(f, r0, t, args=(L1,))


#--------------------------------------------------------------------------------------
radius = sol[:,0]
angle = sol[:,2]

X = radius * np.cos(angle)
Y = radius * np.sin(angle)

fig = plt.figure()

plt.style.use('dark_background')
plt.xlim(-1.2*x0, 1.2*x0)
plt.ylim(-1.2*x0, 1.2*x0)
plt.plot([0], [0], 'o', color='orange', ms=20)
plt.plot([0], [0], 'o', color='black', ms=15)

plt.plot(X, Y,'r',alpha=0.05)

ball1, = plt.plot([], [], 'o', color='g')
ball_line1, = plt.plot([], [], '-', color='g')

def func_anim(i):
    ball1.set_data(X[i], Y[i])
    ball_line1.set_data(X[:i], Y[:i])

ani = animation.FuncAnimation(fig, func_anim, frames=np.arange(0,N,1),interval=100)

plt.axis('equal')

ani.save('name.gif', writer="pillow")
