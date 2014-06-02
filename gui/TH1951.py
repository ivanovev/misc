
from util.mainwnd import monitor_cb
from collections import OrderedDict as OD
from util import Data, dev_serial_io_cb
from util.columns import *

def fmt_cb(val, read=True):
    val = float(val)
    return '%.03g' % val

def get_menu(dev):
    return OD([('Monitor', monitor_cb)])

def columns():
    return get_columns([c_serial])

def get_mntr(dev):
    data = Data('mntr', send=True, io_cb=dev_serial_io_cb)
    data.add('fetch', wdgt='entry', msg='FETCh?', width=20, fmt_cb=fmt_cb)
    return data

