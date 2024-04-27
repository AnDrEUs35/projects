import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors



neighbourhood = ((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1))
EMPTY, TREE, FIRE, WATER  = 0, 1, 2, 3

colors_list = ['black', (0,0.5,0), 'blue', 'orange']
cmap = colors.ListedColormap(colors_list)
bounds = [0,1,2,3,4]
norm = colors.BoundaryNorm(bounds, cmap.N)

def iterate(X):
    X1 = np.zeros((y, x))
    for ix in range(1,x-1):
        for iy in range(1,y-1):
            if X[iy,ix] == EMPTY and np.random.random() <= 0.02:
                X1[iy,ix] = TREE
            if X[iy,ix] == FIRE and np.random.random() <= 0.8:
                X1[iy,ix] = WATER
            if X[iy,ix] == TREE:
                X1[iy,ix] = TREE
                for dx,dy in neighbourhood:
                    if abs(dx) == abs(dy) and np.random.random() < 0.573:
                        continue
                        
                    if X[iy+dy,ix+dx] == FIRE and np.random.random() < 0.573 :
                        X1[iy,ix] = FIRE
                        break
                else:
                    if np.random.random() <= f:
                        X1[iy,ix] = FIRE
    return X1

forest_fraction = 0.2

p,f  = 0.02, 0.0001

x,y = 100, 100

X  = np.zeros((y, x))
X[1:y-1, 1:x-1] = np.random.randint(0, 2, size=(y-2, x-2))
X[1:y-1, 1:x-1] = np.random.random(size=(y-2, x-2)) < forest_fraction

fig = plt.figure(figsize=(25/3, 6.25))
ax = fig.add_subplot(111)
ax.set_axis_off()
im = ax.imshow(X, cmap=cmap, norm=norm)

def animate(i):
    im.set_data(animate.X)
    animate.X = iterate(animate.X)

animate.X = X


interval = 100
anim = animation.FuncAnimation(fig, animate, interval=interval, frames=200)
anim.save('gif.gif')















