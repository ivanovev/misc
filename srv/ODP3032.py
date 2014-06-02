
import usb
import argparse, sys
from util.cache import CachedDict

cache = CachedDict()

def get_device():
    if hasattr(get_device, 'dev'):
        return get_device.dev
    dev = usb.core.find(idVendor=0x5345, idProduct=0x1234)
    if dev == None:
        return
    dev.set_configuration()
    get_device.dev = dev
    return dev

def ODP3032_reset():
    """
    Reset device
    """
    dev = get_device()
    if dev == None:
        return ''
    usb.util.dispose_resources(dev)
    dev.set_configuration()
    dev.reset()
    if hasattr(get_device, 'dev'):
        delattr(get_device, 'dev')
    return '0'

def print_msg(msg):
    print(''.join([chr(i) for i in msg]))
    print(' '.join(['%.2X' % i for i in msg]))

def ODP3032_readep81():
    dev = get_device()
    if not dev:
        return ''
    msg = []
    try:
        msg = dev.read(0x81, 200)
        print_msg(msg)
    except:
        pass
    return ''.join([chr(i) for i in msg])

def ODP3032_readep0(reqtype='0x40', req='6'):
    dev = get_device()
    msg = dev.ctrl_transfer(int(reqtype, 16), int(req))
    return ''.join([chr(i) for i in msg])

def ODP3032_cmd(cmd, param, *args):
    dev = get_device()
    if not dev:
        return ''
    allargs = cmd.split() + param.split() + list(args)
    print(allargs)
    msg = [0x26]
    for a in allargs:
        for i in range(0, len(a)):
            msg.append(ord(a[i]))
        msg.append(0x2C)
    cksum = 0
    for i in range(1, len(msg)):
        cksum += msg[i]
    c = '%d' % cksum
    for i in range(0, len(c)):
        msg.append(ord(c[i]))
    msg.append(0x23)
    print_msg(msg)
    try:
        dev.write(0x03, msg)
    except:
        pass
    return ODP3032_readep81()
    #dev.write(0x03, [0x26, 0x53, 0x59, 0x4E, 0x43, 0x48, 0x52, 0x4F, 0x2C, 0x30, 0x2C, 0x36, 0x38, 0x36, 0x23])
    #dev.read(0x81, 200)

def ODP3032_SYNCHRO():
    return ODP3032_cmd('SYNCHRO', '0')

def ODP3032_cmdio(cmd, v='', index='0'):
    if v:
        ODP3032_cmd(cmd, v)
        ODP3032_cmd('SYNCHRO', '0')
        return v
    else:
        s = cache.get(lambda: ODP3032_cmd('SYNCHRO', '0'), 'SYNCHRO', duration=3)
        ss = s.split(',')
        return ss[int(index)]

def ODP3032_COMMON(mode=''):
    return ODP3032_cmdio('COMMON', mode, 1)

def ODP3032_SW1(v=''):
    return ODP3032_cmdio('SW1', v, 2)

def ODP3032_SCH1V(v=''):
    return ODP3032_cmdio('SCH1V', v, 5)

def ODP3032_SCH1C(v=''):
    return ODP3032_cmdio('SCH1C', v, 6)

def ODP3032_SW2(v='1'):
    return ODP3032_cmdio('SW2', v, 3)

def ODP3032_SCH2V(v=''):
    return ODP3032_cmdio('SCH2V', v, 14)

def ODP3032_SCH2C(v=''):
    return ODP3032_cmdio('SCH2C', v, 15)

def ODP3032_SPARAV(v=''):
    return ODP3032_cmdio('SPARAV', v, 5)

def ODP3032_SPARAC(v=''):
    return ODP3032_cmdio('SPARAC', v, 6)

def ODP3032_SSERIV(v=''):
    return ODP3032_cmdio('SSERIV', v, 5)

def ODP3032_SSERIC(v=''):
    return ODP3032_cmdio('SSERIC', v, 6)

def ODP3032_SDUAL1V(v=''):
    return ODP3032_cmdio('SDUAL1V', v, 5)

def ODP3032_SDUAL1C(v=''):
    return ODP3032_cmdio('SDUAL1C', v, 6)

def ODP3032_SDUAL2V(v=''):
    return ODP3032_cmdio('SDUAL2V', v, 14)

def ODP3032_SDUAL2C(v=''):
    return ODP3032_cmdio('SDUAL2C', v, 15)

