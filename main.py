# coding: utf-8
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from elasticsearch import Elasticsearch
import tkinter.filedialog as fdlg
import string

import sys
import configparser


class OwnTable(ttk.Frame):
    def __init__(self, parent, x_side, t_config):

        f = ttk.Frame(parent)
        f.pack(side=x_side, fill=BOTH, expand=Y)
        self.t_config = t_config
        # create the tree and scrollbars
        self.dataCols = ('ID', 'text', 'user')
        self.tree = ttk.Treeview(columns=self.dataCols, show='headings')

        ysb = ttk.Scrollbar(orient=VERTICAL, command=self.tree.yview)
        # xsb = ttk.Scrollbar(orient=HORIZONTAL, command=self.tree.xview)
        self.tree['yscroll'] = ysb.set
        # self.tree['xscroll'] = xsb.set

        # add tree and scrollbars to frame
        self.tree.grid(in_=f, row=0, column=0, sticky=NSEW)
        ysb.grid(in_=f, row=0, column=1, sticky=NS)
        # xsb.grid(in_=f, row=1, column=0, sticky=EW)

        # set frame resize priorities
        f.rowconfigure(0, weight=10)
        f.columnconfigure(0, weight=10)

        # configure column headings
        for c in self.dataCols:
            self.tree.heading(c, text=c.title(),
                              command=lambda c=c: self._column_sort(c, MenuDemo.SortDir))
            self.tree.column(c, width=Font().measure(c.title()))

        self.f = f

    def return_frame(self):
        return self.f

    def load_data(self, data):
        i = 0
        # add data to the tree
        for i, item in enumerate(data):
            if i >= int(self.t_config['display__limit']):
                break
            i += 1
            a = item[0]
            b = item[1]
            h = item[2]
            z = (a, str(b), str(h))
            test = self.tree.insert('', 'end', values=z)

            if not i%10000 :
                print(i)
            # # and adjust column widths if necessary
            # for idx, val in enumerate(item):
            #     iwidth = Font().measure(val)
            #     if self.tree.column(self.dataCols[idx], 'width') < iwidth:
            #         self.tree.column(self.dataCols[idx], width=iwidth)


    def _column_sort(self, col, descending=False):

        # grab values to sort as a list of tuples (column value, column id)
        # e.g. [('Argentina', 'I001'), ('Australia', 'I002'), ('Brazil', 'I003')]
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]

        # reorder data
        # tkinter looks after moving other items in
        # the same row
        data.sort(reverse=descending)
        for indx, item in enumerate(data):
            self.tree.move(item[1], '', indx)  # item[1] = item Identifier

        # reverse sort direction for next sort operation
        MenuDemo.SortDir = not descending


class MenuDemo(ttk.Frame):

    SortDir = True

    def __init__(self, isapp=True, name='menudemo'):
        ttk.Frame.__init__(self, name=name)
        # self.pack(side=BOTTOM, expand=Y, fill=BOTH)
        self.master.title('Menu Demo')
        self.isapp = isapp
        self.image = 'delete.png'
        self.t_config = self.config_reader()
        self.elastic = cElastic(self.t_config)
        # self.data = self.elastic.search_text(['salon'])
        # self.data = self.elastic.search_user("799317915640152064")
        # self.data = self.elastic.getTweets()
        self._create_widgets()

    @staticmethod
    def config_reader():
        t_config = {}
        x_config = configparser.ConfigParser()
        x_config.read('config.ini')

        t_config['load__option'] = x_config['LOAD']['OPTION']
        t_config['load__path_file'] = x_config['LOAD']['PATH_FILE']
        t_config['load__es_url'] = x_config['LOAD']['ES_URL']
        t_config['load__es_index'] = x_config['LOAD']['ES_INDEX']
        t_config['load__es_doctype'] = x_config['LOAD']['ES_DOCTYPE']
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
        main_panel.pack(side=TOP, fill=BOTH, expand=Y)

        pw1 = ttk.PanedWindow(main_panel, orient=HORIZONTAL)
        pw1.pack(side=RIGHT, expand=Y, fill=BOTH, pady=3, padx='3')

        pw2 = ttk.PanedWindow(pw1, orient=VERTICAL)
        pw2.pack(side=RIGHT, expand=Y, fill=BOTH, pady=3, padx='3')

        pw3 = ttk.PanedWindow(pw1, orient=VERTICAL)
        pw3.pack(side=RIGHT, expand=Y, fill=BOTH, pady=3, padx='3')

        pw4 = ttk.PanedWindow(pw3, orient=HORIZONTAL)
        pw4.pack(side=RIGHT, expand=Y, fill=BOTH, pady=3, padx='3')

        pw5 = ttk.PanedWindow(pw4, orient=HORIZONTAL)
        pw5.pack(side=RIGHT, expand=Y, fill=BOTH, pady=3, padx='3')

        pw1.add(pw3)
        pw1.add(pw2)

        panel_right_1 = Frame(pw1, name='right')
        panel_right_1.pack(side=TOP, fill=BOTH, expand=Y)

        panel_right_1_button = Frame(panel_right_1, name='button', width=30)
        panel_right_1_button.pack(side=BOTTOM, fill=BOTH)

        ok_btn = ttk.Button(panel_right_1_button, text='OK', width=15, name='okBtn')
        ok_btn.pack(side=RIGHT, anchor=CENTER, pady='2m')

        nok_btn = ttk.Button(panel_right_1_button, text='NOK', width=15, name='nokBtn')
        nok_btn.pack(side=RIGHT, anchor=CENTER, pady='2m')

        del_btn = ttk.Button(panel_right_1_button, text="DEL", width=15, name='delBtn')
        del_btn.pack(side=RIGHT, anchor=CENTER, pady='2m')

        msg1 = ["tmp"]
        lb1 = ttk.Label(panel_right_1, text=''.join(msg1))
        lb1.pack(side=TOP, padx=5, pady=5)

        self.table_tmp = OwnTable(panel_right_1, RIGHT, self.t_config)

        panel_right_2 = Frame(pw2, name='right')
        panel_right_2.pack(side=TOP, fill=BOTH, expand=Y)

        msg1 = ['pic']
        lb1 = ttk.Label(panel_right_2, text=''.join(msg1))
        lb1.pack(side=TOP, padx=5, pady=5)

        self.im = PhotoImage(file=self.image)
        lbl = ttk.Label(panel_right_2, image=self.im, relief=SUNKEN, border=2)
        lbl.image = self.im
        lbl.pack(side=TOP, padx='.5m', pady='.5m')

        pw2.add(panel_right_1)
        pw2.add(panel_right_2)

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

        self.table_new = OwnTable(panel_left_top, TOP, self.t_config)
        self.table_new.load_data(self.data)

        tmp_btn = ttk.Button(panel_left_top, text='TMP', width=25, name='tmpBtn')
        tmp_btn.pack(side=RIGHT, anchor=CENTER, pady='2m')

        pw3.add(panel_left_top)
        pw3.add(pw4)

        panel_left_bottom_1 = Frame(pw4)
        panel_left_bottom_1.pack(side=LEFT, fill=BOTH, expand=Y)

        msg3 = ["nok"]
        lb3 = ttk.Label(panel_left_bottom_1, text=''.join(msg3))
        lb3.configure(background='red')
        lb3.pack(side=TOP, padx=5, pady=5)

        self.table_nok = OwnTable(panel_left_bottom_1, LEFT, self.t_config)

        panel_left_bottom_2 = Frame(pw5, name='top')
        panel_left_bottom_2.pack(side=LEFT, fill=BOTH, expand=Y)

        msg4 = ["ok"]
        lb4 = ttk.Label(panel_left_bottom_2, text=''.join(msg4))
        lb4.configure(background='green')
        lb4.pack(side=TOP, padx=5, pady=5)

        self.table_ok = OwnTable(panel_left_bottom_2, LEFT, self.t_config)

        pw4.add(panel_left_bottom_1)
        pw4.add(pw5)

        pw5.add(panel_left_bottom_2)

        ok_btn.bind('<Button-1>', self._load_ok)
        nok_btn.bind('<Button-1>', self._load_nok)
        search_btn.bind('<Button-1>', self._load_search)
        random_btn.bind('<Button-1>', self._load_random)
        del_btn.bind('<Button-1>', self._del_tmp_selection)
        tmp_btn.bind('<Button-1>', self._load_tmp_selection)
        self.table_ok.tree.bind('<Double-Button-1>', self._del_ok_table)
        self.table_nok.tree.bind('<Double-Button-1>', self._del_nok_table)
        # self.table_tmp.tree.bind('<Double-Button-1>', self._change_picture)
        self.table_new.tree.bind('<Double-Button-1>', self._load_tmp_table)
        self.table_new.tree.bind('<Control-a>', self._select_all_new)
        self.table_new.tree.bind('<Control-A>', self._select_all_new)
        self.table_tmp.tree.bind('<Control-a>', self._select_all_tmp)
        self.table_tmp.tree.bind('<Control-A>', self._select_all_tmp)

    # def _change_picture(self,event):
    #     item_id = str(self.table_ok.tree.focus())
    #     item = self.table_ok.tree.item(item_id)

    def _select_all_tmp(self, event):
        for item_id in self.table_tmp.tree.get_children():
            # item = self.table_tmp.tree.item(item_id)
            self.table_tmp.tree.selection_add(item_id)

    def _select_all_new(self, event):
        for item_id in self.table_new.tree.get_children():
            # item = self.table_new.tree.item(item_id)
            self.table_new.tree.selection_add(item_id)

    def _del_ok_table(self, event):
        item_id = self.table_ok.tree.focus()
        item = self.table_ok.tree.item(item_id)
        h = (str(item['values'][0]), str(item['values'][1]), str(item['values'][2]))
        self.data.append(h)
        del self.tmp_dict[item['values'][0]]
        self.table_new.tree.insert('', 'end', values=item['values'])
        self.table_ok.tree.delete(item_id)


    def _del_nok_table(self, event):
        item_id = str(self.table_nok.tree.focus())
        item = self.table_nok.tree.item(item_id)
        h = (str(item['values'][0]), str(item['values'][1]), str(item['values'][2]))
        self.data.append(h)
        del self.tmp_dict[item['values'][0]]
        self.table_new.tree.insert('', 'end', values=item['values'])
        self.table_nok.tree.delete(item_id)

    def _load_ok(self, event):
        for item_id in self.table_tmp.tree.selection():
            item = self.table_tmp.tree.item(item_id)
            for item_new in self.table_new.tree.get_children():
                item_del = self.table_new.tree.item(item_new)
                if item['values'][0] == item_del['values'][0]:
                    h = (str(item['values'][0]), str(item['values'][1]), str(item['values'][2]))
                    self.data.remove(h)
                    self.table_new.tree.delete(item_new)
            self.table_ok.tree.insert('', 'end', values=item['values'])
            self.table_tmp.tree.delete(item_id)

    def _load_nok(self, event):
        for item_id in self.table_tmp.tree.selection():
            item = self.table_tmp.tree.item(item_id)
            for item_new in self.table_new.tree.get_children():
                item_del = self.table_new.tree.item(item_new)
                if str(item['values'][0]) == str(item_del['values'][0]):
                    h = (str(item['values'][0]), str(item['values'][1]), str(item['values'][2]))
                    print(h)
                    self.data.remove(h)
                    self.table_new.tree.delete(item_new)
            self.table_nok.tree.insert('', 'end', values=item['values'])
            self.table_tmp.tree.delete(item_id)

    def _del_tmp_selection(self, event):
        for item_id in self.table_tmp.tree.selection():
            item = self.table_tmp.tree.item(item_id)
            print(item['values'])
            del self.tmp_dict[item['values'][0]]
            # self.table_new.tree.insert('', 'end', values=item['values'])
            self.table_tmp.tree.delete(item_id)

    def _load_tmp_table(self, event):
        item_id = str(self.table_new.tree.focus())
        item = self.table_new.tree.item(item_id)
        if not self.tmp_dict.get(item['values'][0]):
            self.tmp_dict[item['values'][0]] = 1
            self.table_tmp.tree.insert('', 'end', values=item['values'])

    def _load_tmp_selection(self, event):
        for item_id in self.table_new.tree.selection():
            item = self.table_new.tree.item(item_id)
            if not self.tmp_dict.get(item['values'][0]):
                self.tmp_dict[item['values'][0]] = 1
                self.table_tmp.tree.insert('', 'end', values=item['values'])

    def _load_search(self, event):
        if self.cb1.get() == 'word':
            for i in self.table_new.tree.get_children():
                item = self.table_new.tree.item(i)
                if item['values'][1].find(self.ent.get()) < 0:
                    self.table_new.tree.delete(i)
        if self.cb1.get() == 'user':
            for i in self.table_new.tree.get_children():
                item = self.table_new.tree.item(i)
                if str(item['values'][2]) != self.ent.get():
                    self.table_new.tree.delete(i)

    def _load_random(self, event):
        self.table_new.tree.delete(*self.table_new.tree.get_children())
        for i, item in enumerate(self.data):
            if i >= int(self.t_config['display__limit']):
                break
            self.table_new.tree.insert('', 'end', values=item)

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

    def csv_data_load(self):
        with open(self.t_config['load__path_file'], "r", encoding='utf16') as file:
            i = 0
            for row in file:
                if i == 0:
                    i += 1
                else:
                    h = row[1:].split('; ', maxsplit=3)
                    printable = set(string.printable)
                    # tmp = filter(lambda x: x in printable, h[2][1:-3])
                    tmp = h[2][1:-3].encode('ascii', errors='ignore').decode()
                    print(h[0])
                    x = (int(h[0]), str(tmp), str(h[1]))
                    # print(x)
                    self.data.append(x)
        print('DONE')


class CHandleEs:
    def __init__(self):
        self.sCluster = ''

#    def __init__(self, sName):
#        self.sCluster = sName

    def connectionToEs(self):
        if len(self.sCluster):
            es = Elasticsearch(cluster=self.sCluster)
        else:
            es = Elasticsearch()
        return es


class cData:
    def __init__(self):
        pass

    def getTweets(self):
        pass

    def search_text(self):
        pass

    def search_user(self):
        pass

class cCSV(cData):
    def __init__(self, t_config):
        self.t_config = t_config
        self.path = t_config['load__path_file']
        self.data = []
        with open(self.t_config['load__path_file'], "r", encoding='utf16') as file:
            i = 0
            for row in file:
                if i == 0:
                    i += 1
                else:
                    h = row[1:].split('; ', maxsplit=3)
                    tmp = h[2][1:-3].encode('ascii', errors='ignore').decode()
                    x = (int(h[0]), str(tmp), str(h[1]))
                    self.data.append(x)

    def getTweets(self):
        return self.data

    def search_text(self, tKeyWords):




class cElastic(cData):
    def __init__(self, t_config):
        self.sCluster = ''
        self.t_config = t_config
        self.xEs = self._connectionToEs()
        self.sLimit = t_config['load__es_limit']
        self.sIndexName = t_config['load__es_index']
        self.sDocTypeName = t_config['load__es_doctype']
        self.sDateBegin = t_config['load__es_date_begin'] + '000'
        self.sDateEnd = t_config['load__es_date_end'] + '000'

    def _connectionToEs(self):
        if len(self.sCluster):
            es = Elasticsearch(cluster=self.sCluster)
        else:
            es = Elasticsearch()
        return es

    def getTweets(self):
        self.nCurrentSize = 1
        self.nIndexSize = int(self.xEs.count(index = self.sIndexName)['count'])
        self.xIdPack = {}

        lFields = ['id_str', 'text', 'user.id_str']

        xResponse = self.xEs.search(index=self.sIndexName, doc_type=self.sDocTypeName, scroll='10m', sort = ['timestamp_ms:asc'],
                                    _source=lFields, stored_fields=lFields, size=self.sLimit,
                                    body={'query': {'match_all': {}}})

        print(xResponse)

        self.nIndexSize = int(xResponse['hits']['total'])
        print(self.nIndexSize)

        data = self._return_from_scroll(xResponse)
        return data

    def search_text(self, tKeyWords):
        self.nCurrentSize = 1
        self.nIndexSize = int(self.xEs.count(index = self.sIndexName)['count'])
        self.xIdPack = {}

        sKeyWords = '"'
        nWords = 0
        for word in tKeyWords:
            sKeyWords += word
            sKeyWords += ' '
            nWords += 1
        sKeyWords = sKeyWords[:-1]
        sKeyWords += '"'

        xResponse = self.xEs.search(index=self.sIndexName, doc_type=self.sDocTypeName, scroll='10m',
                                    body={"query": {"bool":
                                        {"must": [
                                            {"match":
                                                 {"text":
                                                      {"query": sKeyWords, "operator": "or",
                                                       "minimum_should_match": nWords}}},
                                            {'range': {'timestamp_ms': {'gte': self.sDateBegin,
                                                                        'lte': self.sDateEnd}}}
                                        ]}}})

        self.nIndexSize = int(xResponse['hits']['total'])
        print("%d documents found" % xResponse['hits']['total'])

        data = self._return_from_scroll(xResponse)

        return data

    def search_user(self, sUserId):
        self.nCurrentSize = 1
        self.nIndexSize = int(self.xEs.count(index = self.sIndexName)['count'])
        self.xIdPack = {}

        xResponse = self.xEs.search(index=self.sIndexName, doc_type=self.sDocTypeName, scroll='10m',
                                    body={"query": {"bool":
                                        {"must": [
                                            {"match":
                                                 {"user.id_str":
                                                      {"query": sUserId}}},
                                            {'range': {'timestamp_ms': {'gte': self.sDateBegin,
                                                                        'lte': self.sDateEnd}}}
                                        ]}}})

        self.nIndexSize = int(xResponse['hits']['total'])
        print("%d documents found" % xResponse['hits']['total'])

        data = self._return_from_scroll(xResponse)

        return data

    def _return_from_scroll(self, xResponse):
        data = []
        nCmpt = 0

        sScroll = xResponse['_scroll_id']
        for hit in xResponse['hits']['hits']:
            self.xIdPack.update({hit['_source']['id_str']: 1})
            test = (hit['_source']['id_str'], hit['_source']['text'].encode('ascii', errors='ignore').decode(),
                    hit['_source']['user']['id_str'])
            data.append(test)
            self.nCurrentSize += 1
            nCmpt += 1
        print('Taille index : ' + str(self.nIndexSize))

        print(nCmpt)
        nCmpt += 1

        while (nCmpt < self.nIndexSize and nCmpt < int(self.sLimit)):
            try:
                print('boucle')
                nCmpt -= 1
                xResponse = self.xEs.scroll(scroll_id=sScroll, scroll='10s')
                sScroll = xResponse['_scroll_id']
                for hit in xResponse['hits']['hits']:
                    # self.xIdPack.update({hit['_source']['id_str']:1})
                    test = (hit['_source']['id_str'], hit['_source']['text'].encode('ascii', errors='ignore').decode(),
                            hit['_source']['user']['id_str'])
                    nCmpt += 1
                    data.append(test)
                nCmpt += 1
            except:
                print('test')
                break

        print('toto')
        return data

if __name__ == '__main__':
    MenuDemo().mainloop()
