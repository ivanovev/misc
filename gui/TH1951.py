
from util.mainwnd import monitor_cb
from collections import OrderedDict as OD
from util import Data, dev_serial_io_cb
from util.columns import *

def fmt_cb(val, read=True):
    val = float(val)
    return '%.5f' % val

def get_menu(dev):
    return OD([('Monitor', monitor_cb)])

def columns():
    return get_columns([c_serial])

def get_mntr(dev):
    data = Data('mntr', send=True, io_cb=dev_serial_io_cb)
    data.add('fetch', wdgt='entry', msg='FETCh?', width=10, fmt_cb=fmt_cb)
    data.add('diff', wdgt='entry', msg='diff', width=10, fmt_cb=fmt_cb)
    return data

