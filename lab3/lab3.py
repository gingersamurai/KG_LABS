import numpy as np
from matplotlib import pyplot as plt
from matplotlib.text import Text
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.widgets import Button

fig = plt.figure()
fig.subplots_adjust(bottom=0.3)
ax = fig.add_subplot(111, projection='3d')

N = int(input("Введите точность аппроксимации: "))

x = np.linspace(-1.5, 2.0, N+1)
y = 0.007*x**2
v = np.array([(x[i], y[i], 0) for i in range(N)])
v2 = np.array([(x[i], y[i], 1) for i in range(N)])

ax.scatter3D(v[:, 0], v[:, 1], v[:, 2])
ax.set_zlim(0, 1)

# generate list of sides polygons of pyramid
sides = []
for i in range(1, N):
    sides.append([v[i - 1], v[i], v2[i], v2[i-1]])
sides.append([v[-1], v[0], v2[0], v2[-1]])

# add base of pyramid
sides.append(v)
sides.append(v2)
# add sides on plot
ax.add_collection3d(Poly3DCollection(sides, facecolors='red', linewidth=0.1, edgecolors='black', alpha=0.5))

def remove_func(event):
    ax.add_collection3d(Poly3DCollection(sides, facecolors='red', linewidths=0.1, edgecolors='black', alpha=1))
    plt.draw()

remove_button_ax = fig.add_axes([0.4, 0.15, 0.25, 0.05])
remove_button = Button(remove_button_ax, "Remove invisible lines",  color='r')
remove_button.on_clicked(remove_func)


def show_func(event):
    ax.add_collection3d(Poly3DCollection(sides, facecolors='red', alpha=0.5, edgecolors='black', linewidths=0.1))
    plt.draw()


show_button_ax = fig.add_axes([0.4, 0.25, 0.25, 0.05])
show_button = Button(show_button_ax, "Show invisible lines", color='g')
show_button.on_clicked(show_func)


def isometric_func(event):
    ax.view_init(30)
    plt.draw()


isometric_button_ax = fig.add_axes([0.1, 0.28, 0.23, 0.05])
isometric_button = Button(isometric_button_ax, "Isometric", color='y')
isometric_button.on_clicked(isometric_func)


def top_func(event):
    ax.view_init(elev=90)
    plt.draw()


top_button_ax = fig.add_axes([0.1, 0.16, 0.23, 0.05])
top_button = Button(top_button_ax, "Top", color='y')
top_button.on_clicked(top_func)


def front_func(event):
    ax.view_init(elev=0)
    plt.draw()


front_button_ax = fig.add_axes([0.1, 0.22, 0.23, 0.05])
front_button = Button(front_button_ax, "Front", color='y')
front_button.on_clicked(front_func)

def bottom_func(event):
    ax.view_init(elev=-90)
    plt.draw()


bottom_button_ax = fig.add_axes([0.1, 0.1, 0.23, 0.05])
bottom_button = Button(bottom_button_ax, "Bottom", color='y')
bottom_button.on_clicked(bottom_func)

fig.text(0.1, 0.34, "Projections:")

ax.grid(False)
ax.axis(False)
plt.show()