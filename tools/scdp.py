
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
        self.z = 1
        Control.__init__(self, data=data, dev=dev, parent=parent, title=title)

    def init_io(self):
        self.io = MyAIO(self)
        self.io.add(self.scdp_cb1, self.ctrl_cb2, self.scdp_cb3, proxy.io_cb)

    def init_layout(self):
        self.f1 = tk.Frame(self.frame)
        self.f1.grid(column=0, row=0, sticky=tk.NSEW)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.c = tk.Canvas(self.f1, width=self.iw, height=self.ih)
        #self.c.pack(expand=1, fill=tk.BOTH)
        self.scrx, self.scry = self.add_widget_with_scrolls(self.f1, self.c)
        self.img = tk.PhotoImage()
        self.imgid = self.c.create_image(0, 0, image=self.img, anchor=tk.NW)
        self.add_fb()
        self.add_button(self.fb, 'Close', self.root.destroy)
        self.add_button(self.fb, 'Save as', self.filesaveas_cb)
        self.add_button(self.fb, 'Zoom out', self.zoomout_cb)
        self.add_button(self.fb, 'Zoom in', self.zoomin_cb)
        self.add_button(self.fb, 'Update', self.update_cb)
        #self.add_button(self.fb, 'Test', self.test_cb)
        self.c.bind("<ButtonPress-1>", self.start_move_cb)
        self.c.bind("<ButtonRelease-1>", self.stop_move_cb)
        self.c.bind("<B1-Motion>", self.motion_cb)

    def start_move_cb(self, evt):
        self.x0, self.x1 = self.scrx.get()
        self.y0, self.y1 = self.scry.get()
        self.x = evt.x
        self.y = evt.y
        self.xx = (self.x0 + self.x1)/2

    def stop_move_cb(self, evt):
        self.x = None
        self.y = None

    def motion_cb(self, evt):
        deltax = float(evt.x - self.x)
        deltay = float(evt.y - self.y)
        def newxy(wh, xy0, delta):
            xy0 = xy0 - delta/wh
            xy0 = max(0, xy0)
            xy0 = min(xy0, 1)
            return xy0
        if self.x0 != 0 or self.x1 != 1:
            self.c.xview_moveto(newxy(self.iw*self.z, self.x0, deltax))
        if self.y0 != 0 or self.y1 != 1:
            self.c.yview_moveto(newxy(self.ih*self.z, self.y0, deltay))
        #x = self.root.winfo_x() + deltax
        #y = self.root.winfo_y() + deltay
        #self.root.geometry("+%s+%s" % (x, y))

    def test_cb(self):
        self.c.coords(self.imgid, 200, 200)

    def update_cb(self):
        self.io_start()

    def zoom(self, z=1):
        if not hasattr(self, 'data'):
            return
        self.img1 = self.img.zoom(z, z)
        self.c.itemconfig(self.imgid, image=self.img1)
        self.c.config(scrollregion=self.c.bbox(tk.ALL))
        self.z = z

    def zoomin_cb(self):
        self.zoom(self.z + 1)

    def zoomout_cb(self):
        if self.z > 1:
            self.zoom(self.z - 1)

    def filesave(self, fname):
        f = open(fname, 'wb')
        f.write(self.scdp)
        f.close()

    def scdp_cb1(self):
        if not self.get_data:
            return False
        cmd = dev_io_cb(self.data.dev, 'dispose')
        obj = Obj(cmdid='tmp', cmd=cmd, dev=self.data.dev, srv=self.data.dev[c_server])
        self.io.qo.put(obj)
        return True

    def scdp_cb3(self):
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
        self.zoom(self.z)
        self.scdp = scdp 
        return True

