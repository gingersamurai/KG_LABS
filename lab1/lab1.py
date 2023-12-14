import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
"""
y^2 = x^2/((a-x)(a+x)) a, A, B are constant, entered in window
"""

a = 1
A = -0.5
B = 0.5
x = np.linspace(A, B, max(0, int((B-A) * 100)))
y = x*np.sqrt(1/((a-x)*(a+x)))
color = 'blue'
style = '-'
def update_function():
    """
    Update function
    """
    x = np.linspace(A, B, max(0,  int((B-A) * 100)))
    y = x * np.sqrt(1/((a-x)*(a+x)))
    l.set_xdata(x)
    l.set_ydata(y)
    ax.set_xlim(
        np.min(x) - (np.max(x) - np.min(x)) / 100,
        np.max(x) + (np.max(x) - np.min(x)) / 100
    )
    ax.set_ylim(
        np.min(y) - (np.max(y) - np.min(y)) / 100,
        np.max(y) + (np.max(y) - np.min(y)) / 100
    )
    plt.setp(l, color = color, linestyle = style)

fig = plt.figure()
fig.subplots_adjust(bottom=0.2)
# To remove all of the default key bindings
fig.canvas.mpl_disconnect(fig.canvas.manager.key_press_handler_id)

ax = fig.add_subplot(111)
ax.set_title(r"$y^2 = x^2/((a-x)(a+x))$")
l, = ax.plot(x, y)
ax.grid()

ax.set_xlim(
    np.min(x) - (np.max(x)-np.min(x))/100,
    np.max(x) + (np.max(x)-np.min(x))/100
    )
ax.set_ylim(
    np.min(y) - (np.max(y)-np.min(y))/100,
    np.max(y) + (np.max(y)-np.min(y))/100
    )


def submit_a(a_):
    """
    Set parameter a
    """
    global a
    a = float(a_)
    update_function()
    plt.draw()


axbox_a = fig.add_axes([0.1, 0.05, 0.1, 0.06])
text_box_a = TextBox(axbox_a, "a ")
text_box_a.on_submit(submit_a)
text_box_a.set_val(a)


def submit_A(A_):
    """
    Set parameter A
    """
    global A
    A = float(A_)
    update_function()
    plt.draw()


axbox_A = fig.add_axes([0.25, 0.05, 0.1, 0.06])
text_box_A = TextBox(axbox_A, "A ")
text_box_A.on_submit(submit_A)
text_box_A.set_val(A)

def submit_B(B_):
    """
    Set parameter B
    """
    global B
    B = float(B_)
    update_function()
    plt.draw()


axbox_B = fig.add_axes([0.4, 0.05, 0.1, 0.06])
text_box_B = TextBox(axbox_B, "B ")
text_box_B.on_submit(submit_B)
text_box_B.set_val(B)

def submit_color(color_):
    """
    Set color
    """
    global color
    color = str(color_)
    update_function()
    plt.draw()


axbox_C = fig.add_axes([0.6, 0.05, 0.1, 0.06])
text_box_C = TextBox(axbox_C, "Color: ")
text_box_C.on_submit(submit_color)
text_box_C.set_val(color)

def submit_style(style_):
    """
    Set style
    """
    global style
    style = str(style_)
    update_function()
    plt.draw()


axbox_S = fig.add_axes([0.8, 0.05, 0.1, 0.06])
text_box_S = TextBox(axbox_S, "Style: ")
text_box_S.on_submit(submit_style)
text_box_S.set_val(style)

plt.show()