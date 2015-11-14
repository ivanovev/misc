
from collections import OrderedDict as OD
from copy import deepcopy

from util import Data, monitor_cb, process_cb, dev_io_cb
from util.columns import *

from ..srv.SDS1304CFL import get_data
from ..tools import Scdp

def columns():
    return get_columns()

def startup_cb(apps, mode, dev):
    if mode == 'scdp':
        return Scdp(dev=dev, get_data=lambda: get_data(dispose_dev=True))

def get_menu(dev):
    menu = OD()
    menu_mntr = OD()
    for i in range(1, 5):
        d = deepcopy(dev)
        d['devdata'] = 'C%d' % i
        d[c_name] = '.'.join([dev[c_name], d['devdata']])
        menu_mntr['Channel %d' % i] = lambda dev, d=d: monitor_cb(d)
    menu['Monitor'] = menu_mntr
    menu['Screenshot'] = lambda dev: process_cb('scdp', dev)
    return menu

def mntr_cmd_cb(dev, cmd, val=None, ch='C1'):
    return 'cmd %s:PAVA? %s' % (ch, cmd)

def mntr_fmt_cb(val, read=True):
    if read:
        val = val.strip('V')
        f = float(val)
        return '%g' % f
    else:
        return val

def mntr_fmt_cb2(val, read=True):
    if read:
        val = val.strip('SHz')
        if val.find('*') != -1:
            return '0'
        f = float(val)
        return '%g' % f
    else:
        return val

def get_mntr(dev):
    mntr = Data(io_cb=dev_io_cb, send=True)
    dd = 'devdata'
    def add_channel(data, ch):
        cmd_cb = lambda dev, cmd, val, c=ch: mntr_cmd_cb(dev, cmd, val, ch=c)
        mntr.add_page('%s.vpp' % ch)
        mntr.add('PKPK', wdgt='entry', msg='Vpp', cmd_cb=cmd_cb, fmt_cb=mntr_fmt_cb)
        mntr.add_page('%s.etc' % ch)
        mntr.add('MAX', label='Vmax', wdgt='entry', msg='Vmax', cmd_cb=cmd_cb, fmt_cb=mntr_fmt_cb)
        mntr.add('MIN', label='Vmin', wdgt='entry', msg='Vmin', cmd_cb=cmd_cb, fmt_cb=mntr_fmt_cb)
        mntr.add('PER', label='Period', wdgt='entry', msg='Period', cmd_cb=cmd_cb, fmt_cb=mntr_fmt_cb2)
        mntr.add('FREQ', label='Frequency', wdgt='entry', msg='Frequency', cmd_cb=cmd_cb, fmt_cb=mntr_fmt_cb2)
    if dd in dev:
        ch = dev[dd]
        add_channel(mntr, ch)
    else:
        for ch in ['C1', 'C2', 'C3', 'C4']:
            add_channel(mntr, ch)
    return mntr

