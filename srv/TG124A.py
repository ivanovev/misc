
import argparse, sys
try:
    import usb
except:
    pass

def get_device():
    if hasattr(get_device, 'dev'):
        return get_device.dev
    dev = usb.core.find(idVendor=0x0403, idProduct=0x6001)
    if dev == None:
        return
    print('tg_init')
    try:
        if dev.is_kernel_driver_active(0):
            dev.detach_kernel_driver(0)
    except:
        pass
    dev.set_configuration()
    cfg = dev.get_active_configuration()
    intf = cfg[(0,0)]
    e = usb.util.find_descriptor(intf, bEndpointAddress = 0x81)
    dev.ctrl_transfer(0x40, 0, 0, 0)
    usb.control.clear_feature(dev, usb.control.ENDPOINT_HALT, e)
    dev.ctrl_transfer(0xC0, 5, 0, 0, 2)
    dev.ctrl_transfer(0x40, 0, 0, 0)
    usb.control.clear_feature(dev, usb.control.ENDPOINT_HALT, e)
    dev.ctrl_transfer(0xC0, 5, 0, 0, 2)
    dev.ctrl_transfer(0x40, 3, 0x78, 0)
    dev.ctrl_transfer(0x40, 9, 2, 0)
    get_device.dev = dev
    return dev

def tg_usb_dispose():
    '''
    usb.util.dispose_resources
    '''
    if hasattr(get_device, 'dev'):
        usb.util.dispose_resources(get_device.dev)
        delattr(get_device, 'dev')
    return ''

def TG124A_reset():
    '''
    Reset device
    '''
    dev = get_device()
    if dev == None:
        return ''
    #usb.util.dispose_resources(dev)
    #dev.set_configuration()
    dev.reset()
    if hasattr(get_device, 'dev'):
        delattr(get_device, 'dev')
    return '0'

def TG124A_freq(freq='1000'):
    '''
    Установка частоты выходного сигнала
    @param amp - частота сигнала [0.1..12400]МГц
    @return freq
    '''
    dev = get_device()
    if dev == None:
        return ''
    f = float(freq)
    f = int(f*100000)
    c = []
    for i in [0,1,2,3]:
        c.append((f >> 8*i) & 0xFF)
    msg = []
    for i in c:
        msg.append(i)
    for i in reversed(range(0, len(msg))):
        if msg[i] == 0xC0:
            msg[i] = 0xDB
            msg.insert(i + 1, 0xDC)
        elif msg[i] == 0xDB:
            msg.insert(i + 1, 0xDD)
    msg.insert(0, 0x46)
    msg.append(0xC0)
    if False:
        sys.stdout.write('tg_freq: %g ' % f)
        for i in msg: sys.stdout.write('%.2X ' % i)
        print()
    dev.write(0x02, msg, timeout=200)
    return freq

def TG124A_amp(amp='-25'):
    '''
    Установка амплитуды выходного сигнала
    @param amp - амплитуда сигнала [-40..-6]дБм
    @return amp
    '''
    dev = get_device()
    if dev == None:
        return ''
    #print('tg_amp:', amp)
    a = float(amp)
    if int(a) >= -6:
        c = 0
    elif int(a) == -7:
        c = 1
    elif int(a) <= -8:
        c = int(-2*a - 14)
    if c > 0x3F: c = 0x3F
    #print(a, hex(c))
    msg = [0x41, c, 0xc0]
    dev.write(0x02, msg, timeout=200)
    return amp

