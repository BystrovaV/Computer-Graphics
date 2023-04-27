import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider


def dda(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    steps = int(max(abs(dx), abs(dy)))
    x_inc = dx / steps
    y_inc = dy / steps

    points_x, points_y = [], []
    x, y = x0, y0
    for i in range(steps + 1):
        points_x.append(round(x))
        points_y.append(round(y))
        x += x_inc
        y += y_inc

    return points_x, points_y


def step_by_step_algorithm(x, k, b, steps):
    x_arr, y_arr = [], []

    for i in range(0, steps):
        x_arr.append(x)
        y_arr.append(round(k * x + b))
        x = x + 1

    return x_arr, y_arr


def bresenham_line_2(x0, y0, x1, y1):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    points_x, points_y = [], []
    while True:
        points_x.append(x0)
        points_y.append(y0)
        if x0 == x1 and y0 == y1:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

    return points_x, points_y


def bresenham_circle(x0, y0, r):
    x, y = 0, r
    d = 3 - 2 * r

    points_x, points_y = [], []
    while x <= y:
        points_x.append(x0 + x)
        points_x.append(x0 - x)
        points_x.append(x0 + x)
        points_x.append(x0 - x)
        points_x.append(x0 + y)
        points_x.append(x0 - y)
        points_x.append(x0 + y)
        points_x.append(x0 - y)

        points_y.append(y0 + y)
        points_y.append(y0 + y)
        points_y.append(y0 - y)
        points_y.append(y0 - y)
        points_y.append(y0 + x)
        points_y.append(y0 + x)
        points_y.append(y0 - x)
        points_y.append(y0 - x)
        if d < 0:
            d = d + 4 * x + 6
        else:
            d = d + 4 * (x - y) + 10
            y -= 1
        x += 1

    return points_x, points_y


def on_submit_click_0(event):
    global graph_axes
    graph_axes[0].clear()
    graph_axes[0].set_title('Bresenham circle')
    graph_axes[0].grid()
    x, y = bresenham_circle(slider_0_x.val, slider_0_y.val, slider_0_r.val)
    graph_axes[0].plot(x, y, 'ko', markersize=1)
    graph_axes[0].set_aspect('equal')


def on_submit_click_1(event):
    global graph_axes
    graph_axes[1].clear()
    graph_axes[1].set_title('DDA')
    graph_axes[1].grid()
    x, y = dda(slider_1_x0.val, slider_1_y0.val, slider_1_x1.val, slider_1_y1.val)
    graph_axes[1].plot(x, y, 'ko', markersize=1)
    graph_axes[1].set_aspect('equal')


def on_submit_click_2(event):
    global graph_axes
    graph_axes[2].clear()
    graph_axes[2].set_title('Bresenham line')
    graph_axes[2].grid()
    x, y = bresenham_line_2(int(slider_2_x0.val), int(slider_2_y0.val), int(slider_2_x1.val), int(slider_2_y1.val))
    graph_axes[2].plot(x, y, 'ko', markersize=1)
    graph_axes[2].set_aspect('equal')


def on_submit_click_3(event):
    global graph_axes
    graph_axes[3].clear()
    graph_axes[3].set_title('Step by step')
    graph_axes[3].grid()
    x, y = step_by_step_algorithm(slider_3_x0.val, slider_3_y0.val, slider_3_x1.val, slider_3_y1.val)
    graph_axes[3].plot(x, y, 'ko', markersize=1)
    graph_axes[3].set_aspect('equal')


fig, graph_axes = plt.subplots(1, 4)
fig.set_size_inches(10, 7)

fig.subplots_adjust(left=0.05, right=0.97, top=0.95, bottom=0.6, wspace=0.3)

# ------------------------------- BRESENHAM CIRCLE 0 ---------------------------------------
x, y = bresenham_circle(100, 100, 50)
graph_axes[0].set_title('Bresenham circle')
graph_axes[0].grid()
graph_axes[0].plot(x, y, 'ko', markersize=1)
graph_axes[0].set_aspect('equal')

axes_button_submit_0 = plt.axes(
    [0.05 + graph_axes[0].get_position().width / 4, 0.25, graph_axes[0].get_position().width / 2, 0.04])
button_submit_0 = Button(axes_button_submit_0, 'Submit')
button_submit_0.on_clicked(on_submit_click_0)

axes_slider_0_x = plt.axes([graph_axes[0].get_position().x0, 0.50,
                            graph_axes[0].get_position().width, 0.04])
slider_0_x = Slider(axes_slider_0_x,
                    label='x',
                    valmin=-300,
                    valmax=300,
                    valinit=100,
                    valfmt='%1.f')

axes_slider_0_y = plt.axes([graph_axes[0].get_position().x0, 0.45,
                            graph_axes[0].get_position().width, 0.04])
slider_0_y = Slider(axes_slider_0_y,
                    label='y',
                    valmin=-300,
                    valmax=300,
                    valinit=100,
                    valfmt='%1.f')

axes_slider_0_r = plt.axes([graph_axes[0].get_position().x0, 0.40,
                            graph_axes[0].get_position().width, 0.04])
slider_0_r = Slider(axes_slider_0_r,
                    label='y',
                    valmin=0,
                    valmax=100,
                    valinit=50,
                    valfmt='%1.f')

# ------------------------------- DDA 1 ---------------------------------------
x, y = dda(100, 0, 0, 100)
graph_axes[1].set_title('DDA')
graph_axes[1].grid()
graph_axes[1].plot(x, y, 'ko', markersize=1)
graph_axes[1].set_aspect('equal')

axes_button_submit_1 = plt.axes([graph_axes[1].get_position().x0 + graph_axes[1].get_position().width / 4, 0.25,
                                 graph_axes[1].get_position().width / 2, 0.04])
button_submit_1 = Button(axes_button_submit_1, 'Submit')
button_submit_1.on_clicked(on_submit_click_1)

# print(graph_axes[0].get_position())
axes_slider_1_x0 = plt.axes([graph_axes[1].get_position().x0, 0.5,
                             graph_axes[1].get_position().width, 0.04])
slider_1_x0 = Slider(axes_slider_1_x0,
                     label='x0',
                     valmin=-300,
                     valmax=300,
                     valinit=100,
                     valfmt='%1.f')

axes_slider_1_y0 = plt.axes([graph_axes[1].get_position().x0, 0.45,
                             graph_axes[1].get_position().width, 0.04])
slider_1_y0 = Slider(axes_slider_1_y0,
                     label='y0',
                     valmin=-300,
                     valmax=300,
                     valinit=0,
                     valfmt='%1.f')

axes_slider_1_x1 = plt.axes([graph_axes[1].get_position().x0, 0.40,
                             graph_axes[1].get_position().width, 0.04])
slider_1_x1 = Slider(axes_slider_1_x1,
                     label='x1',
                     valmin=-300,
                     valmax=300,
                     valinit=0,
                     valfmt='%1.f')

axes_slider_1_y1 = plt.axes([graph_axes[1].get_position().x0, 0.35,
                             graph_axes[1].get_position().width, 0.04])
slider_1_y1 = Slider(axes_slider_1_y1,
                     label='y1',
                     valmin=-300,
                     valmax=300,
                     valinit=100,
                     valfmt='%1.f')

# ------------------------------- BRESENHAM LINE 3 ---------------------------------------
x, y = bresenham_line_2(100, 0, 0, 100)
graph_axes[2].set_title('Bresenham line')
graph_axes[2].grid()
graph_axes[2].plot(x, y, 'ko', markersize=1)
graph_axes[2].set_aspect('equal')

axes_button_submit_2 = plt.axes([graph_axes[2].get_position().x0 + graph_axes[2].get_position().width / 4, 0.25,
                                 graph_axes[2].get_position().width / 2, 0.04])
button_submit_2 = Button(axes_button_submit_2, 'Submit')
button_submit_2.on_clicked(on_submit_click_2)

axes_slider_2_x0 = plt.axes([graph_axes[2].get_position().x0, 0.5,
                             graph_axes[2].get_position().width, 0.04])
slider_2_x0 = Slider(axes_slider_2_x0,
                     label='x0',
                     valmin=-300,
                     valmax=300,
                     valinit=100,
                     valfmt='%0.0f')

axes_slider_2_y0 = plt.axes([graph_axes[2].get_position().x0, 0.45,
                             graph_axes[2].get_position().width, 0.04])
slider_2_y0 = Slider(axes_slider_2_y0,
                     label='y0',
                     valmin=-300,
                     valmax=300,
                     valinit=0,
                     valfmt='%0.0f')

axes_slider_2_x1 = plt.axes([graph_axes[2].get_position().x0, 0.40,
                             graph_axes[2].get_position().width, 0.04])
slider_2_x1 = Slider(axes_slider_2_x1,
                     label='x1',
                     valmin=-300,
                     valmax=300,
                     valinit=0,
                     valfmt='%0.0f')

axes_slider_2_y1 = plt.axes([graph_axes[2].get_position().x0, 0.35,
                             graph_axes[2].get_position().width, 0.04])
slider_2_y1 = Slider(axes_slider_2_y1,
                     label='y1',
                     valmin=-300,
                     valmax=300,
                     valinit=100,
                     valfmt='%0.0f')

# ------------------------------- STEP BY STEP 4 ---------------------------------------
x, y = step_by_step_algorithm(0, -1, 100, 100)
graph_axes[3].set_title('Step by step')
graph_axes[3].grid()
graph_axes[3].plot(x, y, 'ko', markersize=1)
graph_axes[3].set_aspect('equal')

axes_button_submit_3 = plt.axes([graph_axes[3].get_position().x0 + graph_axes[3].get_position().width / 4, 0.25,
                                 graph_axes[3].get_position().width / 2, 0.04])
button_submit_3 = Button(axes_button_submit_3, 'Submit')
button_submit_3.on_clicked(on_submit_click_3)

axes_slider_3_x0 = plt.axes([graph_axes[3].get_position().x0, 0.5,
                             graph_axes[3].get_position().width, 0.04])
slider_3_x0 = Slider(axes_slider_3_x0,
                     label='x',
                     valmin=-300,
                     valmax=300,
                     valinit=100,
                     valfmt='%1.f')

axes_slider_3_y0 = plt.axes([graph_axes[3].get_position().x0, 0.45,
                             graph_axes[3].get_position().width, 0.04])
slider_3_y0 = Slider(axes_slider_3_y0,
                     label='k',
                     valmin=-50,
                     valmax=50,
                     valinit=0,
                     valfmt='%1.f')

axes_slider_3_x1 = plt.axes([graph_axes[3].get_position().x0, 0.40,
                             graph_axes[3].get_position().width, 0.04])
slider_3_x1 = Slider(axes_slider_3_x1,
                     label='b',
                     valmin=-50,
                     valmax=50,
                     valinit=0,
                     valfmt='%1.f')

axes_slider_3_y1 = plt.axes([graph_axes[3].get_position().x0, 0.35,
                             graph_axes[3].get_position().width, 0.04])
slider_3_y1 = Slider(axes_slider_3_y1,
                     label='steps',
                     valmin=0,
                     valmax=300,
                     valinit=100,
                     valfmt='%1.f')
plt.show()
