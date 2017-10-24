from data_handle import *
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from math import ceil, floor, sqrt
import own_table
import os
import tkinter.filedialog as fdlg
import configparser


class CTable:
    def __init__(self):
        self.data = []
        self.ok = []
        self.nok = []
        self.ok_id = []
        self.nok_id = []


class CTmp:
    def __init__(self, parent):
        self.cv = Canvas(parent, bg='green')
        self.cv.pack(side='top', fill='both', expand='yes')
        image_tmp = ImageTk.PhotoImage(Image.open('delete.png'))
        self.cv.create_image((0, 0), image=image_tmp)
        self.cv.update()

    def get_tmp(self):
        return self.cv

class MenuDemo(ttk.Frame):
    SortDir = True

    def __init__(self, isapp=True, name='menudemo'):
        ttk.Frame.__init__(self, name=name)
        # self.pack(side=BOTTOM, expand=Y, fill=BOTH)
        self.master.title('Menu Demo')
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        self.master.geometry("%dx%d+0+0" % (w, h))
        # self.master.attributes('-zoomed', True)
        self.isapp = isapp
        self.image = ['delete.png', 'delete.png', 'delete.png', 'delete.png']
        self.t_config = self.config_reader()
        self.tData = CTable()
        print(self.t_config['load__option'])
        print(type(self.t_config['load__option']))
        if self.t_config['load__option'] == '1':
            self.handleData = CCSV(self.t_config, self.tData)
            print('csv')
        if self.t_config['load__option'] == '2':
            self.handleData = CElastic(self.t_config, self.tData)
            print('elastic')
        if self.handleData.get_tri_exist() == 0:
            self.handleData.init_tri()
        # self.data = self.elastic.search_text(['salon'])
        # self.data = self.elastic.search_user("799317915640152064")
        self.tData.ok = self.handleData.get_ok()
        self.tData.nok = self.handleData.get_nok()
        self.tData.nok_id = self.handleData.get_nok_id()
        self.tData.ok_id = self.handleData.get_ok_id()
        self.tData.data = self.handleData.get_tweets()

        print(self.tData.nok_id)
        print(self.tData.nok)
        # self.handleData.save_data('802862927342608384', 1)
        self.handleData.get_tri_exist()

        self._create_widgets()

    @staticmethod
    def config_reader():
        t_config = {}
        x_config = configparser.ConfigParser()
        x_config.read('config.ini')

        t_config['load__option'] = x_config['LOAD']['OPTION']
        t_config['load__path_file'] = x_config['LOAD']['PATH_FILE']
        t_config['load__path_image'] = x_config['LOAD']['PATH_IMAGE']
        t_config['load__es_url'] = x_config['LOAD']['ES_URL']
        t_config['load__es_index'] = x_config['LOAD']['ES_INDEX']
        t_config['load__es_doctype'] = x_config['LOAD']['ES_DOCTYPE']
        t_config['load__es_tri_name'] = x_config['LOAD']['ES_TRI_NAME']
        t_config['load__es_limit'] = x_config['LOAD']['ES_LIMIT']
        t_config['load__es_granularity'] = x_config['LOAD']['ES_GRANULARITY']
        t_config['load__es_date_begin'] = x_config['LOAD']['ES_DATE_BEGIN']
        t_config['load__es_date_end'] = x_config['LOAD']['ES_DATE_END']
        t_config['load__mongo_url'] = x_config['LOAD']['MONGO_URL']
        t_config['load__mongo_db'] = x_config['LOAD']['MONGO_DB']
        t_config['load__mongo_collection'] = x_config['LOAD']['MONGO_COLLECTION']
        t_config['display__limit'] = x_config['DISPLAY']['LIMIT']
        return t_config

    def file_dialog(self, ent):
        opts = {'initialfile': ent.get(), 'filetypes': (('CSV files', '.csv'), ('Text files', '.txt'),
                                                        ('All files', '.*'),)}
        opts['title'] = 'Select a file to open'
        fn = fdlg.asksaveasfilename(**opts)
        if fn:
            ent.delete(0, END)
            ent.insert(END, fn)

    def _create_widgets(self):
        self._create_demo_panel()

    def _create_demo_panel(self):
        # create the main menu (only displays if child of the 'root' window)
        self.master.option_add('*tearOff', False)  # disable all tearoff's
        self._menu = Menu(self.master, name='menu')
        self._build_submenus()
        self.master.config(menu=self._menu)
        self.tmp_dict = dict()
        self.tmp_dict[0] = 1

        main_panel = Frame(self.master, name='demo1')
        main_panel.pack(side=TOP, fill=BOTH, expand=1)

        pw1 = ttk.PanedWindow(main_panel, orient=HORIZONTAL)
        ttk.Separator(pw1, orient=HORIZONTAL)
        pw1.pack(side=RIGHT, expand=Y, fill=BOTH, pady=1, padx='1')

        pw2 = ttk.PanedWindow(pw1, orient=VERTICAL)
        pw2.pack(side=RIGHT, pady=3, padx='3')

        pw3 = ttk.PanedWindow(pw1, orient=VERTICAL)
        pw3.pack(side=RIGHT, pady=3, padx='3')

        pw4 = ttk.PanedWindow(pw3, orient=HORIZONTAL)
        pw4.pack(side=RIGHT, pady=3, padx='3')

        pw5 = ttk.PanedWindow(pw4, orient=HORIZONTAL)
        pw5.pack(side=RIGHT, pady=3, padx='3')

        pw1.add(pw3)
        pw1.add(pw2)

        panel_right_1 = Frame(pw1, name='right', width=200, height=200)
        panel_right_1.pack(side=TOP, fill=BOTH, expand=Y)

        panel_right_1_button = Frame(panel_right_1, name='button', width=30)
        panel_right_1_button.pack(side=BOTTOM, fill=BOTH)

        del_btn_tmp = ttk.Button(panel_right_1_button, text="DEL", width=15, name='delBtn')
        del_btn_tmp.pack(side=RIGHT, anchor=CENTER, pady='2m')

        nok_btn_tmp = ttk.Button(panel_right_1_button, text='NOK (-)', width=15, name='nokBtn')
        nok_btn_tmp.pack(side=RIGHT, anchor=CENTER, pady='2m')

        ok_btn_tmp = ttk.Button(panel_right_1_button, text='OK (+)', width=15, name='okBtn')
        ok_btn_tmp.pack(side=RIGHT, anchor=CENTER, pady='2m')

        msg1 = ["tmp"]
        lb1 = ttk.Label(panel_right_1, text=''.join(msg1))
        lb1.pack(side=TOP, pady=11)

        self.table_tmp = own_table.OwnTable(panel_right_1, RIGHT, self.t_config)

        panel_right_2 = Frame(pw2, name='right')
        panel_right_2.pack(side=TOP, fill=BOTH, expand=Y)

        msg1 = ['pic']
        lb1 = ttk.Label(panel_right_2, text=''.join(msg1))
        lb1.pack(side=TOP, padx=5, pady=5)

        # photos = []
        # for i, image in enumerate(images):
        #     print(i, " loading, ", image)
        #     try:
        #         photo = PhotoImage(file=image)
        #         photos.append(photo)
        #         print("done")
        #     except:
        #         print ("FAIL")
        #


        # for i, photo in enumerate(photos):
        #     cv.create_image(100*i, 100*i, image=photo, anchor='nw')
        #
        # cv.pack(side='top', fill='both', expand='yes')


        self.image_canvas = Canvas(panel_right_2, bg='white')
        image_tmp = ImageTk.PhotoImage(Image.open('delete.png'))
        self.image_canvas.create_image((0, 0), image=image_tmp, anchor='nw')
        self.image_canvas.pack(side=RIGHT, fill=BOTH, expand=Y)


        pw2.add(panel_right_1)
        pw2.add(panel_right_2)

        self.panel_right_2 = panel_right_2

        # self.cv = Canvas(panel_right_2, bg='green')
        # self.cv.pack(side='top', fill='both', expand='yes')
        # image_tmp = ImageTk.PhotoImage(Image.open('delete.png'))
        # self.cv.create_image((0, 0), image=image_tmp)
        # self.cv.update()

        panel_left_top = Frame(pw3, name='left_top')
        panel_left_top.pack(side=TOP)

        panel_left_top2 = Frame(panel_left_top, name='left_top')
        panel_left_top2.pack(side=TOP)

        random_btn = ttk.Button(panel_left_top2, text='RANDOM', width=15, name='randomBtn')
        random_btn.pack(side=RIGHT, anchor=CENTER, pady='2m')

        search_btn = ttk.Button(panel_left_top2, text='SEARCH', width=15, name='searchBtn')
        search_btn.pack(side=RIGHT, anchor=CENTER, pady='2m')

        filters = ('word', 'user')
        self.cb1 = ttk.Combobox(panel_left_top2, values=filters, state='readonly')
        self.cb1.pack(side=RIGHT, pady=5, padx=10)

        self.ent = ttk.Entry(panel_left_top2, width=200)
        self.ent.pack(side=LEFT, expand=Y, fill=X)

        self.table_new = own_table.OwnTable(panel_left_top, TOP, self.t_config)
        self.table_new.load_data(self.tData.data)

        tmp_btn = ttk.Button(panel_left_top, text='TMP (T)', width=25, name='tmpBtn')
        tmp_btn.pack(side=RIGHT, anchor=CENTER, pady='2m')

        rt_btn_new = ttk.Button(panel_left_top, text='RETWEET (R)', width=25, name='rtBtnNew')
        rt_btn_new.pack(side=RIGHT, anchor=CENTER, pady='2m')

        user_btn_new = ttk.Button(panel_left_top, text='USER (U)', width=25, name='userBtnNew')
        user_btn_new.pack(side=RIGHT, anchor=CENTER, pady='2m')

        nok_btn_new = ttk.Button(panel_left_top, text='NOK (-)', width=25, name='nokBtnNew')
        nok_btn_new.pack(side=RIGHT, anchor=CENTER, pady='2m')

        ok_btn_new = ttk.Button(panel_left_top, text='OK (+)', width=25, name='okBtnNew')
        ok_btn_new.pack(side=RIGHT, anchor=CENTER, pady='2m')

        pw3.add(panel_left_top)
        pw3.add(pw4)

        panel_left_bottom_2 = Frame(pw4, name='top')
        panel_left_bottom_2.pack(side=LEFT, fill=BOTH, expand=Y)

        msg4 = ["ok"]
        lb4 = ttk.Label(panel_left_bottom_2, text=''.join(msg4))
        lb4.configure(background='green')
        lb4.pack(side=TOP, padx=5, pady=5)

        panel_left_bottom_1 = Frame(pw5)
        panel_left_bottom_1.pack(side=LEFT, fill=BOTH, expand=Y)

        msg3 = ["nok"]
        lb3 = ttk.Label(panel_left_bottom_1, text=''.join(msg3))
        lb3.configure(background='red')
        lb3.pack(side=TOP, padx=5, pady=5)

        self.table_nok = own_table.OwnTable(panel_left_bottom_1, LEFT, self.t_config)
        self.table_nok.load_data(self.tData.nok)

        self.table_ok = own_table.OwnTable(panel_left_bottom_2, LEFT, self.t_config)
        self.table_ok.load_data(self.tData.ok)

        pw4.add(panel_left_bottom_2)
        pw4.add(pw5)

        pw5.add(panel_left_bottom_1)

        ok_btn_new.bind('<Button-1>', self._load_ok_new)
        nok_btn_new.bind('<Button-1>', self._load_nok_new)
        ok_btn_tmp.bind('<Button-1>', self._load_ok_tmp)
        nok_btn_tmp.bind('<Button-1>', self._load_nok_tmp)
        search_btn.bind('<Button-1>', self._load_search)
        random_btn.bind('<Button-1>', self._load_random)
        del_btn_tmp.bind('<Button-1>', self._del_tmp_selection)
        tmp_btn.bind('<Button-1>', self._load_tmp_selection)
        rt_btn_new.bind('<Button-1>', self._load_search_rt)
        user_btn_new.bind('<Button-1>', self._load_search_user)
        self.table_new.tree.bind('<ButtonRelease-1>', self._load_image_selection)
        self.table_new.tree.bind('<Shift-ButtonRelease-1>', self._load_image_selection)
        self.table_new.tree.bind('<Control-ButtonRelease-1>', self._load_image_selection)
        self.table_new.tree.bind('u', self._load_search_user)
        self.table_new.tree.bind('U', self._load_search_user)
        self.table_new.tree.bind('r', self._load_search_rt)
        self.table_new.tree.bind('R', self._load_search_rt)
        self.table_new.tree.bind('t', self._load_tmp_selection)
        self.table_new.tree.bind('T', self._load_tmp_selection)
        self.table_ok.tree.bind('<Delete>', self._del_ok_select)
        self.table_nok.tree.bind('<Delete>', self._del_nok_select)
        self.table_ok.tree.bind('<Double-Button-1>', self._del_ok_table)
        self.table_nok.tree.bind('<Double-Button-1>', self._del_nok_table)
        self.table_new.tree.bind('<Double-Button-1>', self._load_tmp_table)
        self.table_new.tree.bind('<Control-a>', self._select_all_new)
        self.table_new.tree.bind('<Control-A>', self._select_all_new)
        self.table_new.tree.bind('+', self._load_ok_new)
        self.table_new.tree.bind('-', self._load_nok_new)
        self.table_tmp.tree.bind('<Control-a>', self._select_all_tmp)
        self.table_tmp.tree.bind('<Control-A>', self._select_all_tmp)
        self.table_tmp.tree.bind('+', self._load_ok_tmp)
        self.table_tmp.tree.bind('-', self._load_nok_tmp)

        self.master.mainloop()

        # while 1:
        #     self.master.update_idletasks()
        #     self.master.update()
        #     sleep(0.01)

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

        self.image_gallery = photos

        for i, photo in enumerate(self.image_gallery):
            self.image_canvas.create_image((i % nb_line) * resize, floor(i / nb_line) * resize, image=photo,
                                           anchor='nw')
        self.image_canvas.update()
        # self.image_canvas.pack(side='top', fill='both', expand='yes')

    # def _load_image_selection(self, event):
    #     nb_images = {}
    #     widget = event.widget
    #     selection = widget.curselection()
    #     print (selection)

    # def _get_selected_tweets_image_filenames(table_new):
    #     selected_filenames = []
    #     for item_id in table_new.tree.selection():
    #         item = table_new.tree.item(item_id)
    #         str(item['values'][2])

    def _load_image_selection(self, event):
        nb_images_per_tweet = {}
        for item_id in self.table_new.tree.selection():
            item = self.table_new.tree.item(item_id)
            if item['values'] != "":
                if item['values'][4] != 0:
                    nb_images_per_tweet[item['values'][2]] = item['values'][4]
        if len(nb_images_per_tweet):
            self.image_loader(nb_images_per_tweet, event)



    def _select_all_tmp(self, event):
        for item_id in self.table_tmp.tree.get_children():
            self.table_tmp.tree.selection_add(item_id)

    def _select_all_new(self, event):
        for item_id in self.table_new.tree.get_children():
            self.table_new.tree.selection_add(item_id)

    def _load_search_rt(self, event):
        item_id = self.table_new.tree.focus()
        item = self.table_new.tree.item(item_id)
        s_tweet_id = str(item['values'][2])
        self.tData.data = self.handleData.search_retweet(s_tweet_id)
        self.table_tmp.load_data(self.tData.data)

    def _load_search_user(self, event):
        # self.table_tpm.tree.delete(*self.table_tmp.tree.get_children())
        item_id = self.table_new.tree.focus()
        item = self.table_new.tree.item(item_id)
        s_user = str(item['values'][3])
        self.tData.data = self.handleData.search_user(s_user)
        self.table_tmp.load_data(self.tData.data)

    def _del_ok_table(self, event):
        item_id = self.table_ok.tree.focus()
        item = self.table_ok.tree.item(item_id)
        h = (str(item['values'][0]), str(item['values'][1]), str(item['values'][2]), str(item['values'][3]))
        self.tData.data.append(h)
        if h in self.tData.ok:
            self.tData.ok.remove(h)
        if str(item['values'][2]) in self.tData.ok_id:
            self.tData.ok_id.remove(str(item['values'][2]))
        self.handleData.save_data(str(item['values'][2]), 0)
        self.table_new.tree.insert('', 'end', values=item['values'])
        if self.table_ok.tree.exists(item_id):
            self.table_ok.tree.delete(item_id)

    def _del_ok_select(self, event):
        print('ok')
        for item_id in self.table_ok.tree.selection():
            item = self.table_ok.tree.item(item_id)
            h = (str(item['values'][0]), str(item['values'][1]), str(item['values'][2]), str(item['values'][3]))
            self.tData.data.append(h)
            if h in self.tData.ok:
                self.tData.ok.remove(h)
            if str(item['values'][2]) in self.tData.ok_id:
                self.tData.ok_id.remove(str(item['values'][2]))
            self.handleData.save_data(str(item['values'][2]), 0)
            self.table_new.tree.insert('', 'end', values=item['values'])
            if self.table_ok.tree.exists(item_id):
                self.table_ok.tree.delete(item_id)

    def _del_nok_select(self, event):
        print('nok')
        for item_id in self.table_nok.tree.selection():
            item = self.table_nok.tree.item(item_id)
            h = (str(item['values'][0]), str(item['values'][1]), str(item['values'][2]), str(item['values'][3]))
            self.tData.data.append(h)
            if h in self.tData.nok:
                self.tData.nok.remove(h)
            if str(item['values'][2]) in self.tData.nok_id:
                self.tData.nok_id.remove(str(item['values'][2]))
            self.handleData.save_data(str(item['values'][2]), 0)
            self.table_new.tree.insert('', 'end', values=item['values'])
            if self.table_nok.tree.exists(item_id):
                self.table_nok.tree.delete(item_id)

    def _del_nok_table(self, event):
        item_id = str(self.table_nok.tree.focus())
        item = self.table_nok.tree.item(item_id)
        h = (str(item['values'][0]), str(item['values'][1]), str(item['values'][2]), str(item['values'][3]))
        self.tData.data.append(h)
        if h in self.tData.nok:
            self.tData.nok.remove(h)
        if str(item['values'][2]) in self.tData.nok_id:
            self.tData.nok_id.remove(str(item['values'][2]))
        self.handleData.save_data(str(item['values'][2]), 0)
        self.table_new.tree.insert('', 'end', values=item['values'])
        if self.table_nok.tree.exists(item_id):
            self.table_nok.tree.delete(item_id)

    def _load_ok_new(self, event):
        for item_id in self.table_new.tree.selection():
            item = self.table_new.tree.item(item_id)
            h = (str(item['values'][0]), str(item['values'][1]), str(item['values'][2]), str(item['values'][3]))
            self.tData.ok.append(h)
            self.tData.ok_id.append(str(item['values'][2]))
            self.handleData.save_data(str(item['values'][2]), 1)
            if h in self.tData.data:
                self.tData.data.remove(h)
            if self.table_new.tree.exists(item_id):
                self.table_new.tree.delete(item_id)
            self.table_ok.tree.insert('', 'end', values=item['values'])

    def _load_nok_new(self, event):
        for item_id in self.table_new.tree.selection():
            item = self.table_new.tree.item(item_id)
            h = (str(item['values'][0]), str(item['values'][1]), str(item['values'][2]), str(item['values'][3]))
            self.tData.nok.append(h)
            self.tData.nok_id.append(str(item['values'][2]))
            self.handleData.save_data(str(item['values'][2]), -1)
            if h in self.tData.data:
                self.tData.data.remove(h)
            if self.table_new.tree.exists(item_id):
                self.table_new.tree.delete(item_id)
            self.table_nok.tree.insert('', 'end', values=item['values'])

    def _load_ok_tmp(self, event):
        for item_id in self.table_tmp.tree.selection():
            item = self.table_tmp.tree.item(item_id)
            h = (str(item['values'][0]), str(item['values'][1]), str(item['values'][2]), str(item['values'][3]))
            for item_new in self.table_new.tree.get_children():
                item_del = self.table_new.tree.item(item_new)
                if item['values'][2] == item_del['values'][2]:
                    if h in self.tData.data:
                        self.tData.data.remove(h)
                    if self.table_new.tree.exists(item_new):
                        self.table_new.tree.delete(item_new)
            self.tData.ok.append(h)
            self.tData.ok_id.append(str(item['values'][2]))
            self.handleData.save_data(str(item['values'][2]), 1)
            self.table_ok.tree.insert('', 'end', values=item['values'])
            if self.table_tmp.tree.exists(item_id):
                self.table_tmp.tree.delete(item_id)

    def _load_nok_tmp(self, event):
        for item_id in self.table_tmp.tree.selection():
            item = self.table_tmp.tree.item(item_id)
            h = (str(item['values'][0]), str(item['values'][1]), str(item['values'][2]), str(item['values'][3]))
            for item_new in self.table_new.tree.get_children():
                item_del = self.table_new.tree.item(item_new)
                if str(item['values'][2]) == str(item_del['values'][2]):
                    if h in self.tData.data:
                        self.tData.data.remove(h)
                    if self.table_new.tree.exists(item_id):
                        self.table_new.tree.delete(item_new)
            self.tData.nok.append(h)
            self.tData.nok_id.append(str(item['values'][2]))
            self.handleData.save_data(str(item['values'][2]), -1)
            self.table_nok.tree.insert('', 'end', values=item['values'])
            if self.table_tmp.tree.exists(item_id):
                self.table_tmp.tree.delete(item_id)

    def _del_tmp_selection(self, event):
        for item_id in self.table_tmp.tree.selection():
            item = self.table_tmp.tree.item(item_id)
            print(item['values'])
            if item['values'][2] in self.tmp_dict:
                del self.tmp_dict[item['values'][2]]
            if self.table_tmp.tree.exists(item_id):
                self.table_tmp.tree.delete(item_id)

    def _load_tmp_table(self, event):
        item_id = str(self.table_new.tree.focus())
        item = self.table_new.tree.item(item_id)
        if not self.tmp_dict.get(item['values'][2]):
            self.tmp_dict[item['values'][2]] = 1
            self.table_tmp.tree.insert('', 'end', values=item['values'])

    def _load_tmp_selection(self, event):
        for item_id in self.table_new.tree.selection():
            item = self.table_new.tree.item(item_id)
            if not self.tmp_dict.get(item['values'][2]):
                self.tmp_dict[item['values'][2]] = 1
                self.table_tmp.tree.insert('', 'end', values=item['values'])

    def _load_search(self, event):
        self.table_new.tree.delete(*self.table_new.tree.get_children())
        if self.cb1.get() == 'word':
            t_words = self.ent.get().split(' ')
            self.tData.data = self.handleData.search_text(t_words)
            self.table_new.load_data(self.tData.data)
        if self.cb1.get() == 'user':
            s_user = self.ent.get()
            self.tData.data = self.handleData.search_user(s_user)
            self.table_new.load_data(self.tData.data)

    def _load_random(self, event):
        self.table_new.tree.delete(*self.table_new.tree.get_children())
        self.tData.data = self.handleData.get_tweets()
        self.table_new.load_data(self.tData.data)

        # for i, item in enumerate(self.tData.data):
        #     if i >= int(self.t_config['display__limit']):
        #         break
        #     self.table_new.tree.insert('', 'end', values=item)

    def _build_submenus(self):
        # create the submenus
        # the routines are essentially the same:
        #    1. create the submenu, passing the main menu as parent
        #    2. add the submenu to the main menu as a 'cascade'
        #    3. add the submenu's individual items

        self._add_file_menu()
        self._add_more_menu()

    # ================================================================================
    # Submenu routines
    # ================================================================================

    # File menu ------------------------------------------------------------------
    def _add_file_menu(self):
        f_menu = Menu(self._menu, name='fmenu')
        self._menu.add_cascade(label='File', menu=f_menu, underline=0)

        f_menu.add_command(label='Open/Connect')
        f_menu.add_command(label='Save')
        f_menu.add_command(label='Save as...')

        f_menu.add_separator()
        f_menu.add_command(label='Exit Demo', command=lambda: self.master.destroy())

    def _add_more_menu(self):
        menu = Menu(self._menu)
        self._menu.add_cascade(label='More', menu=menu, underline=0)

        labels = ('An entry', 'Another entry', 'Does nothing',
                  'Does almost nothing', 'Make life meaningful')

        for item in labels:
            menu.add_command(label=item)

