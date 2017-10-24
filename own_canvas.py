from tkinter import *
from tkinter import ttk
from math import ceil, floor, sqrt
from PIL import Image, ImageTk

import os

class OwnCanvas(ttk.Frame):
    def __init__(self, parent, t_config):
        # f = ttk.Frame(parent)
        # f.pack(side=RIGHT, fill=BOTH, expand=Y)
        self.t_config = t_config
        self.label = ttk.Label(parent)
        self.label.pack()
        image_tmp = PhotoImage(file='delete.png')
        self.label['image'] = image_tmp
        # self.f = f

        # self.image_canvas = Canvas(parent, bg='red')
        # image_tmp = ImageTk.PhotoImage(Image.open('delete.png'))
        # self.image_canvas.create_image((0, 0), image=image_tmp, anchor='nw')
        # self.t_config = t_config
        # self.image_canvas.pack()
        # self.image_canvas.update()
        # sleep(3)

    def return_frame(self):
        return self.f

    def image_loader(self, nb_images_per_tweets, event):
        self.image_canvas.delete("all")
        height = self.image_canvas.winfo_height()
        width = self.image_canvas.winfo_width()
        path_images = []
        for tweet_id in nb_images_per_tweets:
            for nb in range(nb_images_per_tweets[tweet_id]):
                # TRES TRES LENT A CAUSE DES REGEX !!!
                # reg_ex_path = self.t_config['load__path_image'] + '/' + str(tweet_id) + '_' + str(nb) + '.*'
                # file = glob.glob(reg_ex_path)
                # print(reg_ex_path)
                # print(file)
                path_png = self.t_config['load__path_image'] + '/' + str(tweet_id) + '_' + str(nb) + '.png'
                path_jpg = self.t_config['load__path_image'] + '/' + str(tweet_id) + '_' + str(nb) + '.jpg'
                if os.path.isfile(path_png):
                    path_images.append(path_png)
                elif os.path.isfile(path_jpg):
                    path_images.append(path_jpg)

        nb_images = len(path_images)
        nb_line = ceil(sqrt(nb_images))
        carre = min(height, width)
        resize = floor(carre / nb_line)
        photos = []
        for path in path_images:
            image = Image.open(path)
            image_size = image.size
            factor = resize / max(image_size[0], image_size[1])
            image = image.resize(((int(image_size[0] * factor)), int(image_size[1] * factor)), Image.ANTIALIAS)
            photos.append(ImageTk.PhotoImage(image))

        for i, photo in enumerate(photos):
            self.image_canvas.create_image((i % nb_line) * resize, floor(i / nb_line) * resize, image=photo,
                                           anchor='nw')
        self.image_canvas.update()
        # self.image_canvas.pack(side='top', fill='both', expand='yes')