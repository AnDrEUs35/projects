# Import libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import time

# Set common figure parameters
fig_size = 10
newparams = {'axes.grid': True,
             'lines.linewidth': 1.5, 'lines.markersize': 10,
             'font.size': 14}
plt.rcParams.update(newparams)

def Veff(rho, l):
    return -1/(2*rho) + l**2/(2*rho**2) - l**2/(2*rho**3)

def Vclassical(rho, l):
    return -1/(2*rho) + l**2/(2*rho**2)

def K(Z):
    rho2 = Z[0, :]**2 + Z[1, :]**2
    return .5 * (Z[3, :]*Z[1, :] + Z[2, :]*Z[0, :])**2/rho2
N = 1000
rho = np.linspace(1, 30, N)
l = 2


def getB(x, y, u, v):
    l2 = (x*v - y*u)**2
    # Note that l2 has the "dimension" R_s 
    return 3*l2

def getA():
    return .5

def RHS(Z, A, B):
    
    rho = np.sqrt(Z[0]**2 + Z[1]**2)
    correction = 1 + B/rho**2
    dUdtau = -A*Z[0]/rho**3*correction
    dVdtau = -A*Z[1]/rho**3*correction
    
    return np.array([Z[2], Z[3], dUdtau, dVdtau])

def rk4step(f, y, h, A, B):
    
    s1 = f(y, A, B)
    s2 = f(y + h*s1/2.0, A, B)
    s3 = f(y + h*s2/2.0, A, B)
    s4 = f(y + h*s3, A, B)
    
    return y + h/6.0*(s1 + 2.0*s2 + 2.0*s3 + s4)

def getOrbit(n, T_max, Z0):
    B = getB(*Z0)
    print("GR correction constant: %.2e"%(B))
    A = getA()
    
    h = T_max/float(n)
    Z = np.zeros((4, n + 1))
    Z[:, 0] = Z0

    tic = time.time()
    for i in range(0, n):
        Z[:, i + 1] = rk4step(RHS, Z[:, i], h, A, B)
    print("%.5f s, run time with %i steps."% (time.time() - tic, n))
    
    return Z


def plotOrbit(Z, lim_fact):
    plt.figure(figsize=(2*fig_size, fig_size))

    rho = (Z[0, :]**2 + Z[1, :]**2)**.5
    l = Z[0, :]*Z[3, :] - Z[1, :]*Z[2, :]
    
    # Trajectory
    ax = plt.subplot(2, 2, (1, 3))
    plt.title("Orbit")
    ax.plot(Z[0, :], Z[1, :], label="Orbit")
    ax.plot(Z[0, 0], Z[1, 0], "o", label="Start")
    plt.xlabel(r"$x$")
    plt.ylabel(r"$y$")
    ax.plot(0, 0, ".", label="Origin")
    circle = plt.Circle((0, 0), radius=1, color="gray")
    ax.add_artist(circle)
    ax_lim = max(Z[0, 0], Z[1, 0])
    plt.xlim([-lim_fact*ax_lim, lim_fact*ax_lim])
    plt.ylim([-lim_fact*ax_lim, lim_fact*ax_lim])
    plt.legend()
    
    plt.savefig('aaaaa.png')


#Z0 = [0, 20, .1, 0]
#Z0 = [0, 10, 0.2, -0.2]
#Z0 = [0, 10, .25, 0]
#Z0 = [0, 10, 0.2, -.1]
Z0 = [0, 10, .2, 0]
n = 5000
tau_max = 5000
Z = getOrbit(n, tau_max, Z0)
plotOrbit(Z, 1.1)