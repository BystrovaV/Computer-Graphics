import numpy as np
import cv2 as cv
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog as fd
from matplotlib import pyplot as plt


global image


def select_file():
    filetypes = (('jpg file', '*.jpg'),('bmp file', '*.bmp'),('jpeg file', '*.jpeg'),('png file', '*.png')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    change_image(filename)


def convert_to_tk_image(img):
    blue, green, red = cv.split(img)
    img = cv.merge((red, green, blue))
    im = Image.fromarray(img)
    im.thumbnail((400, 300), Image.ANTIALIAS)
    imgtk = ImageTk.PhotoImage(image=im)
    return imgtk


def equalization_rgb():
    blue, green, red = cv.split(image)

    blue = cv.equalizeHist(blue)
    green = cv.equalizeHist(green)
    red = cv.equalizeHist(red)

    lc_image = convert_to_tk_image(cv.merge((blue, green, red)))
    image_new.configure(image=lc_image)
    image_new.image = lc_image


def equalization_hsv():
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)

    v = cv.equalizeHist(v)
    brg = cv.cvtColor(cv.merge((h, s, v)), cv.COLOR_HSV2BGR)

    _image = convert_to_tk_image(brg)
    image_new.configure(image=_image)
    image_new.image = _image


def linear_contrast(image):
    blue, green, red = cv.split(image)
    alpha1 = 255 / (blue.max() - blue.min())
    alpha2 = 255 / (green.max() - green.min())
    alpha3 = 255 / (red.max() - red.min())

    blue = alpha1 * (blue - blue.min())
    green = alpha2 * (green - green.min())
    red = alpha3 * (red - red.min())
    new_image = cv.merge((blue.astype(np.uint8), green.astype(np.uint8), red.astype(np.uint8)))

    return new_image


def change_lc():
    lc_image = linear_contrast(image)
    lc_image = convert_to_tk_image(lc_image)
    image_new.configure(image=lc_image)
    image_new.image = lc_image
    print("change")


def conture():
    scale = 1
    delta = 0
    ddepth = cv.CV_16S

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    grad_x = cv.Sobel(gray, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)
    grad_y = cv.Sobel(gray, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)

    abs_grad_x = cv.convertScaleAbs(grad_x)
    abs_grad_y = cv.convertScaleAbs(grad_y)

    grad = cv.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

    im = Image.fromarray(grad)
    im.thumbnail((400, 300), Image.ANTIALIAS)
    imgtk = ImageTk.PhotoImage(image=im)
    image_new.configure(image=imgtk)
    image_new.image = imgtk


def spots():
    mask = np.full(shape=(3, 3), fill_value=-1)
    mask[1][1] = 8
    img_filter = cv.filter2D(image, -1, mask)
    ret, thresh1 = cv.threshold(img_filter, 127, 255, cv.THRESH_BINARY)

    im = Image.fromarray(thresh1)
    im.thumbnail((400, 300), Image.ANTIALIAS)
    imgtk = ImageTk.PhotoImage(image=im)
    image_new.configure(image=imgtk)
    image_new.image = imgtk


def change_image(image_name):
    global image
    global image_gray
    image_gray = cv.imdecode(np.fromfile(image_name, dtype=np.uint8), 0)
    image = cv.imdecode(np.fromfile(image_name, dtype=np.uint8), cv.IMREAD_COLOR)
    imgtk = convert_to_tk_image(image)
    image_original.configure(image=imgtk)
    image_original.image = imgtk
    image_new.configure(image=imgtk)
    image_new.image = imgtk


def line_segmentation():
    lsd = cv.createLineSegmentDetector(0)
    lines = lsd.detect(image_gray)[0]
    drawn_img = lsd.drawSegments(image_gray,lines)

    im = Image.fromarray(drawn_img)
    im.thumbnail((400, 300), Image.ANTIALIAS)
    imgtk = ImageTk.PhotoImage(image=im)
    image_new.configure(image=imgtk)
    image_new.image = imgtk


window = tk.Tk()
window.resizable(False, False)
window.geometry("900x600")

f_top_1 = tk.Frame(window)
f_top_1.pack(padx=5, pady=5)

f_top_2 = tk.Frame(window)
f_top_2.pack(padx=5, pady=5)

f_top_3 = tk.Frame(window)
f_top_3.pack(padx=5, pady=5)

button_lc= tk.Button(f_top_1, width=20, text= "Linear Contrast", command=change_lc)
button_lc.pack(side=tk.LEFT, padx=5)

button_seg_conture= tk.Button(f_top_1, width=20, text= "Conture", command=conture)
button_seg_conture.pack(side=tk.LEFT, padx=5)

button_eq= tk.Button(f_top_2, width=20, text= "Equalization RGB", command=equalization_rgb)
button_eq.pack(side=tk.LEFT, padx=5)

button_eq_hsv= tk.Button(f_top_3, width=20, text= "Equalization HSV", command=equalization_hsv)
button_eq_hsv.pack(side=tk.LEFT, padx=5)

button_seg_spots= tk.Button(f_top_2, width=20, text= "Spots", command=spots)
button_seg_spots.pack(side=tk.LEFT, padx=5)

button_seg_lines= tk.Button(f_top_3, width=20, text= "Lines", command=line_segmentation)
button_seg_lines.pack(side=tk.LEFT, padx=5)

open_button = tk.Button(window, width=20, text='Open Image', command=select_file)
open_button.pack()

image = cv.imread('Fig10.29(a).bmp')
image_gray = cv.imread('Fig10.29(a).bmp', 0)
imgtk = convert_to_tk_image(image)
image_original = tk.Label(window, image= imgtk, height=300, width=400)
image_original.pack(side="left")
image_new = tk.Label(window, image= imgtk, height=300, width=400)
image_new.pack(side="right")

window.bind("<Return>", change_lc)
window.bind("<Return>", equalization_rgb)
window.bind("<Return>", equalization_hsv)
window.bind("<Return>", conture)
window.bind("<Return>", spots)
window.bind("<Return>", line_segmentation)
window.bind("<Return>", select_file)
window.mainloop()
