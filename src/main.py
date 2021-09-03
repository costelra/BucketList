from tkinter import *
import tkmacosx as tkmac
from typing import overload
from PIL import ImageTk, Image, ImageGrab
from math import ceil
import pandas as pd

root = Tk()
root.title("Bucket List")

def image_resize(root: Tk, img: Image):
    max_width = root.winfo_screenwidth()
    max_height = root.winfo_screenheight()
    img_width = img.width
    img_height = img.height
    if img_width > max_width or img_height > max_height:
        resize_factor = max(ceil(img_width/max_width), ceil(img_height/max_height))
        img = img.resize((img_width//resize_factor, img_height//resize_factor))
    return img

# Get image in Tkinter accepted format
image_path = "graphics/BucketListTemplate.png"
img = Image.open(image_path)
img = image_resize(root, img)
my_img = ImageTk.PhotoImage(img)

# Create canvas using template
# This will need to be updated to right dimensions
canvas = Canvas(root, width=img.width, height= 630) #img.height)
canvas.pack()
canvas.create_image(img.width/2,img.height/2,anchor=CENTER,image=my_img)

# Read CSV file
df = pd.read_csv("data/CaymanBucketList.csv")
num_items = len(df)
# Will use in future, for now hard coded to be 36 - 6 rows of 6 boxes

# The header section is going to be a fixed distance from the top.
# Or if it isn't, it will be defined within the programme so we know
# sqr = canvas.create_rectangle(50, 125, 100, 175, fill='white')

# print(img.width, img.height)
# canvas.pack()
# we have 530 to place 5 sqrs and include margin
# we have 793 - 125 = 668 to include 8 rows and a bottom margin

# im1 = im.crop((left, top, right, bottom))
row_num = 0
col_num = 0
num_per_row = 6
imgs = []
for i, row in df.iterrows():
    x1 = 26 + (12*col_num) + (70*col_num)
    y1 = 125 + (12*row_num) + (70*row_num)
    if row["Completed"] == "Yes":
        tmp_img = Image.open(row["Link"])
        tmp_img = tmp_img.resize((70,70))
        my_tmp_img = ImageTk.PhotoImage(tmp_img)
        canvas.create_image(x1+35,y1+35,anchor=CENTER,image=my_tmp_img)
        imgs.append(my_tmp_img)
    else:
        sqr = canvas.create_rectangle(x1,y1,x1+70,y1+70, fill="white")
        quit_button = tkmac.Button(root, command = root.quit, anchor ='w',
                     width=4, highlightbackground='white', bg='white') # also kinda cool with black
        quit_button_window = canvas.create_window(x1+1, y1+1, anchor='nw', window=quit_button,
                                                height=70, width=70)
    canvas.pack()
    col_num += 1
    if (i + 1) % num_per_row == 0:
        row_num += 1
        col_num = 0

# This is what enables scrolling with the mouse:
def scroll_start(event):
    canvas.scan_mark(event.x, event.y)

def scroll_move(event):
    canvas.scan_dragto(event.x, event.y, gain=1)

canvas.bind("<ButtonPress-1>", scroll_start)
canvas.bind("<B1-Motion>", scroll_move)


canvas.scan_dragto(10, 10)

def save_img(canvas, file_name):
    # save postscipt image 
    canvas.postscript(file = file_name + '.eps') 
    # use PIL to convert to PNG 
    img = Image.open(file_name + '.eps') 
    img.save(file_name + '.png', 'png') 

# save_img(canvas, "canvas")

# canvas.postscript(file="save_canvas.ps", colormode='color')



# Zooming in! Anywhere for now
# Let's zoom in on 2nd row, 1st col where we have a pic
# def button_click(canvas: Canvas):
#     img_w, img_h = canvas.winfo_width, canvas.winfo_height
#     canvas.delete('all')

    # calculate crop rectangle
    # cw, ch = 

    #     cw, ch = iw / self.scale, ih / self.scale
    #     if cw > iw or ch > ih:
    #         cw = iw
    #         ch = ih
        # crop it
        # _x = int(iw/2 - cw/2)
        # _y = int(ih/2 - ch/2)
        # tmp = self.orig_img.crop((_x, _y, _x + int(cw), _y + int(ch)))
        # size = int(cw * self.scale), int(ch * self.scale)
        # # draw
        # self.img = ImageTk.PhotoImage(tmp.resize(size))
        # self.img_id = self.canvas.create_image(x, y, image=self.img)

root.mainloop()