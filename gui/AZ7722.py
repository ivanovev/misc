
from collections import OrderedDict as OD
from util import Data, dev_serial_io_cb, monitor_cb
from util.columns import *

def get_menu(dev):
    return OD([('Monitor', monitor_cb)])

def columns():
    return get_columns([c_serial])

def get_mntr(dev):
    data = Data('mntr', send=True, io_cb=dev_serial_io_cb)
    data.add('CO2', wdgt='entry', msg='PPM')
    data.add('TEMP', wdgt='entry', msg='C')
    data.add('RH', wdgt='entry', msg='RH')
    return data

