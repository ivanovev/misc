
import tkinter as tk
from util import Control, Data, MyAIO, Obj, dev_io_cb, proxy
from util.columns import *

class Scdp(Control):
    def __init__(self, dev=None, parent=None, title='Screenshot', get_data=None, iw=480, ih=234):
        data = Data()
        self.fileext = 'bmp'
        self.get_data = get_data
        self.iw = iw
        self.ih = ih
        self.isz = self.iw*self.ih
        Control.__init__(self, data=data, dev=dev, parent=parent, title=title)

    def init_io(self):
        self.io = MyAIO(self)
        self.io.add(self.scdp_cb1, self.ctrl_cb2, self.scdp_cb3, proxy.io_cb)

    def init_layout(self):
        self.f1 = tk.Frame(self.frame)
        self.f1.grid(column=0, row=0)
        #self.frame.columnconfigure(0, weight=1)
        #self.frame.rowconfigure(0, weight=1)
        self.img = tk.PhotoImage()
        self.c = tk.Canvas(self.f1, width=self.iw, height=self.ih)
        #self.c.pack(expand=1, fill=tk.BOTH)
        self.add_widget_with_scrolls(self.f1, self.c)
        self.imgid = self.c.create_image(0, 0, image=self.img, anchor=tk.NW)
        self.add_fb()
        self.add_button(self.fb, 'Close', self.root.destroy)
        self.add_button(self.fb, 'Save As', self.filesaveas_cb)
        self.add_button(self.fb, 'Zoom', self.zoom_cb)
        self.add_button(self.fb, 'Update', self.update_cb)

    def update_cb(self):
        self.io_start()

    def zoom_cb(self):
        if hasattr(self, 'data'):
            img = self.img.zoom(2, 2)
            print(img.width())
            self.c.itemconfig(self.imgid, image=img)
            self.c.configure(width=img.width(), height=img.height())
            self.img = img

    def filesave(self, fname):
        f = open(fname, 'wb')
        f.write(self.scdp)
        f.close()

    def scdp_cb1(self):
        if not self.get_data:
            return False
        cmd = dev_io_cb(self.data.dev, 'dispose')
        print(cmd)
        obj = Obj(cmdid='tmp', cmd=cmd, dev=self.data.dev, srv=self.data.dev[c_server])
        self.io.qo.put(obj)
        return True

    def scdp_cb3(self):
        print('cb3')
        scdp = self.get_data()
        row = 0
        col = 0
        start = 56
        for i in range(0, self.isz):
            p = start + i*3
            self.img.put('#%02x%02x%02x' % (scdp[p], scdp[p+2], scdp[p+1]), (col, self.ih-row-1))
            col += 1
            if col == self.iw:
                row +=1; col = 0
        self.scdp = scdp 
        return True

