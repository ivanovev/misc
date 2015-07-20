
from util.mainwnd import monitor_cb
from collections import OrderedDict as OD
from util import Data, dev_serial_io_cb, alarm_trace_cb
from util.columns import *

def fmt_cb1(val, read=True, ch=1):
    vv = val.split()
    if len(vv) >= ch:
        return '1' if vv[ch-1] == '-100000.0' else '0'

def fmt_cb2(val, read=True, ch=1):
    vv = val.split()
    if len(vv) >= ch:
        return vv[ch-1]

def get_menu(dev):
    return OD([('Monitor', monitor_cb)])

def columns():
    return get_columns([c_serial])

def get_mntr(dev):
    data = Data('mntra', send=True, io_cb=dev_serial_io_cb)
    for ch in range(1, 9):
        data.add('a%d'%ch,cmd='fetch',wdgt='alarm',msg='CH%d'%ch,fmt_cb=lambda val,read,c=ch:fmt_cb1(val,read,c),send=(ch==1),trace_cb=alarm_trace_cb)
    data.add_page('mntre', send=False)
    for ch in range(1, 9):
        v = data.add('e%d'%ch,cmd='fetch',wdgt='entry',label='CH%d'%ch,msg='CH%d'%ch,fmt_cb=lambda val,read,c=ch:fmt_cb2(val,read,c))
    data.cmds.columns = 4
    return data
