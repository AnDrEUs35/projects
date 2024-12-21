import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Задаём
x0 = 46001009
y0 = 0
try:
    if x0 == 0:
        raise ZeroDivisionError
    else:
        phi = np.arctan(y0 / x0)
except ZeroDivisionError:
    phi = 0

v_merc = 47.36
ecc = 0.205


def f(r, t, params):
    r1, r2, r3 = r
    l = params
    return [r2, -1/(2*r1**2)+l**2/r1**3-1*1.5*l**2/r1**4, l/r1**2]

# МОЖНО ИССЛЕДОВАТЬ параметры: r0, params
# r_g = 2 * G * M / c**2
r_g_sun = 2.95 # km
c = 2.99e5
r_merc = np.sqrt(x0**2 + y0**2) / r_g_sun
r0 =[r_merc, 0, phi] # В единицах гравитационного радиуса
N = 300

v_per = v_merc * np.sqrt((1 + ecc) / (1 - ecc)) / c

L1 = v_per * r_merc # момент импульса для круговой орбиты
params = 1.0 * L1 # если взять больше, то орбита еще вытянется
time = 2 * np.pi * r0[0]**2 / L1 # период обращения по круговой орбите

t = np.linspace(0, 15*time, N)

sol = odeint(f, r0, t, args=(params,))

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
