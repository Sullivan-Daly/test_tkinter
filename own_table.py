from main_window import *
from tkinter import *
from tkinter import ttk
from tkinter.font import Font

class OwnTable(ttk.Frame):

    def __init__(self, parent, x_side, t_config):

        f = ttk.Frame(parent)
        f.pack(side=x_side, fill=BOTH, expand=Y)
        self.t_config = t_config
        # create the tree and scrollbars
        self.dataCols = ('text', 'timestamp', 'ID', 'user')
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
                              command=lambda ca=c: self._column_sort(ca, MenuDemo.SortDir))
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
            c = item[2]
            d = item[3]
            e = item[4]
            z = (str(a), str(b), c, d, e)
            test = self.tree.insert('', 'end', values=z)

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
