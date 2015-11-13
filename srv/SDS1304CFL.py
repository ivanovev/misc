
import usb
import usb.util
import pdb
from datetime import datetime
try:
    import usbtmc
except:
    pass

def get_instr():
    try:
        if hasattr(get_instr, 'instr'):
            return get_instr.instr
        instr = usbtmc.Instrument(0xF4EC, 0xEE3A)
        get_instr.instr = instr
        return instr
    except:
        pass

def usbtmc_io(cmd, read=True):
    instr = get_instr()
    if instr:
        instr.write(cmd)
        if read:
            return instr.read()
    return ''

def SDS1304CFL_cmd(cmd='*IDN?', *args):
    """
    SDS1304CFL cmd io
    """
    if len(args):
        cmd += ' ' + ' '.join(args)
    read = cmd[-1] == '?'
    val = cmd.split(' ')[-1]
    ret = usbtmc_io(cmd, read)
    return ret if read else val

def SDS1304CFL_dispose():
    if hasattr(get_instr, 'instr'):
        usb.util.dispose_resources(get_instr.instr.device)
        delattr(get_instr, 'instr')
    return '0'

def get_data(dispose_dev=False):
    usbtmc_io('SCDP', False)
    instr = get_instr()
    data = instr.read_raw()
    if dispose_dev:
        SDS1304CFL_dispose()
    return data

def test1():
    import tkinter as tk
    data = get_data()
    wnd = tk.Tk()
    t1 = datetime.now()
    w = 480
    h = 234
    sz = w*h
    img = tk.PhotoImage(width=w, height=h)
    row = 0
    col = 0
    start = 56
    counter = 0
    pixels = []
    for i in range(0, sz):
        p = start + i*3
        img.put('#%02x%02x%02x' % (data[p], data[p+2], data[p+1]), (col, h-row-1))
        col += 1
        if col == w:
            row +=1; col = 0
    img.zoom(2, 2)
    c = tk.Canvas(wnd, width=w, height=h); c.pack()
    c.create_image(0, 0, image = img, anchor=tk.NW)
    t2 = datetime.now()
    dt = t2 - t1
    dt = dt.seconds + float(dt.microseconds)/10e6
    print('duration2: %.3f' % dt)
    wnd.mainloop()

def test2():
    import tkinter as tk
    from PIL import Image, ImageTk
    data = get_data()
    wnd = tk.Tk()
    t1 = datetime.now()
    w = 480
    h = 234
    start = 54
    im = Image.frombytes('RGB', (w, h), data[start:])
    img = ImageTk.PhotoImage(im)
    c = tk.Canvas(wnd, width=w, height=h); c.pack()
    c.create_image(0, 0, image = img, anchor=tk.NW)
    t2 = datetime.now()
    dt = t2 - t1
    dt = dt.seconds + float(dt.microseconds)/10e6
    print('duration2: %.3f' % dt)
    wnd.mainloop()

def main():
    t1 = datetime.now()
    test1()
    t2 = datetime.now()
    dt = t2 - t1
    dt = dt.seconds + float(dt.microseconds)/10e6
    #print('duration: %.3f' % dt)

if __name__ == '__main__':
    main()

