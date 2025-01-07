import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def f(r, t, L1):
    r1, r2, r3,= r
    l = L1
    return [r2, -1/(2*r1**2)+l**2/r1**3-1*1.5*l**2/r1**4, l/r1**2]

# Задаём
x0 = 46001009 # km
y0 = 0
Vx = 0
Vy = 47.36 # km / s
ecc = 0.205

phi = np.arctan2(y0, x0)
alpha = np.arctan2(Vy, Vx)

# r_g = 2 * G * M / c**2
r_g_sun = 2.95 # km
c = 2.99e5
r_merc = np.sqrt(x0**2 + y0**2) / r_g_sun
N = 300

v_merc = np.sqrt(Vx**2 + Vy**2) / c
v_thau = v_merc * np.sin(phi - alpha) # тангенциальная скорость
v_r = v_merc * np.cos(phi - alpha) # радиальная скорость


v_per = v_merc * np.sqrt((1 + ecc) / (1 - ecc)) / c # тоже тангенциальная скорость

L1 = 1.3 * v_thau * r_merc # момент импульса для круговой орбиты

r0 =[r_merc, v_r, phi] # Расстояние, радиальная компонента скорость, угол
time = 2 * np.pi * r0[0]**2 / L1 # период обращения по круговой орбите

t = np.linspace(0, 15*time, N)

sol = odeint(f, r0, t, args=(L1,))


#--------------------------------------------------------------------------------------
radius = sol[:,0]
angle = sol[:,2]

X = radius * np.cos(angle)
Y = radius * np.sin(angle)

fig = plt.figure()
plt.xlim(-30, 30)
plt.ylim(-30, 30)
plt.plot([0], [0], 'o', ms=10, color='k')

plt.plot(X, Y,'r',alpha=0.05)

def func_anim(i):
    plt.plot(X[:i], Y[:i],'g')

ani = animation.FuncAnimation(fig, func_anim, frames=np.arange(0,N,1),interval=100)

plt.axis('equal')

ani.save('name.gif', writer="pillow")
